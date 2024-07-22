import os
import importlib
import types  # Import types to use ModuleType
import sys

from typing import Any, Dict

from src.config import config as default_config


def load_config(app_name: str = 'default', base_dir: str = None) -> Dict[str, Any]:
    # Load default config
    config = {attr: getattr(default_config, attr) for attr in dir(default_config) if
              not callable(getattr(default_config, attr)) and not attr.startswith("__")}

    # Load user-defined configurations from the specific app
    if app_name != 'default' and base_dir:
        try:
            user_config_app = importlib.import_module(f'{app_name}.config')
            user_config = {attr: getattr(user_config_app.config, attr) for attr in dir(user_config_app.config) if
                           not callable(getattr(user_config_app.config, attr)) and not attr.startswith("__")}
            config.update(user_config)  # Merge configs, user config overrides default config
            config['APP_NAME'] = app_name
            config['BASE_DIR'] = base_dir
        except ModuleNotFoundError as e:
            print(f"Module '{app_name}.config' not found for app '{app_name}'.")
            print(f"sys.path: {sys.path}")
            print(e)
            pass  # No user-defined configuration found for this app

    return config


# Load and print merged configuration for demonstration
if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')  # Adjust path for testing
    merged_config = load_config('dummy_app', base_dir=base_dir)
    # Filter and print only the configuration settings
    filtered_config = {k: v for k, v in merged_config.items() if
                       not k.startswith('__') and not callable(v) and not isinstance(v, types.ModuleType)}
    print(filtered_config)
