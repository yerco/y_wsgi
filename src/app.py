from typing import Callable, Dict, Any, List, Tuple, Iterable, Type, Union, Optional

from src.hooks import Hooks
from src.middleware import Middleware
from src.request import Request
from src.response import Response
from src.router import Router
from src.view import View

"""
A string (str) for the status.
A list of tuples (List[Tuple[str, str]]) for the response headers.
An optional third argument of any type (Any) for exception information.
"""
StartResponseType = Callable[[str, List[Tuple[str, str]], Any], None]

HandlerType = Union[Type[View], Callable[[Request, Dict[str, Any]], Response]]


class App:
    def __init__(self):
        self.router = Router()
        self.middlewares: List[Middleware] = []
        self.hooks = Hooks()

    # decorator
    def route(self, path: str) -> Callable[[HandlerType], HandlerType]:
        def wrapper(handler: HandlerType) -> HandlerType:
            self.router.add_route(path, handler)
            return handler
        return wrapper

    def use_middleware(self, middleware_cls: Callable) -> None:
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
        # print('request method: ', request.method)
        # print('request.path', request.path)
        # print('request.headers', request.headers)

        # Apply before_first_request hooks
        if self.hooks.first_request:
            for hook in self.hooks.before_first_request_hooks:
                hook()
            self.hooks.first_request = False

        # Apply middleware and before_request hooks
        response = self._apply_before_request_middlewares_and_hooks(request)
        if response:
            return self._start_response(response, start_response)

        handler, params = self.router.match(request.path)
        if handler:
            if isinstance(handler, type) and issubclass(handler, View):
                handler_instance = handler()
                response = handler_instance(request, **params)
            elif callable(handler):
                response = handler(request, **params)
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
        response = self._apply_after_request_middlewares_and_hooks(request, response)
        # Apply teardown_request hooks
        self._apply_teardown_request_hooks(request)

        return self._start_response(response, start_response)

    def _apply_before_request_middlewares_and_hooks(self, request: Request) -> Optional[Response]:
        for hook in self.hooks.before_request_hooks:
            hook()
        for middleware in self.middlewares:
            response = middleware.before_request(request)
            if response:
                return response
        return None

    def _apply_after_request_middlewares_and_hooks(self, request: Request, response: Response) -> Response:
        for middleware in self.middlewares:
            response = middleware.after_request(request, response)
        for hook in self.hooks.after_request_hooks:
            hook()
        return response

    def _apply_teardown_request_hooks(self, request: Request) -> None:
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
