from typing import Callable, Dict, Any, List, Tuple, Iterable

from src.request import Request
from src.response import Response
from src.router import Router

"""
A string (str) for the status.
A list of tuples (List[Tuple[str, str]]) for the response headers.
An optional third argument of any type (Any) for exception information.
"""
StartResponseType = Callable[[str, List[Tuple[str, str]], Any], None]


class App:
    def __init__(self):
        self.router = Router()

    def route(self, path: str) -> Callable[[Callable[[Request], Response]], Callable[[Request], Response]]:
        def wrapper(handler: Callable[[Request], Response]) -> Callable[[Request], Response]:
            self.router.add_route(path, handler)
            return handler
        return wrapper

    def __call__(self, environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
        request = Request(environ)
        # print('request method: ', request.method)
        # print('request.path', request.path)
        # print('request.headers', request.headers)

        handler = self.router.match(request.path)
        if handler:
            response = handler(request)
        else:
            response = Response(status='404 Not Found', headers=[('Content-type', 'text/plain')], body=[b'Not Found'])

        response_status: str = response.status
        response_headers: List[Tuple[str, str]] = response.headers

        # Ensure that the response status and headers are correctly typed
        assert isinstance(response_status, str), f"Expected str, got {type(response_status).__name__}"
        assert isinstance(response_headers, list) and all(isinstance(header, tuple) for header in response_headers), \
            "Headers should be a list of tuples"

        start_response(response_status, response_headers, None)

        # An iterable yielding byte strings
        return response
