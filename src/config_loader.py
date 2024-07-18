import os
import importlib
import types  # Import types to use ModuleType
import sys

from typing import Any, Dict

from src.config import config as default_config
from src.utils.app_scanner import get_user_apps


class ConfigLoader:
    _instances: Dict[str, 'ConfigLoader'] = {}

    def __new__(cls, app_name: str ='default', base_dir : str = None) -> 'ConfigLoader':
        if app_name not in cls._instances:
            cls._instances[app_name] = super(ConfigLoader, cls).__new__(cls)
            cls._instances[app_name].config = {}
            cls._instances[app_name].load_config(base_dir)
        return cls._instances[app_name]

    def __init__(self, app_name: str = 'default', base_dir: str = None):
        # Initialization logic if necessary
        if not hasattr(self, 'config'):
            self.config = {}  # Ensure config is defined

    def load_config(self, base_dir: str):
        # Load default config
        class_attributes = {attr: getattr(default_config, attr) for attr in dir(default_config) if
                            not callable(getattr(default_config, attr)) and not attr.startswith("__")}
        # print("Values:", class_attributes)
        self.config.update({k: v for k, v in class_attributes.items()})

        # Load user-defined configurations from detected apps
        user_apps = get_user_apps(base_dir=base_dir)
        for user_app_name, user_app_path in user_apps.items():
            # Temporarily add base_dir to sys.path for module importing
            original_sys_path = sys.path.copy()
            if user_app_path not in sys.path:
                sys.path.insert(0, base_dir)
            try:
                user_config = importlib.import_module(f'{user_app_name}.config',)
                temp = user_config.config
                app_class_attributes = {attr: getattr(temp, attr) for attr in dir(temp) if
                                        not callable(getattr(temp, attr)) and not attr.startswith("__")}
                self.config.update({k: v for k, v in app_class_attributes.items()})
            except ModuleNotFoundError:
                pass  # No user-defined configuration found for this app
            finally:
                sys.path = original_sys_path  # Restore original sys.path

        return self.config

    def get(self, key: str, default: Any = None):
        return self.config.get(key, default)


# Helper function to load configuration
def load_config(app_name: str = 'default', base_dir: str = None) -> Dict[str, Any]:
    loader = ConfigLoader(app_name, base_dir)
    return loader.config


# Load and print merged configuration for demonstration
if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')  # Adjust path for testing
    merged_config = load_config(base_dir=base_dir).config
    # Filter and print only the configuration settings
    filtered_config = {k: v for k, v in merged_config.items() if
                       not k.startswith('__') and not callable(v) and not isinstance(v, types.ModuleType)}
    print(filtered_config)
