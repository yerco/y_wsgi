from src.app import App
from src.core.request import Request
from src.core.response import Response


def test_before_request_hook():
    app = App()

    def before_request_hook():
        app.hooks.called_before_request = True

    app.before_request(before_request_hook)

    assert len(app.hooks.before_request_hooks) == 1
    assert app.hooks.before_request_hooks[0] == before_request_hook

    app._apply_before_request_middlewares_and_hooks(Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'}))
    assert app.hooks.called_before_request


def test_after_request_hook():
    app = App()

    def after_request_hook():
        app.hooks.called_after_request = True

    app.after_request(after_request_hook)

    assert len(app.hooks.after_request_hooks) == 1
    assert app.hooks.after_request_hooks[0] == after_request_hook

    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'})
    response = Response(status='200 OK', body=[b'Test'])

    app._apply_after_request_middlewares_and_hooks(request, response)
    assert app.hooks.called_after_request


def test_teardown_request_hook():
    app = App()

    def teardown_request_hook():
        app.hooks.called_teardown_request = True

    app.teardown_request(teardown_request_hook)

    assert len(app.hooks.teardown_request_hooks) == 1
    assert app.hooks.teardown_request_hooks[0] == teardown_request_hook

    app._apply_teardown_request_hooks(Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'}))
    assert app.hooks.called_teardown_request


def test_before_first_request_hook():
    app = App()

    def before_first_request_hook():
        app.hooks.called_before_first_request = True

    app.before_first_request(before_first_request_hook)

    assert len(app.hooks.before_first_request_hooks) == 1
    assert app.hooks.before_first_request_hooks[0] == before_first_request_hook

    app._apply_before_request_middlewares_and_hooks(Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'}))
    print(app.hooks)
    assert app.hooks.before_first_request_hooks
    assert not app.hooks.first_request  # Ensure it only runs once
