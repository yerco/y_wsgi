from typing import Callable, List, Optional

from src.request import Request
from src.response import Response
from src.route import Route


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, path: str, handler: Callable[[Request], Response]) -> None:
        self.routes.append(Route(path, handler))

    def match(self, path: str) -> Optional[Callable[[Request], Response]]:
        for route in self.routes:
            if route.match(path):
                return route.handler
        return None
