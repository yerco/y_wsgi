import os
from typing import Any, Dict

from src.app import App
from src.core.module import Module
from src.core.app_context import AppContext
from src.config_loader import load_config


class AppRegistry:
    def __init__(self):
        self._apps: Dict[str, App] = {}
        self.modules: Dict[str, Module] = {}

    def create_app(self, name: str) -> App:
        if name in self._apps:
            raise ValueError(f'App with {name} already exists')

        app = App(name)

        # Set the AppContext for this specific app
        base_dir = self._get_app_base_dir(name)
        # print("Checking base dir:", base_dir)
        config = load_config(name, base_dir)
        # print("Loaded config:", config)
        app_context = AppContext()
        app_context.set_context(name, base_dir, config)
        app_context.set_current_app(name)
        app.set_context(app_context)

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

    @staticmethod
    def _get_app_base_dir(app_name: str) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        base_dir = os.path.join(parent_dir, app_name)
        return base_dir if os.path.isdir(base_dir) else parent_dir
