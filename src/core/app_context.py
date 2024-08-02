import threading

from typing import Any, Dict, Optional, TYPE_CHECKING

from src.forms.form_mediator import FormMediator

if TYPE_CHECKING:
    from src.app import App


class AppContext:
    _configs: Dict[str, Dict[str, Optional[str]]] = {}  # Global dictionary for storing app contexts
    _current_app_name = threading.local()  # Thread-local storage for current app
    _current_module_dir = threading.local()
    _form_mediator: Optional[FormMediator] = None

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
        return getattr(self._current_app_name, 'app_name', None)

    def reset_current_app_name(self):
        self._current_app_name.app_name = None

    def get_config(self, app_name: str = None) -> Optional[Dict[str, Optional[str]]]:
        if app_name is None:
            app_name = self.get_current_app_name()
        context = self._configs.get(app_name, None)
        return context.get('config', None) if context else None

    def get_full_context(self, app_name: str) -> Optional[Dict[str, Optional[str]]]:
        return self._configs.get(app_name, None)

    def get_app_instance(self, app_name: str):  # -> App | None:
        context = self._configs.get(app_name, None)
        return context.get('app_instance', None) if context else None

    def render_template(self, app_name: str, template_name: str, template_vars: Dict[str, Any]) -> str:
        app_instance = self.get_app_instance(app_name)
        if app_instance:
            return app_instance.render_template(template_name, template_vars)
        raise ValueError(f"App instance for {app_name} not found.")

    def get_modules(self):
        app_name = self.get_current_app_name()
        app_instance = self.get_app_instance(app_name)
        return app_instance.modules if app_instance else None

    def set_current_module_dir(self, module_dir: str):
        self._current_module_dir.module_dir = module_dir

    def get_current_module_dir(self) -> Optional[str]:
        return getattr(self._current_module_dir, 'module_dir', None)

    def set_form_mediator(self, form_mediator: FormMediator):
        self._form_mediator = form_mediator

    def get_form_mediator(self) -> Optional[FormMediator]:
        if self._form_mediator is None:
            self._form_mediator = FormMediator()  # Initialize it when accessed for the first time
        return self._form_mediator
