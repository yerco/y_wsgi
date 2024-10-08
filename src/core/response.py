from typing import Union, Iterable, List, Tuple, Generator, Dict


class Response:
    def __init__(self, body: Union[bytes, Iterable[bytes]] = b'', status: Union[int, str] = 200,
                 headers: List[Tuple[str, str]] = None) -> None:
        if isinstance(body, str):
            body = body.encode()
        elif isinstance(body, bytes):
            body = [body]  # Ensure body is an iterable of bytes
        self.body: Union[bytes, Iterable[bytes]] = body
        self._status: str = self._init_status(status)
        self.headers_dict = dict(headers) if headers else {}

    @property
    def headers(self) -> List[Tuple[str, str]]:
        return list(self.headers_dict.items())

    # Converts an integer status code to a status message
    def _init_status(self, status: Union[int, str]) -> str:
        if isinstance(status, int):
            return f'{status} {self._status_message(status)}'
        return status

    def __call__(self, environ, start_response):
        # Start the WSGI response
        start_response(self._status, self.headers)
        # Return the body as an iterable
        return self

    @staticmethod
    def _status_message(status_code: int) -> str:
        # A simple mapping of status codes to messages
        # This should be expanded with all the relevant HTTP status codes and messages.
        status_messages = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }
        return status_messages.get(status_code, "Unknown Status")

    # Sets a header, replacing it if it already exists
    def set_header(self, name: str, value: str) -> None:
        self.headers_dict[name] = value

    def __iter__(self) -> Generator[bytes, None, None]:
        # Convert the body to an iterable
        if isinstance(self.body, bytes):
            yield self.body
        else:
            for chunk in self.body:
                if not isinstance(chunk, bytes):
                    raise TypeError('%r is not a byte' % chunk)
                yield chunk

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: Union[int, str]) -> None:
        self._status = self._init_status(value)

    # Extracts the status code from the status message
    @property
    def status_code(self) -> int:
        return int(self.status.split()[0])

    # Extracts the status message from the status
    @property
    def status_message(self) -> str:
        return " ".join(self.status.split()[1:])
