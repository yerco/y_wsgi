import os
import pytest
import sys

from src.app import App
from src.app_registry import AppRegistry


@pytest.fixture
def app_registry():
    registry = AppRegistry()
    return registry


def test_create_app(app_registry, monkeypatch):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(current_dir, 'apps')

    def mock_get_app_base_dir(self, name):
        return str(apps_dir)

    sys.path.insert(0, apps_dir)
    monkeypatch.setattr(AppRegistry, '_get_app_base_dir', mock_get_app_base_dir)
    app_name1 = 'dummy_app'
    app1 = app_registry.create_app(app_name1)
    app_name2 = 'another_dummy_app'
    app2 = app_registry.create_app(app_name2)

    assert len(app_registry._apps) == 2
    assert app_registry._apps[app_name1] == app1
    assert isinstance(app_registry._apps[app_name1], App)
    assert app_registry._apps[app_name2] == app2
    assert isinstance(app_registry._apps[app_name2], App)


def test_create_module(app_registry, monkeypatch):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(current_dir, 'apps')

    def mock_get_app_base_dir(self, name):
        return str(apps_dir)

    sys.path.insert(0, apps_dir)
    monkeypatch.setattr(AppRegistry, '_get_app_base_dir', mock_get_app_base_dir)
    app_name1 = 'dummy_app'
    app1 = app_registry.create_app(app_name1)
    app_name2 = 'another_dummy_app'
    app2 = app_registry.create_app(app_name2)

    app_registry.create_module('module1', app1)
    app_registry.create_module('module2', app1)
    app_registry.create_module('module3', app1)
    app_registry.create_module('module1', app2)
    app_registry.create_module('module2', app2)
    app_registry.create_module('module3', app2)

    assert len(app1.modules) == 3
    assert 'module1' in app1.modules.keys()
    assert 'module2' in app1.modules.keys()

    dummy_app = app_registry.get_app('dummy_app')
    dummy_app_context = dummy_app.get_context()
    dummy_app_config = dummy_app_context.get_config()
    assert dummy_app_config.SECRET_KEY == 'dummy-app-secret-key'

    another_dummy_app = app_registry.get_app('another_dummy_app')
    another_dummy_app_context = another_dummy_app.get_context()
    another_dummy_app_config = another_dummy_app_context.get_config()
    assert another_dummy_app_config.SECRET_KEY == 'another-dummy-app-secret-key'

    dummy_app2 = app_registry.get_app('dummy_app')
    dummy_app_context2 = dummy_app2.get_context()
    dummy_app_config2 = dummy_app_context2.get_config()
    assert dummy_app_config2.SECRET_KEY == 'dummy-app-secret-key'
