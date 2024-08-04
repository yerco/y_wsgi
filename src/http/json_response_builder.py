import json
from typing import Union, Dict, Any

from src.core.response import Response
from src.http.response_builder import ResponseBuilder


class JSONResponseBuilder(ResponseBuilder):
    def __init__(self):
        super().__init__()
        self._response = Response()
        self.set_header('Content-Type', 'application/json')

    def set_status(self, status: Union[int, str]) -> 'JSONResponseBuilder':
        self._response.status = status
        return self

    def set_header(self, name: str, value: str) -> 'JSONResponseBuilder':
        self._response.set_header(name, value)
        return self

    def set_body(self, body: Union[Dict[str, Any], str, bytes]) -> 'JSONResponseBuilder':
        if isinstance(body, dict):
            body = json.dumps(body).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        elif isinstance(body, bytes):
            pass  # If it's already bytes, we assume it's in the correct format
        self._response.body = [body]  # Ensure the body is a list of bytes
        return self

    def build(self) -> Response:
        return self._response
