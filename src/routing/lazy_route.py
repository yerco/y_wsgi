import re
from typing import Type, Union, Callable, Optional, Tuple, Dict, Any

from src.core.request import Request
from src.core.response import Response
from src.core.view import View

HandlerType = Union[Type[View], Callable[[Request, Dict[str, Any]], Response]]


class LazyRoute:
    def __init__(self, path: str, handler_factory: Optional[Callable[[], HandlerType]] = None) -> None:
        self.path = path
        self._handler = None
        self._handler_factory = handler_factory
        self.regex = re.compile(self._convert_path_to_regex(path))

    @property
    def handler(self) -> HandlerType:
        if self._handler is None:
            print(f"Instantiating handler for path: {self.path}")
            self._handler = self._handler_factory()
        return self._handler

    def match(self, path: str) -> Optional[Tuple[HandlerType, Dict[str, Any]]]:
        match = self.regex.match(path)
        if match:
            return self.handler, match.groupdict()
        return None

    @staticmethod
    def _convert_path_to_regex(path: str) -> str:
        path = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        return f'^{path}$'
