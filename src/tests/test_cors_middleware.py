import os
import pytest

from src.middleware.cors_middleware import CORSMiddleware
from src.core.request import Request
from src.core.request_context import RequestContext
from src.core.response import Response
from src.app_registry import AppRegistry


class Config:
    PUBLIC_ROUTES = ['/public']
    DEFAULT_USERS = [
        {"username": "admin", "password": "adminpassword", "role": "admin"},
        {"username": "user", "password": "password", "role": "user"}
    ]
    ALLOWED_ORIGINS = ["https://example.com", "https://anotherdomain.com"]
    ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    ALLOWED_HEADERS = ["Content-Type", "Authorization"]


@pytest.fixture
def app_registry():
    return AppRegistry()


@pytest.fixture
def app(app_registry, monkeypatch):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(current_dir, 'apps')

    def mock_get_app_base_dir(self, name):
        return str(apps_dir) + '/' + 'dummy_app'
    monkeypatch.setattr(AppRegistry, '_get_app_base_dir', mock_get_app_base_dir)
    return app_registry.create_app('dummy_app')


@pytest.fixture
def app_module(app_registry, app):
    return app_registry.create_module('module1', app)


@pytest.fixture
def request_context(app):
    request = Request({
        "REQUEST_METHOD": "OPTIONS",
        "PATH_INFO": "/",
        "HTTP_ORIGIN": "https://example.com"
    })
    return RequestContext(request, app.get_context())


def test_cors_middleware_before_request(app_module, request_context, monkeypatch):
    config = Config()
    cors_middleware = CORSMiddleware(config)
    response = cors_middleware.before_request(request_context)
    assert response is not None
    assert response.status_code == 200
    assert response.headers_dict["Access-Control-Allow-Origin"] == "https://example.com"
    assert response.headers_dict["Access-Control-Allow-Methods"] == "GET, POST, PUT, DELETE, OPTIONS"
    assert response.headers_dict["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    assert response.headers_dict["Access-Control-Allow-Credentials"] == "true"


def test_cors_middleware_after_request(app_module, request_context):
    cors_middleware = CORSMiddleware(config=Config())
    response = Response(body=b"Hello, world!")
    response = cors_middleware.after_request(request_context, response)
    assert response.headers_dict["Access-Control-Allow-Origin"] == "https://example.com"
    assert response.headers_dict["Access-Control-Allow-Methods"] == "GET, POST, PUT, DELETE, OPTIONS"
    assert response.headers_dict["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    assert response.headers_dict["Access-Control-Allow-Credentials"] == "true"


def test_cors_middleware_integration(app_registry, app, app_module):
    app_module.use_middleware(CORSMiddleware, config=Config())

    request = Request({
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "HTTP_ORIGIN": "https://example.com"
    })
    request_context = RequestContext(request, app.get_context())

    response = Response(body=b"Hello, world!")
    response = app._apply_after_request_middlewares_and_hooks(request_context, response)

    assert response.headers_dict["Access-Control-Allow-Origin"] == "https://example.com"
    assert response.headers_dict["Access-Control-Allow-Methods"] == "GET, POST, PUT, DELETE, OPTIONS"
    assert response.headers_dict["Access-Control-Allow-Headers"] == "Content-Type, Authorization"
    assert response.headers_dict["Access-Control-Allow-Credentials"] == "true"
