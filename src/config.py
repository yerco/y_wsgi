import os


class Config:
    # General configuration
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Authentication configuration
    MAX_FAILED_ATTEMPTS = int(os.getenv("MAX_FAILED_ATTEMPTS", 3))

    # Default users for testing
    DEFAULT_USERS = [
        {"username": "admin", "password": "adminpassword", "role": "admin"},
        {"username": "user", "password": "password", "role": "user"}
    ]

    # Framework-specific configuration


config = Config()
