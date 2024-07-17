import os


class DummyAppConfig:
    # General configuration
    DEBUG = os.getenv("DUMMY_APP_DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("DUMMY_APP_SECRET_KEY", "dummy-app-secret-key")

    # Database configuration
    DATABASE_URL = os.getenv("DUMMY_APP_DATABASE_URL", "sqlite:///./dummy_app.db")

    PUBLIC_ROUTES = ["/", "/greet", "/about", "/users", "/create_user"]


config = DummyAppConfig()
