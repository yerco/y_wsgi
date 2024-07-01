from typing import List, Optional, Type, Union, Callable, Tuple, Dict, Any

from src.request import Request
from src.response import Response
from src.lazy_route import LazyRoute
from src.view import View

HandlerType = Union[Type[View], Callable[[Request], Response]]


class Router:
    def __init__(self):
        self.routes: List[LazyRoute] = []

    def add_route(self, path: str, handler: HandlerType) -> None:
        self.routes.append(LazyRoute(path, handler_factory=lambda: handler))

    def match(self, path: str) -> Tuple[Optional[HandlerType], Dict[str, str]]:
        for route in self.routes:
            match = route.match(path)
            if match:
                print(f"Route matched: {route.path}")
                return match
        print("No route matched")
        return None, {}
