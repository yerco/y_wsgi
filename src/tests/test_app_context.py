import pytest
import threading

from typing import Any, Dict, Optional

from src.app import App
from src.core.app_context import AppContext
from src.app_registry import AppRegistry


@pytest.fixture
def app_context() -> AppContext:
    return AppContext()


@pytest.fixture
def app_instance() -> App:
    template_engine = None
    return App(name='test_app', template_engine=template_engine)


def test_set_and_get_context(app_context, app_instance):
    config = {'DEBUG': 'True'}
    app_context.set_context('test_app', base_dir='.', config=config, app_instance=app_instance)

    full_context = app_context.get_full_context('test_app')
    assert full_context is not None
    assert full_context['app_name'] == 'test_app'
    assert full_context['base_dir'] == '.'
    assert full_context['config'] == config
    assert full_context['app_instance'] == app_instance

    config_context = app_context.get_config('test_app')
    assert config_context == config


def test_set_and_get_current_app_name(app_context):
    app_context.set_current_app_name('test_app')
    assert app_context.get_current_app_name() == 'test_app'

    app_context.reset_current_app_name()
    assert app_context.get_current_app_name() is None


def test_get_app_instance(app_context, app_instance):
    app_context.set_context('test_app', base_dir='.', app_instance=app_instance)

    retrieved_instance = app_context.get_app_instance('test_app')
    assert retrieved_instance == app_instance


def test_render_template(app_context, app_instance, monkeypatch):
    app_context.set_context('test_app', base_dir='.', app_instance=app_instance)

    # Define a mock render_template method
    def mock_render_template(template_name: str, context: Dict[str, Any]) -> str:
        return '<html>Test</html>'

    # Use monkeypatch to replace the render_template method with the mock
    monkeypatch.setattr(app_instance, 'render_template', mock_render_template)

    rendered_html = app_context.render_template('test_app', 'test_template.html',
                                                {'key': 'value'})
    assert rendered_html == '<html>Test</html>'


def test_render_template_app_not_found(app_context):
    with pytest.raises(ValueError) as excinfo:
        app_context.render_template('NonExistentApp', 'test_template.html',
                                    {'key': 'value'})
    assert str(excinfo.value) == "App instance for NonExistentApp not found."


def test_thread_local_storage(app_context):
    # Set context for two different apps
    app_context.set_context('app1', base_dir='/path/to/app1', config={'DEBUG': 'True'})
    app_context.set_context('app2', base_dir='/path/to/app2', config={'DEBUG': 'False'})

    # Set and get current app name in the main thread
    app_context.set_current_app_name('app1')
    assert app_context.get_current_app_name() == 'app1'

    # Simulate a new thread with a different current app name
    def new_thread():
        app_context.set_current_app_name('app2')
        assert app_context.get_current_app_name() == 'app2'
        assert app_context.get_config() == {'DEBUG': 'False'}

    import threading
    new_thread = threading.Thread(target=new_thread)
    new_thread.start()
    new_thread.join()

    # Ensure the main thread's current app name remains unchanged
    assert app_context.get_current_app_name() == 'app1'
    assert app_context.get_config() == {'DEBUG': 'True'}

    # Reset the current app name in the main thread
    app_context.reset_current_app_name()
    assert app_context.get_current_app_name() is None
    assert app_context.get_config() is None


def handle_request(request_id, app_registry):
    app_registry.create_app(f"app{request_id}")
    app = app_registry.get_app(f"app{request_id}")
    if app:
        return app.get_context().get_current_app_name(), app.get_context().get_config()


def test_concurrent_requests(monkeypatch):
    app_registry = AppRegistry()

    # Simulating concurrent requests
    results = []
    threads = []

    def mock_get_app_base_dir(self, name):
        return "/fake/path"

    monkeypatch.setattr(AppRegistry, '_get_app_base_dir', mock_get_app_base_dir)

    for i in range(3):
        t = threading.Thread(target=lambda q, arg1: q.append(handle_request(arg1, app_registry)), args=(results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected_app_names = {f"app{i}" for i in range(3)}

    # Ensure that we have the correct number of results
    assert len(results) == 3

    # Ensure that each request got the correct app name and config
    for result in results:
        app_name, config = result
        assert app_name in expected_app_names
        assert config is not None
        expected_app_names.remove(app_name)
