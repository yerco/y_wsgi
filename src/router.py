from typing import List, Optional, Type

from src.route import Route
from src.view import View


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, path: str, handler: Type[View]) -> None:
        self.routes.append(Route(path, handler))

    def match(self, path: str) -> Optional[Type[View]]:
        for route in self.routes:
            if route.match(path):
                return route.handler
        return None
