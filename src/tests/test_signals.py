from src.signals.signal import Signal


def test_signal_connect_and_emit():
    test_signal = Signal()
    results = []

    def handler(**kwargs):
        results.append(kwargs)

    test_signal.connect(handler)
    test_signal.emit(data="test")

    assert results == [{'data': 'test'}], "Handler should be called with the emitted data"


def test_signal_disconnect():
    test_signal = Signal()
    results = []

    def handler(**kwargs):
        results.append(kwargs)

    test_signal.connect(handler)
    test_signal.disconnect(handler)
    test_signal.emit(data="test")

    assert results == [], "Handler should not be called after disconnection"


def test_signal_multiple_handlers():
    test_signal = Signal()
    results = []

    def handler1(**kwargs):
        results.append('handler1')

    def handler2(**kwargs):
        results.append('handler2')

    test_signal.connect(handler1)
    test_signal.connect(handler2)
    test_signal.emit()

    assert results == ['handler1', 'handler2'], "All connected handlers should be called"
