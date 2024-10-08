import os


class Config:
    # General configuration
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    # Authentication configuration
    MAX_FAILED_ATTEMPTS = int(os.getenv("MAX_FAILED_ATTEMPTS", 3))

    # Default users for testing
    DEFAULT_USERS = [
        {"username": "admin", "password": "adminpassword", "role": "admin"},
        {"username": "user", "password": "password", "role": "user"}
    ]

    SESSION_EXPIRY = 3600  # Session expiry time in seconds (e.g., 1 hour)
    SESSION_ID_ROTATION_INTERVAL = 1800  # Session ID rotation interval in seconds (e.g., 30 minutes)
    # Framework-specific configuration

    # Define the allowed origins, methods, and headers
    ALLOWED_ORIGINS = ["https://example.com", "https://anotherdomain.com"]
    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS = ["Content-Type", "Authorization"]

    TEMPLATE_ENGINE = "jinja2"


config = Config()
