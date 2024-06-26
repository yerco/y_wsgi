import re
from typing import Type, Union, Callable, Optional, Tuple, Dict, Any

from src.request import Request
from src.response import Response
from src.view import View

HandlerType = Union[Type[View], Callable[[Request], Response]]


class Route:
    def __init__(self, path: str, handler: HandlerType) -> None:
        self.path = path
        self.handler = handler
        self.regex = re.compile(self._convert_path_to_regex(path))

    def match(self, path: str) -> Optional[Tuple[Callable, Dict[str, Any]]]:
        match = self.regex.match(path)
        if match:
            return self.handler, match.groupdict()
        return None

    @staticmethod
    def _convert_path_to_regex(path: str) -> str:
        path = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
        return f'^{path}$'
