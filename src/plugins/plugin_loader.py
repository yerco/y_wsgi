import importlib
import os

from inspect import isabstract, isclass

from src.plugins.base_plugin import BasePlugin


def initialize_module_plugins(module, app) -> None:
    plugin_directory = os.path.join(module.directory, 'plugins')

    if os.path.exists(plugin_directory) and os.path.isdir(plugin_directory):
        for file_name in os.listdir(plugin_directory):
            if file_name.endswith(".py") and file_name not in ["base_plugin.py", "__init__.py"]:
                module_name = file_name[:-3]
                relative_path = os.path.relpath(plugin_directory, os.getcwd()).replace(os.sep, ".")
                full_module_name = f"{relative_path}.{module_name}"

                # Import the module
                plugin_module = importlib.import_module(full_module_name)

                # Iterate through module attributes and find plugin classes
                for attr_name in dir(plugin_module):
                    plugin_class = getattr(plugin_module, attr_name, None)
                    # Check if it is a class, is subclass of BasePlugin, and not abstract
                    if isclass(plugin_class) and issubclass(plugin_class, BasePlugin) and not isabstract(plugin_class):
                        plugin_instance = plugin_class()
                        module.register_plugin(plugin_instance)
