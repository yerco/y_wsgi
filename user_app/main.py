from src.app_registry import AppRegistry
from src.database.repository import UserRepository
from src.database.orm_initializer import initialize_orm

from user_app.middleware.logging_middleware import LoggingMiddleware
from user_app.middleware.authentication_middleware import AuthenticationMiddleware
from user_app.hooks import some_hooks
from user_app.views import user_views, hello_views
from user_app.models.models import User


# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('user_app')

# Register Middlewares
app.use_middleware(LoggingMiddleware)
app.use_middleware(AuthenticationMiddleware)

# Register hooks
app.before_request(some_hooks.before_request_hook)
app.after_request(some_hooks.after_request_hook)
app.teardown_request(some_hooks.teardown_request_hook)
app.before_first_request(some_hooks.before_first_request_hook)

# Initialize the ORM adapter
orm = initialize_orm([User])

# Register model (example)
orm.register(User)

# Register routes
user_views.register_routes(app, orm)
hello_views.register_routes(app)

# Example usage
user_repo = UserRepository(orm)

# Create a user using the factory and add it via the repository
user = orm.create(User, username='john_doe', password='password123')
print(user)
user = orm.create(User, username='jane_doe', password='password123')
print(user)

users = orm.all(User)
print("All of them:\n", users)
