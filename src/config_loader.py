import os
import importlib
import types  # Import types to use ModuleType
import sys

from src.config import config as default_config
from src.utils.app_scanner import get_user_apps


class ConfigLoader:
    _instances = {}

    def __new__(cls, app_name='default', base_dir=None):
        if app_name not in cls._instances:
            cls._instances[app_name] = super(ConfigLoader, cls).__new__(cls)
            cls._instances[app_name].config = cls._instances[app_name].load_config(base_dir)
        return cls._instances[app_name]

    def load_config(self, base_dir):
        self.config = {}

        # Load default config
        class_attributes = {attr: getattr(default_config, attr) for attr in dir(default_config) if
                            not callable(getattr(default_config, attr)) and not attr.startswith("__")}
        # print("Values:", class_attributes)
        self.config.update({k: v for k, v in class_attributes.items()})

        # Load user-defined configurations from detected apps
        user_apps = get_user_apps(base_dir=base_dir)
        for app_name in user_apps:
            # Temporarily add base_dir to sys.path for module importing
            original_sys_path = sys.path.copy()
            if base_dir and base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            try:
                user_config = importlib.import_module(f'{app_name}.config',)
                temp = user_config.config
                app_class_attributes = {attr: getattr(temp, attr) for attr in dir(temp) if
                                        not callable(getattr(temp, attr)) and not attr.startswith("__")}
                self.config.update({k: v for k, v in app_class_attributes.items()})
            except ModuleNotFoundError:
                pass  # No user-defined configuration found for this app
            finally:
                sys.path = original_sys_path  # Restore original sys.path

        return self.config

    def get(self, key, default=None):
        return self.config.get(key, default)


# Helper function to load configuration
def load_config(app_name='default', base_dir=None):
    return ConfigLoader(app_name, base_dir)


# Load and print merged configuration for demonstration
if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')  # Adjust path for testing
    merged_config = load_config(base_dir=base_dir).config
    # Filter and print only the configuration settings
    filtered_config = {k: v for k, v in merged_config.items() if
                       not k.startswith('__') and not callable(v) and not isinstance(v, types.ModuleType)}
    print(filtered_config)
