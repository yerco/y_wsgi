from typing import Union, Iterable

from src.core.response import Response
from src.http.response_builder import ResponseBuilder


class HTTPResponseBuilder(ResponseBuilder):
    def __init__(self):
        self._response = Response()

    def set_status(self, status: Union[int, str]) -> 'HTTPResponseBuilder':
        self._response.status = status
        return self

    def set_header(self, name: str, value: str) -> 'HTTPResponseBuilder':
        self._response.set_header(name, value)
        return self

    def set_body(self, body: Union[bytes, str]) -> 'HTTPResponseBuilder':
        if isinstance(body, str):
            body = [body.encode('utf-8')]
        elif isinstance(body, bytes):
            body = [body]
        elif isinstance(body, Iterable):
            body = [chunk.encode('utf-8') if isinstance(chunk, str) else chunk for chunk in body]
        self._response.body = body
        return self

    def build(self) -> Response:
        return self._response
