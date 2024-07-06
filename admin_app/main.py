from src.app_registry import AppRegistry
from admin_app.modules.admin_main_module.middleware.logging_middleware import LoggingMiddleware
from admin_app.modules.admin_main_module.views import admin_main_views

# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('admin_app')

# Create user module
admin_main_mod = app_registry.create_module('admin_main_module', app)

# Register admin_main_module middlewares
admin_main_mod.use_middleware(LoggingMiddleware)

admin_main_mod.register_routes(admin_main_views.register_routes)

