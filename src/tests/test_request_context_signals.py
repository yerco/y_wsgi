import pytest
from src.core.request_context import RequestContext
from src.core.request import Request
from src.core.app_context import AppContext
from src.core.response import Response
from src.signals.signal_manager import SignalManager


@pytest.fixture
def signal_manager():
    return SignalManager()


def test_request_signals(signal_manager):
    started_emitted = False
    finished_emitted = False

    def on_request_started(request_context):
        nonlocal started_emitted
        started_emitted = True

    def on_request_finished(request_context, response):
        nonlocal finished_emitted
        finished_emitted = True

    signal_manager.connect('request_started', on_request_started)
    signal_manager.connect('request_finished', on_request_finished)

    # Simulate a request
    request = Request(environ={})
    app_context = AppContext()
    request_context = RequestContext(request, app_context)

    # Explicitly emit the signal
    signal_manager.emit('request_started', request_context=request_context)
    assert started_emitted, "Request started signal was not emitted"

    # Explicitly emit the signal for request finished
    response = Response()
    signal_manager.emit('request_finished', request_context=request_context, response=response)
    assert finished_emitted, "Request finished signal was not emitted"
