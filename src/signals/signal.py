from typing import Callable, List, Dict


class Signal:
    def __init__(self):
        self._handlers: List[Callable] = []

    def connect(self, handler: Callable) -> None:
        """Connect a handler to the signal."""
        self._handlers.append(handler)

    def disconnect(self, handler: Callable) -> None:
        """Disconnect a handler from the signal."""
        if handler in self._handlers:
            self._handlers.remove(handler)

    def emit(self, **kwargs) -> None:
        """Emit the signal, calling all connected handlers."""
        for handler in self._handlers:
            handler(**kwargs)
