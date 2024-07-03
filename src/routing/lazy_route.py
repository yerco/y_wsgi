import re
from typing import Type, Union, Callable, Optional, Tuple, Dict, Any, List

from src.core.request import Request
from src.core.response import Response
from src.core.view import View

HandlerType = Union[Type[View], Callable[[Request, Dict[str, Any]], Response]]


class LazyRoute:
    def __init__(self, path: str, handler_factory: Optional[Callable[[], HandlerType]] = None,
                 methods: List[str] = None) -> None:
        self.path = path
        self._handler = None
        self._handler_factory = handler_factory
        self.methods = methods if methods else ['GET']
        self.regex = re.compile(self._convert_path_to_regex(path))
        print(f"Converted path '{self.path}' to regex '{self.regex.pattern}'")  # Debugging output

    @property
    def handler(self) -> HandlerType:
        if self._handler is None:
            print(f"Instantiating handler for path: {self.path}")
            self._handler = self._handler_factory()
        return self._handler

    def match(self, path: str, method: str) -> Optional[Tuple[HandlerType, Dict[str, Any]]]:
        if method not in self.methods:
            return None
        match = self.regex.match(path)
        if match:
            return self.handler, match.groupdict()
        return None

    @staticmethod
    def _convert_path_to_regex(path: str) -> str:
        print(f"Original path: {path}")  # Debugging output

        # Patterns to replace
        patterns = {
            r'<int:(\w+)>': r'(?P<\1>[0-9]+)',
            r'<str:(\w+)>': r'(?P<\1>[^/]+)',
            r'<(\w+)>': r'(?P<\1>[^/]+)',  # General pattern for other types
        }

        # Apply replacements one by one and return immediately once a match is found
        for pattern, replacement in patterns.items():
            new_path = re.sub(pattern, replacement, path)
            if new_path != path:
                print(f"Converted regex path: {new_path}")  # Debugging output
                return f'^{new_path}$'

        # If no patterns matched, return the original path wrapped in regex start and end anchors
        print(f"No patterns matched. Converted regex path: {path}")  # Debugging output
        return f'^{path}$'
