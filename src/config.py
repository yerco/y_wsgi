import os


class Config:
    # General configuration
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Framework-specific configuration


config = Config()
