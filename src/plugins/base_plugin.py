from abc import ABC, abstractmethod


class BasePlugin(ABC):
    @abstractmethod
    def register(self, app):
        """Method to register the plugin with the application context."""
        pass
