from typing import Callable, Dict, Any
from src.core.request_context import RequestContext
from src.core.response import Response

# Define a type alias for the method signatures
HandlerFunction = Callable[[RequestContext, Dict[str, Any]], Response]


class View:
    def __init__(self):
        # Type hint for method_map
        self.method_map: Dict[str, HandlerFunction] = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete,
            'head': self.head,
            'options': self.options,
            'trace': self.trace,
        }

    def __call__(self, request_context: RequestContext, **params: Any) -> Response:
        return self.execute(request_context, **params)

    def execute(self, request_context: RequestContext, **params: Any) -> Response:
        method = request_context.method.lower()
        handler_method = self.method_map.get(method, self.http_method_not_allowed)
        return handler_method(request_context, **params)

    def http_method_not_allowed(self, request_context: RequestContext, params: Dict[str, Any]) -> Response:
        return Response(status='405 Method Not Allowed', headers=[('Content-type', 'text/plain')],
                        body=[b'Method Not Allowed'])

    def get(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def post(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def put(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def delete(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def head(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def options(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    def trace(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request_context, params)

    @classmethod
    def as_view(cls, *class_args, **class_kwargs):
        def view(request_context: RequestContext, **params: Any) -> Response:
            # Create an instance of the class with the provided arguments
            self = cls(*class_args, **class_kwargs)
            # Execute the view instance
            return self(request_context, **params)
        return view
