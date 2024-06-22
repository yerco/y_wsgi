from typing import Callable

from src.request import Request
from src.response import Response


class Route:
    def __init__(self, path: str, handler: Callable[[Request], Response]) -> None:
        self.path = path
        self.handler = handler

    def match(self, path: str) -> bool:
        return self.path == path
