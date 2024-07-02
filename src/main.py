from src.app import App
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.authentication_middleware import AuthenticationMiddleware
from src.hooks import some_hooks
from src.views import user_views, hello_views

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
