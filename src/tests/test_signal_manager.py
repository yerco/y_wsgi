import pytest
from src.signals.signal_manager import SignalManager


@pytest.fixture
def signal_manager():
    return SignalManager()


def test_signal_manager_connect_and_emit(signal_manager):
    emitted = False

    def test_handler(**kwargs):
        nonlocal emitted
        emitted = True

    signal_manager.connect('test_signal', test_handler)
    signal_manager.emit('test_signal')

    assert emitted, "Signal was not emitted or handler did not run"


def test_signal_manager_disconnect(signal_manager):
    emitted = False

    def test_handler(**kwargs):
        nonlocal emitted
        emitted = True

    signal_manager.connect('test_signal', test_handler)
    signal_manager.disconnect('test_signal', test_handler)
    signal_manager.emit('test_signal')

    assert not emitted, "Handler should have been disconnected and not run"
