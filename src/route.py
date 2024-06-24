from typing import Type, Union, Callable

from src.request import Request
from src.response import Response
from src.view import View

HandlerType = Union[Type[View], Callable[[Request], Response]]


class Route:
    def __init__(self, path: str, handler: HandlerType) -> None:
        self.path = path
        self.handler = handler

    def match(self, path: str) -> bool:
        return self.path == path
