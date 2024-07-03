import os


class Config:
    # General configuration
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # Database configuration
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./test.db")


config = Config()
