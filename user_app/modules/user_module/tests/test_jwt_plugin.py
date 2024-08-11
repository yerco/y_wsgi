import pytest
import jwt
import datetime
from unittest.mock import MagicMock

from src.core.app_context import AppContext
from user_app.modules.user_module.middleware.jwt_auth_middleware import JWTAuthMiddleware
from src.core.request import Request
from src.core.request_context import RequestContext
from src.core.response import Response
from src.app import App
from user_app.modules.user_module.plugins.jwt_demo_plugin import JWTDemoPlugin

SECRET_KEY = "user-app-secret-key"  # same as in config.py


@pytest.fixture
def app():
    app_instance = App(name='TestApp')
    app_context = AppContext()
    app_instance.set_context(app_context)
    plugin = JWTDemoPlugin()
    plugin.register(app_instance)
    return app_instance


@pytest.fixture
def valid_token():
    return jwt.encode({
        'user': 'testuser',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")


@pytest.fixture
def expired_token():
    return jwt.encode({
        'user': 'testuser',
        'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=5)
    }, SECRET_KEY, algorithm="HS256")


def test_missing_token(app):
    jwt_middleware = JWTAuthMiddleware()
    request = MagicMock(spec=Request)
    request.headers = {}
    request_context = RequestContext(request, None)

    response = jwt_middleware.before_request(request_context)
    assert isinstance(response, Response)
    assert response.status == "401 Unauthorized"
    assert response.body == [b"Authorization token is missing"]


def test_invalid_token(app):
    jwt_middleware = JWTAuthMiddleware()
    request = MagicMock(spec=Request)
    request.headers = {'authorization': 'Bearer invalid_token'}
    request_context = RequestContext(request, None)

    response = jwt_middleware.before_request(request_context)
    assert isinstance(response, Response)
    assert response.status == "401 Unauthorized"
    assert response.body == [b"Invalid token"]


def test_expired_token(app, expired_token):
    jwt_middleware = JWTAuthMiddleware()
    request = MagicMock(spec=Request)
    request.headers = {'authorization': f'Bearer {expired_token}'}
    request_context = RequestContext(request, None)

    response = jwt_middleware.before_request(request_context)
    assert isinstance(response, Response)
    assert response.status == "401 Unauthorized"
    assert response.body == [b"Token has expired"]


def test_valid_token(app, valid_token):
    jwt_middleware = JWTAuthMiddleware()
    request = MagicMock(spec=Request)
    request.headers = {'authorization': f'Bearer {valid_token}'}
    request_context = RequestContext(request, None)

    response = jwt_middleware.before_request(request_context)
    assert response is None  # Middleware should return None if everything is okay
    assert request_context.user == 'testuser'


def test_jwt_demo_route_without_token(app):
    request = MagicMock(spec=Request)
    request.headers = {}
    request.method = 'GET'
    request.path = '/jwt-demo'
    request_context = RequestContext(request, None)

    response = app.router.match('/jwt-demo', 'GET')[0](request_context)
    assert isinstance(response, Response)
    assert response.status == "401 Unauthorized"
    assert response.body == [b"Authorization token is missing"]


def test_jwt_demo_route_with_valid_token(app, valid_token):
    request = MagicMock(spec=Request)
    request.headers = {'authorization': f'Bearer {valid_token}'}
    request.method = 'GET'
    request.path = '/jwt-demo'
    request_context = RequestContext(request, None)

    response = app.router.match('/jwt-demo', 'GET')[0](request_context)
    assert isinstance(response, Response)
    assert response.status == "200 OK"
    assert response.body == [b"This is protected content. You have a valid JWT!"]
