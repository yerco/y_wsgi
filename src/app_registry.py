import os
from typing import Any, Dict, List

from src.app import App
from src.core.module import Module
from src.core.app_context import AppContext
from src.config_loader import load_config


class AppRegistry:
    def __init__(self):
        self._apps: Dict[str, App] = {}

    def create_app(self, name: str) -> App:
        if name in self._apps:
            raise ValueError(f'App with {name} already exists')

        try:
            # Set the AppContext for this specific app
            base_dir = self._get_app_base_dir(name)
            # print("Checking base dir:", base_dir)
            config = load_config(name, base_dir)
            app = App(name, config.TEMPLATE_ENGINE if config.TEMPLATE_ENGINE else None)
            # print("Loaded config:", config)
            app_context = AppContext()
            app_context.set_context(name, base_dir, config, app)
            app_context.set_current_app_name(name)
            app.set_context(app_context)

            self._apps[name] = app

            return app
        except KeyError as e:
            raise ValueError(f'Missing required configuration key: {e}')
        except Exception as e:
            raise RuntimeError(f'Error creating app {name}: {e}')

    def create_module(self, module_name: str, app: App) -> Module:
        if app.name not in self._apps:
            raise ValueError(f'App {app.name} does not exist')
        base_dir = self._get_app_base_dir(app.name)
        module_dir = os.path.join(base_dir, module_name)
        module = Module(module_name, app, module_dir)
        app.add_module(module_name, module)
        return module

    def get_app(self, name: str) -> App:
        app = self._apps.get(name)
        if app:
            app.get_context().set_current_app_name(name)
        return app

    def get_module(self, app_name: str, module_name: str) -> Module:
        app = self.get_app(app_name)
        if app:
            return app.modules.get(module_name)
        raise ValueError(f'App {app_name} does not exist')

    def list_apps(self) -> List[str]:
        return list(self._apps.keys())

    @staticmethod
    def _get_app_base_dir(app_name: str) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        base_dir = os.path.join(parent_dir, app_name)
        return base_dir if os.path.isdir(base_dir) else parent_dir
