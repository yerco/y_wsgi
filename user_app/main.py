from src.app_registry import AppRegistry
from user_app.modules.user_module.repositories.repository import UserRepository
from src.database.orm_initializer import initialize_orm
from src.middleware.authentication_middleware import AuthenticationMiddleware
from src.middleware.session_middleware import SessionMiddleware
from src.middleware.csrf_middleware import CSRFMiddleware
from src.middleware.static_middleware import StaticMiddleware
from src.middleware.xss_protection_middleware import XSSProtectionMiddleware
from src.middleware.cors_middleware import CORSMiddleware

from user_app.modules.user_module.middleware.logging_middleware import LoggingMiddleware
# from user_app.modules.user_module.middleware.authentication_middleware import AuthenticationMiddleware
from user_app.modules.user_module.hooks import some_hooks
from user_app.modules.user_module.views import hello_views, user_views
from user_app.modules.user_module.models.models import User
from user_app.config import config

# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('user_app')

# Initialize the ORM adapter
orm = initialize_orm([User])

# Create user module
user_mod = app_registry.create_module('user_module', app)

# Register user module middlewares, order matters!
user_mod.use_middleware(CORSMiddleware, allowed_origins=config.ALLOWED_ORIGINS, allowed_methods=config.ALLOWED_METHODS,
                        allowed_headers=config.ALLOWED_HEADERS)
# user_mod.use_middleware(XSSProtectionMiddleware)
user_mod.use_middleware(StaticMiddleware)
# Apply SessionMiddleware
user_mod.use_middleware(SessionMiddleware)
# Apply CSRFMiddleware after SessionMiddleware and before AuthenticationMiddleware
user_mod.use_middleware(CSRFMiddleware, secret_key=config.SECRET_KEY)
# Apply AuthenticationMiddleware after SessionMiddleware
user_mod.use_middleware(AuthenticationMiddleware, public_routes=config.PUBLIC_ROUTES)


# # Register user module hooks
# user_mod.before_request(some_hooks.before_request_hook)
# user_mod.after_request(some_hooks.after_request_hook)
# user_mod.teardown_request(some_hooks.teardown_request_hook)
# user_mod.before_first_request(some_hooks.before_first_request_hook)

# Register routes
user_mod.register_routes(user_views.register_routes, orm)
user_mod.register_routes(hello_views.register_routes)

# # Example usage
# user_repo = UserRepository(orm)
# user_repo.add(User(username='johnny_marx', password='123password'))
#
# # Create a user using the factory and add it via the repository
# user = orm.create(User, username='john_doe', password='password123')
# print(user)
# user = orm.create(User, username='jane_doe', password='password123')
# print(user)
#
# users = orm.all(User)
# print("All of them:\n", users)
