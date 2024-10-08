from src.app_registry import AppRegistry
from user_app.modules.user_module.repositories.repository import UserRepository
from src.database.orm_initializer import initialize_orm
from src.middleware.authentication_middleware import AuthenticationMiddleware
from src.middleware.session_middleware import SessionMiddleware
from src.middleware.csrf_middleware import CSRFMiddleware
from src.middleware.static_middleware import StaticMiddleware
from src.middleware.xss_protection_middleware import XSSProtectionMiddleware
from src.middleware.cors_middleware import CORSMiddleware
from src.signals.signal_manager import SignalManager
from src.middleware.response_time_middleware import ResponseTimeMiddleware

from user_app.modules.user_module.hooks import some_hooks
from user_app.modules.user_module.views import hello_views, user_views, another_view
from user_app.modules.user_module.models.models import User
from user_app.config import config

# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('user_app')

signal_manager = SignalManager()

# Initialize the ORM adapter
orm = initialize_orm([User])

# Create user module
user_mod = app_registry.create_module('user_module', app)

# Register user module middlewares, order matters!
user_mod.use_middleware(ResponseTimeMiddleware, signal_manager)  # TODO change second argument must be signal_manager
user_mod.use_middleware(CORSMiddleware, config)
user_mod.use_middleware(XSSProtectionMiddleware)
user_mod.use_middleware(StaticMiddleware)
# Apply SessionMiddleware
user_mod.use_middleware(SessionMiddleware, config)
# Apply CSRFMiddleware (it works together with SessionMiddleware)
# user_mod.use_middleware(CSRFMiddleware, config)
# Apply AuthenticationMiddleware after SessionMiddleware
user_mod.use_middleware(AuthenticationMiddleware, config)


# # Register user module hooks
# user_mod.before_request(some_hooks.before_request_hook)
# user_mod.after_request(some_hooks.after_request_hook)
# user_mod.teardown_request(some_hooks.teardown_request_hook)
# user_mod.before_first_request(some_hooks.before_first_request_hook)

# Register routes
user_mod.register_routes(user_views.register_routes, orm)
user_mod.register_routes(hello_views.register_routes)
user_mod.register_routes(another_view.register_routes)
