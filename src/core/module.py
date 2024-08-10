from typing import List, Callable, Type, Any

from src.app import App
from src.database.orm_interface import ORMInterface
from src.middleware.middleware import Middleware
from src.hooks.hooks import Hooks
from src.plugins.base_plugin import BasePlugin
from src.plugins.plugin_loader import initialize_module_plugins


class Module:
    def __init__(self, name: str, app: App, directory: str):
        self.name = name
        self.app = app
        self.middlewares: List[Middleware] = []
        self.hooks = Hooks()
        self.directory = directory
        self.plugins: List[BasePlugin] = []
        # Initialize plugins for this module
        self._initialize_plugins()

    def _initialize_plugins(self):
        # Use the plugin loader to discover and initialize plugins
        initialize_module_plugins(self, self.app)

    def register_plugin(self, plugin: BasePlugin):
        self.plugins.append(plugin)
        plugin.register(self.app)

    def use_middleware(self, middleware_cls: Type[Middleware], *args: Any, **kwargs: Any) -> None:
        middleware_instance = middleware_cls(*args, **kwargs)
        self.middlewares.append(middleware_instance)
        self.app.use_middleware(lambda: middleware_instance)

    def before_request(self, hook: Callable) -> None:
        self.hooks.add_before_request(hook)
        self.app.before_request(hook)

    def after_request(self, hook: Callable) -> None:
        self.hooks.add_after_request(hook)
        self.app.after_request(hook)

    def teardown_request(self, hook: Callable) -> None:
        self.hooks.add_teardown_request(hook)
        self.app.teardown_request(hook)

    def before_first_request(self, hook: Callable) -> None:
        self.hooks.add_before_first_request(hook)
        self.app.before_first_request(hook)

    def register_routes(self, register_func: Callable[..., None], orm: ORMInterface = None) -> None:
        if orm:
            try:
                register_func(self.app, orm)
            except TypeError:
                register_func(self.app)
        else:
            register_func(self.app)
