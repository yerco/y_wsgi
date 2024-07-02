from typing import Callable, Dict, Any
from src.core.request import Request
from src.core.response import Response

# Define a type alias for the method signatures
HandlerFunction = Callable[[Request, Dict[str, Any]], Response]


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

    def __call__(self, request: Request, **params: Any) -> Response:
        return self.execute(request, **params)

    def execute(self, request: Request, **params: Any) -> Response:
        method = request.method.lower()
        handler_method = self.method_map.get(method, self.http_method_not_allowed)
        return handler_method(request, **params)

    def http_method_not_allowed(self, request: Request, params: Dict[str, Any]) -> Response:
        return Response(status='405 Method Not Allowed', headers=[('Content-type', 'text/plain')],
                        body=[b'Method Not Allowed'])

    def get(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def post(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def put(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def delete(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def head(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def options(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)

    def trace(self, request: Request, params: Dict[str, Any] = None) -> Response:
        return self.http_method_not_allowed(request, params)
