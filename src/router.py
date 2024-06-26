from typing import List, Optional, Type, Union, Callable, Tuple, Dict, Any

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

    def match(self, path: str) -> Optional[Tuple[Callable, Dict[str, Any]]]:
        for route in self.routes:
            match = route.match(path)
            if match:
                return match
        return None
