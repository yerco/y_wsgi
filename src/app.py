from typing import Callable, Dict, Any, List, Tuple, Iterable, Type, Union, Optional

from src.hooks.hooks import Hooks
from src.middleware.middleware import Middleware
from src.core.request import Request
from src.core.request_context import RequestContext
from src.core.response import Response
from src.routing.router import Router
from src.core.view import View
from src.core.app_context import AppContext
from src.templates.template_engine import TemplateEngine
from src.templates.simple_template_engine import SimpleTemplateEngine
from src.utils.template_scanner import TemplateScanner

"""
A string (str) for the status.
A list of tuples (List[Tuple[str, str]]) for the response headers.
An optional third argument of any type (Any) for exception information.
"""
StartResponseType = Callable[[str, List[Tuple[str, str]], Any], None]

HandlerType = Union[Type[View], Callable[[Request, Dict[str, Any]], Response]]


class App:
    def __init__(self, name: str, template_engine: Optional[TemplateEngine] = None):
        self.name = name
        self.router = Router()
        self.middlewares: List[Middleware] = []
        self.hooks = Hooks()
        self.context: Optional[AppContext] = None

        # Initialize the template engine
        if template_engine is None:
            self.template_engine = SimpleTemplateEngine(template_dir='templates')
        else:
            self.template_engine = template_engine

        # Scan for template directories
        try:
            self.template_directory = self.scan_template_directory()
            module, module_templates_dir = list(self.template_directory.items())[0]
            self.template_engine.template_dir = module_templates_dir
        except FileNotFoundError as e:
            print(f"Template directory not found: {e}")

    def scan_template_directory(self) -> Dict[str, str]:
        scanner = TemplateScanner(base_dir=self.get_base_dir())
        return scanner.scan()

    def get_base_dir(self) -> str:
        if self.context:
            app_config = self.context.get_config(self.name)
            if app_config:
                return app_config.get('base_dir', '.')
        return '.'

    def set_context(self, context: AppContext) -> None:
        self.context = context

    def get_context(self) -> Optional[AppContext]:
        return self.context

    # decorator
    def route(self, path: str, methods: List[str] = None) -> Callable[[HandlerType], HandlerType]:
        def wrapper(handler: HandlerType) -> HandlerType:
            self.router.add_route(path, handler, methods)
            return handler
        return wrapper

    def use_middleware(self, middleware_cls: Callable[[], Middleware]) -> None:
        self.middlewares.append(middleware_cls())

    def before_request(self, hook: Callable) -> None:
        self.hooks.add_before_request(hook)

    def after_request(self, hook: Callable) -> None:
        self.hooks.add_after_request(hook)

    def teardown_request(self, hook: Callable) -> None:
        self.hooks.add_teardown_request(hook)

    def before_first_request(self, hook: Callable) -> None:
        self.hooks.add_before_first_request(hook)

    def __call__(self, environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
        request = Request(environ)
        request_context = RequestContext(request, self.context)

        # Apply before_first_request hooks
        if self.hooks.first_request:
            for hook in self.hooks.before_first_request_hooks:
                hook()
            self.hooks.first_request = False

        # Apply middleware and before_request hooks
        response = self._apply_before_request_middlewares_and_hooks(request_context)
        if response:
            return self._start_response(response, start_response)

        handler, params = self.router.match(request_context.path, request_context.method)
        # print(f"Matched handler: {handler}, Params: {params}")

        if handler:
            if isinstance(handler, type) and issubclass(handler, View):
                handler_instance = handler()
                response = handler_instance(request_context, **params)
            elif callable(handler):
                response = handler(request_context, **params)
            else:
                response = Response(status='500 Internal Server Error', headers=[('Content-type', 'text/plain')],
                                    body=[b'Internal Server Error'])
        else:
            response = Response(status='404 Not Found', headers=[('Content-type', 'text/plain')], body=[b'Not Found'])

        # Ensure response is always a Response object
        if not isinstance(response, Response):
            response = Response(status='500 Internal Server Error', headers=[('Content-type', 'text/plain')],
                                body=[b'Internal Server Error'])

        # Apply after_request hooks and middleware
        response = self._apply_after_request_middlewares_and_hooks(request_context, response)
        # Apply teardown_request hooks
        self._apply_teardown_request_hooks(request_context.request)

        return self._start_response(response, start_response)

    def _apply_before_request_middlewares_and_hooks(self, request_context: RequestContext) -> Optional[Response]:
        if self.hooks.first_request:
            for hook in self.hooks.before_first_request_hooks:
                hook()
            self.hooks.first_request = False  # Ensure it only runs once

        for hook in self.hooks.before_request_hooks:
            hook()

        for middleware in self.middlewares:
            response = middleware.before_request(request_context)
            if response:
                return response
        return None

    def _apply_after_request_middlewares_and_hooks(self, request_context: RequestContext, response: Response) -> Response:
        for middleware in self.middlewares:
            response = middleware.after_request(request_context, response)
        for hook in self.hooks.after_request_hooks:
            hook()
        return response

    def _apply_teardown_request_hooks(self, request_context: Request) -> None:
        for hook in self.hooks.teardown_request_hooks:
            hook()

    @staticmethod
    def _start_response(response: Response, start_response: StartResponseType) -> Iterable[bytes]:
        response_status: str = response.status
        response_headers: List[Tuple[str, str]] = response.headers

        # Ensure that the response status and headers are correctly typed
        assert isinstance(response_status, str), f"Expected str, got {type(response_status).__name__}"
        assert isinstance(response_headers, list) and all(isinstance(header, tuple) for header in response_headers), \
            "Headers should be a list of tuples"

        start_response(response_status, response_headers, None)

        # An iterable yielding byte strings
        return response.body

    def render_template(self, template_name: str, template_vars: Dict[str, Any]) -> str:
        return self.template_engine.render(template_name, template_vars)
