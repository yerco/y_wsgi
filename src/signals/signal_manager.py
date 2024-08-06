from typing import Callable

from src.signals.signal import Signal


class SignalManager:
    def __init__(self):
        self.signals = {}

    def get_signal(self, name: str) -> Signal:
        if name not in self.signals:
            self.signals[name] = Signal()
        return self.signals[name]

    def connect(self, name: str, handler: Callable) -> None:
        """Connect a handler to a named signal."""
        signal = self.get_signal(name)
        signal.connect(handler)

    def disconnect(self, name: str, handler: Callable) -> None:
        """Disconnect a handler from a named signal."""
        if name in self.signals:
            self.signals[name].disconnect(handler)

    def emit(self, name: str, **kwargs) -> None:
        """Emit a named signal."""
        if name in self.signals:
            self.signals[name].emit(**kwargs)
