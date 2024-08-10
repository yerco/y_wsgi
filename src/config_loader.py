import importlib
import sys

from src.config import config as default_config


class BaseConfig:
    def __init__(self):
        self.TEMPLATE_ENGINE = None
    pass


def load_config(app_name: str = 'default', base_dir: str = None) -> BaseConfig:
    # Load default config
    # Load default config as attributes in the BaseConfig class
    config = BaseConfig()
    for attr in dir(default_config):
        if not callable(getattr(default_config, attr)) and not attr.startswith("__"):
            setattr(config, attr, getattr(default_config, attr))

    # Load user-defined configurations from the specific app
    if app_name != 'default' and base_dir:
        try:
            user_config_app = importlib.import_module(f'{app_name}.config')
            for attr in dir(user_config_app.config):
                if not callable(getattr(user_config_app.config, attr)) and not attr.startswith("__"):
                    setattr(config, attr, getattr(user_config_app.config, attr))
            setattr(config, 'APP_NAME', app_name)
            setattr(config, 'BASE_DIR', base_dir)
        except ModuleNotFoundError as e:
            print(f"Module '{app_name}.config' not found for app '{app_name}'.")
            print(f"sys.path: {sys.path}")
            print(e)
            pass  # No user-defined configuration found for this app

    return config
