import pytest
import os

from unittest.mock import patch

from src.app_registry import AppRegistry
from src.database.orm_initializer import initialize_orm
from src.middleware.authentication_middleware import AuthenticationMiddleware
from src.tests.test_client import FrameworkTestClient
from src.tests.model_for_testing import ModelForTesting
from src.tests.views_for_testing import register_routes


class Config:
    PUBLIC_ROUTES = ['/public']
    DEFAULT_USERS = [
        {"username": "admin", "password": "adminpassword", "role": "admin"},
        {"username": "user", "password": "password", "role": "user"}
    ]


@pytest.fixture
def app():
    # Create and instance of AppRegistry
    app_registry = AppRegistry()
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    test_directory = os.path.join(current_file_dir, 'apps/dummy_app')
    # Mock the _get_app_base_dir method
    with patch.object(AppRegistry, '_get_app_base_dir', return_value=test_directory):
        # Create an application instance
        app = app_registry.create_app('dummy_app')

        # Initialize the ORM adapter
        orm = initialize_orm([ModelForTesting])  # Replace with your actual models for testing
        # Create a test module
        test_mod = app_registry.create_module('module1', app)
        # Register authentication middleware with public routes
        config = Config()
        test_mod.use_middleware(AuthenticationMiddleware, config)

        test_mod.register_routes(register_routes, orm)

    return app


@pytest.fixture
def client(app):
    return FrameworkTestClient(app)


def test_public_route(client):
    response = client.get('/public')
    assert response.status == '200 OK'
    assert b'Public Content' in response.body


def test_private_route_unauthenticated(client):
    response = client.get('/private')
    assert response.status == '401 Unauthorized'
    assert b'Unauthorized' in response.body


def test_private_route_authenticated_user(client):
    headers = {
        'X-Username': 'user',
        'X-Password': 'password'
    }
    lowercase_headers = {key.lower(): value.lower() for key, value in headers.items()}
    response = client.get('/private', headers=lowercase_headers)
    assert response.status == '403 Forbidden'
    assert b'Forbidden' in response.body


def test_private_route_authenticated_admin(client):
    headers = {
        'X-Username': 'admin',
        'X-Password': 'adminpassword'
    }
    response = client.get('/private', headers=headers)
    assert response.status == '200 OK'
    assert b'Private Content' in response.body
