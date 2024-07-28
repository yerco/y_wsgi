from typing import List, Optional, Type, Union, Callable, Tuple, Dict

from src.core.request import Request
from src.core.response import Response
from src.routing.lazy_route import LazyRoute
from src.core.view import View

HandlerType = Union[Type[View], Callable[..., Response]]


class Router:
    def __init__(self):
        self.routes: List[LazyRoute] = []

    def add_routes(self, routes: List[Tuple[str, HandlerType, List[str]]]) -> None:
        for path, handler, methods in routes:
            self.add_route(path, handler, methods)

    def add_route(self, path: str, module_dir: str, handler: HandlerType, methods: List[str]) -> None:
        self.routes.append(LazyRoute(path, module_dir=module_dir, handler_factory=lambda: handler, methods=methods))

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

    def get_module_dir(self, path: str) -> Optional[str]:
        for route, module_dir, handler, methods in self.routes:
            if path == route:
                return module_dir
        return None
