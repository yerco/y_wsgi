from typing import Dict

from src.app import App
from src.core.module import Module


class AppRegistry:
    def __init__(self):
        self._apps: Dict[str, App] = {}
        self.modules: Dict[str, 'Module'] = {}

    def create_app(self, name: str) -> App:
        if name in self._apps:
            raise ValueError(f'App with {name} already exists')
        app = App()
        self._apps[name] = app
        return app

    def create_module(self, name: str, app: App) -> Module:
        module = Module(name, app)
        self.modules[name] = module
        return module

    def get_app(self, name: str) -> App:
        return self._apps.get(name)

    def list_apps(self) -> Dict[str, App]:
        return self._apps
