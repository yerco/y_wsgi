import pytest
from src.core.app_context import AppContext
from src.app import App
from typing import Any, Dict, Optional


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

    context = app_context.get_config('test_app')
    assert context is not None
    assert context['app_name'] == 'test_app'
    assert context['base_dir'] == '.'
    assert context['config'] == config
    assert context['app_instance'] == app_instance


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
