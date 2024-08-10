import os


class UserAppConfig:
    # General configuration
    DEBUG = os.getenv("USER_APP_DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("USER_APP_SECRET_KEY", "user-app-secret-key")

    # Database configuration
    DATABASE_URL = os.getenv("USER_APP_DATABASE_URL", "sqlite:///./user_app.db")

    PUBLIC_ROUTES = ["/", "/greet", "/greet/[^/]+", "/about", "/users", "/create_user",
                     r"/user/\d+", "/filter_users/[^/]+", "/user_app_page", "/jinja2",
                     "/register", "/register/admin", "/register/user", "/json", "/start_background_task",
                     "/wait_for_tasks", "/another", "/example-as-view", "/proxy-example", "/demo-plugin"]

    # Jinja2 configuration
    TEMPLATE_ENGINE = "jinja2"

    ALLOWED_ORIGINS = ["*"]
    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS = [""]

    # Default users for testing
    DEFAULT_USERS = [
        {"username": "john", "password": "password", "role": "user"}
    ]


config = UserAppConfig()
