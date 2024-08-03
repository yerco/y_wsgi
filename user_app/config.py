import os


class UserAppConfig:
    # General configuration
    DEBUG = os.getenv("USER_APP_DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("USER_APP_SECRET_KEY", "user-app-secret-key")

    # Database configuration
    DATABASE_URL = os.getenv("USER_APP_DATABASE_URL", "sqlite:///./user_app.db")

    PUBLIC_ROUTES = ["/", "/greet", "/greet/[^/]+", "/about", "/users", "/create_user",
                     r"/user/\d+", "/filter_users/[^/]+", "/user_app_page", "/jinja2",
                     "/register", "/register/admin", "/register/user"]  # "/json" removed

    # Jinja2 configuration
    TEMPLATE_ENGINE = "jinja2"

    ALLOWED_ORIGINS = ["*"]
    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS = [""]


config = UserAppConfig()
