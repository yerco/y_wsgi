from typing import Dict, Any, Optional, List, Tuple
from src.app import App
from src.core.response import Response


class FrameworkTestClient:
    def __init__(self, app: App):
        self.app = app
        self.response_headers: List[Tuple[str, str]] = []

    def _make_request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None,
                      headers: Optional[Dict[str, str]] = None) -> Response:
        query_string = ''
        if '?' in path:
            path, query_string = path.split('?', 1)

        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'wsgi.input': data or b'',
            'CONTENT_LENGTH': str(len(data or b'')),
            'CONTENT_TYPE': 'application/json',
        }

        if headers:
            for header, value in headers.items():
                environ[f'HTTP_{header.upper().replace("-", "_")}'] = value

        response_body = self.app(environ, self._start_response)
        response = Response(status='200 OK', headers=self.response_headers, body=response_body)
        return response

    def _start_response(self, status: str, headers: list, exc_info: Optional[Any] = None) -> None:
        self.response_status = status
        self.response_headers = headers

    def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Response:
        return self._make_request('GET', path, headers=headers)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Response:
        return self._make_request('POST', path, data=data, headers=headers)
