from abc import ABC, abstractmethod
from typing import Union

from src.core.response import Response


class ResponseBuilder(ABC):
    @abstractmethod
    def set_status(self, status: Union[int, str]) -> 'ResponseBuilder':
        pass

    @abstractmethod
    def set_header(self, name: str, value: str) -> 'ResponseBuilder':
        pass

    @abstractmethod
    def set_body(self, body: Union[bytes, str]) -> 'ResponseBuilder':
        pass

    @abstractmethod
    def build(self) -> Response:
        pass
