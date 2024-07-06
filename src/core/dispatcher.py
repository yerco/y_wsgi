from typing import Callable, Dict, Any, Tuple, Iterable
from src.core.response import Response

StartResponseType = Callable[[str, list[Tuple[str, str]]], Any]


class Dispatcher:
    def __init__(self):
        self.apps: Dict[str, Callable[[Dict[str, Any], StartResponseType], Iterable[bytes]]] = {}

    def add_app(self, path_prefix: str,
                app: Callable[[Dict[str, Any], StartResponseType], Iterable[bytes]]):
        # Ensure the root application is always checked last to handle overlapping paths
        if path_prefix == '/':
            self.apps[path_prefix] = app
        else:
            self.apps = {path_prefix: app, **self.apps}

    def __call__(self, environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
        path = environ.get('PATH_INFO', '')
        for prefix, app in self.apps.items():
            if path.startswith(prefix):
                return app(environ, start_response)
        response = Response(status='404 Not Found', body=[b'Not Found'])
        return response(environ, start_response)
