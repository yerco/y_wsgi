import threading

from typing import Dict, Optional


class AppContext:
    _contexts: Dict[str, Dict[str, Optional[str]]] = {}  # Global dictionary for storing app contexts
    _current_app = threading.local()  # Thread-local storage for current app

    def set_context(self, app_name: str, base_dir: str, config: Dict[str, Optional[str]] = None):
        self._contexts[app_name] = {
            'app_name': app_name,
            'base_dir': base_dir,
            'config': config,
        }

    def set_current_app(self, app_name: str | None):
        self._current_app.app_name = app_name  # Store current app name in thread-local storage

    def get_current_app(self) -> Optional[str]:
        # Retrieve current app name from thread-local storage
        current_app_name = getattr(self._current_app, 'app_name', None)
        return current_app_name

    def reset_current_app(self):
        self._current_app.app_name = None

    def get_context(self, app_name: str) -> Optional[Dict[str, Optional[str]]]:
        return self._contexts.get(app_name, None)
