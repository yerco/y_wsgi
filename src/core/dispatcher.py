from typing import Callable, Dict, Any, Tuple, Iterable
from src.core.response import Response
from src.app import App

StartResponseType = Callable[[str, list[Tuple[str, str]], Any], None]


class Dispatcher:
    def __init__(self):
        self.apps: Dict[str, Callable[[Dict[str, Any], StartResponseType], Iterable[bytes]]] = {}

    def add_app(self, path_prefix: str, app: App):
        # Ensure the root application is always checked last to handle overlapping paths
        if path_prefix == '/':
            self.apps[path_prefix] = app
        else:
            self.apps = {path_prefix: app, **self.apps}

    def __call__(self, environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
        path = environ.get('PATH_INFO', '')

        # Handle /favicon.ico request
        if path == '/favicon.ico':
            response = Response(status='204 No Content')  # TODO serve an actual favicon file
            return response(environ, start_response)

        for prefix, app in self.apps.items():
            prefix: str
            app: App
            if path.startswith(prefix):
                # print(f"Setting context for app: {app.name}")
                app.context.set_current_app_name(app.name)
                try:
                    return app(environ, start_response)
                finally:
                    # print("Resetting Current app Context name to None")
                    app.context.set_current_app_name(None)
        response = Response(status='404 Not Found', body=[b'Not Found'])
        return response(environ, start_response)
