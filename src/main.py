from src.app import App
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.authentication_middleware import AuthenticationMiddleware
from src.hooks import some_hooks
from src.views import user_views, hello_views
from src.database.orm import ORM
from src.database.models import User
from src.database.factory import UserFactory
from src.database.repository import UserRepository

app = App()

# Register Middlewares
app.use_middleware(LoggingMiddleware)
app.use_middleware(AuthenticationMiddleware)

# Register hooks
app.before_request(some_hooks.before_request_hook)
app.after_request(some_hooks.after_request_hook)
app.teardown_request(some_hooks.teardown_request_hook)
app.before_first_request(some_hooks.before_first_request_hook)

# Register routes
user_views.register_routes(app)
hello_views.register_routes(app)

# Set up ORM and repositories
orm = ORM()
orm.register(User)

# Using the repository
user_repo = UserRepository(orm)

# Create a user using the factory and add it via the repository
user = UserFactory.create_user('john_doe', 'password123')
user_repo.add(user)

# Fetch and print the user
retrieved_user = user_repo.get_by_username('john_doe')
print(retrieved_user)

# Directly using ORM to create a user (not the repository)
orm.create('user', username='jane_doe', password='password123')

# Fetch and print all users
users = orm.all('user')
print(users)
