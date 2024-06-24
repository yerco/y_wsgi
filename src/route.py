from typing import Type

from src.view import View


class Route:
    def __init__(self, path: str, handler: Type[View]) -> None:
        self.path = path
        self.handler = handler

    def match(self, path: str) -> bool:
        return self.path == path
