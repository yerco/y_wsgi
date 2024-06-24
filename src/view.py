from typing import Callable, Dict, Optional

from src.request import Request
from src.response import Response


class View:
    def __init__(self):
        self.method_map: Dict[str, Callable[[Request], Response]] = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete,
            'head': self.head,
            'options': self.options,
            'trace': self.trace,
        }

    def __call__(self, request: Request) -> Response:
        return self.execute(request)

    def execute(self, request: Request) -> Response:
        method = request.method.lower()
        handler_method = self.method_map.get(method, self.http_method_not_allowed)
        return handler_method(request)

    def http_method_not_allowed(self, request: Request) -> Response:
        return Response(status='405 Method Not Allowed', headers=[('Content-type', 'text/plain')],
                        body=[b'Method Not Allowed'])

    def get(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def post(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def put(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def delete(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def head(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def options(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)

    def trace(self, request: Request) -> Optional[Response]:
        return self.http_method_not_allowed(request)
