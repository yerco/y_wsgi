from typing import List, Optional, Type, Union, Callable, Tuple, Dict

from src.core.request import Request
from src.core.response import Response
from src.routing.lazy_route import LazyRoute
from src.core.view import View

HandlerType = Union[Type[View], Callable[..., Response]]


class Router:
    def __init__(self):
        self.routes: List[LazyRoute] = []

    def add_route(self, path: str, handler: HandlerType, methods: List[str]) -> None:
        self.routes.append(LazyRoute(path, handler_factory=lambda: handler, methods=methods))

    def match(self, path: str, method: str) -> Tuple[Optional[HandlerType], Dict[str, str]]:
        # Strip query parameters from the path
        path = path.split('?')[0]
        for route in self.routes:
            match = route.match(path, method)
            if match:
                print(f"Route matched: {route.path}")
                return match
        print("No route matched")
        return None, {}
