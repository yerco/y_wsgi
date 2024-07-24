import threading

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App


class AppContext:
    _configs: Dict[str, Dict[str, Optional[str]]] = {}  # Global dictionary for storing app contexts
    _current_app_name = threading.local()  # Thread-local storage for current app

    def set_context(self, app_name: str, base_dir: str, config: Dict[str, Optional[str]] = None,
                    app_instance: Optional[Any] = None):
        self._configs[app_name] = {
            'app_name': app_name,
            'base_dir': base_dir,
            'config': config,
            'app_instance': app_instance
        }

    def set_current_app_name(self, app_name: str | None):
        self._current_app_name.app_name = app_name  # Store current app name in thread-local storage

    def get_current_app_name(self) -> Optional[str]:
        # Retrieve current app name from thread-local storage
        current_app_name = getattr(self._current_app_name, 'app_name', None)
        return current_app_name

    def reset_current_app_name(self):
        self._current_app_name.app_name = None

    def get_config(self, app_name: str) -> Optional[Dict[str, Optional[str]]]:
        return self._configs.get(app_name, None)

    def get_app_instance(self, app_name: str):  # -> App | None:
        app_context = self.get_config(app_name)
        if app_context:
            return app_context.get('app_instance', None)
        return None

    def render_template(self, app_name: str, template_name: str, template_vars: Dict[str, Any]) -> str:
        app_instance = self.get_app_instance(app_name)
        if app_instance:
            return app_instance.render_template(template_name, template_vars)
        raise ValueError(f"App instance for {app_name} not found.")
