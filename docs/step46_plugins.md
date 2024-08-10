# Plugins
The plugin system allows developers to extend or modify the framework’s functionality without altering 
the core codebase. This is particularly beneficial in a modular architecture, where third-party 
extensions or custom modules can be easily added.

At `src/plugins/base_plugin.py`, we define a base class for all plugins.
```python
class BasePlugin(ABC):
    @abstractmethod
    def register(self, app: App):
        """Method to register the plugin with the application context."""
        pass
```
The `register` method receives an instance of the `App` class. Although passing the `App` object is “heavier”
than passing an `AppContext`, it provides more flexibility to the plugins. By passing the `App` object, plugins
can add routes, register middleware, or interact with hooks. 
If the goal were to restrict plugins to configuration-related tasks or lightweight operations, passing 
an `AppContext` might be more appropriate.

To manage and load these plugins, we’ve also introduced a plugin loader in `src/plugins/plugin_loader.py`. 
This loader dynamically discovers and initializes plugins within each module, ensuring they are correctly 
integrated into the application.