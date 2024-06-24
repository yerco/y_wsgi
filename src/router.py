from typing import List, Optional, Type, Union, Callable

from src.request import Request
from src.response import Response
from src.route import Route
from src.view import View

HandlerType = Union[Type[View], Callable[[Request], Response]]


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, path: str, handler: HandlerType) -> None:
        self.routes.append(Route(path, handler))

    def match(self, path: str) -> Optional[HandlerType]:
        for route in self.routes:
            if route.match(path):
                return route.handler
        return None
