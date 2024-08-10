import pytest
import time
import os
import sys

from src.app_registry import AppRegistry
from src.database.orm_initializer import initialize_orm
from src.middleware.session_middleware import SessionMiddleware
from src.tests.test_client import FrameworkTestClient
from src.tests.model_for_testing import ModelForTesting
from src.tests.views_for_testing import register_routes


@pytest.fixture
def app(monkeypatch):
    # Create and instance of AppRegistry
    app_registry = AppRegistry()
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    sys.path.insert(0, base_dir)
    # Mock the _get_app_base_dir method
    def mock_get_app_base_dir(self, name):
        return base_dir
    monkeypatch.setattr(AppRegistry, '_get_app_base_dir', mock_get_app_base_dir)
    # Create an application instance
    app = app_registry.create_app('dummy_app')
    # Initialize the ORM adapter
    orm = initialize_orm([ModelForTesting])
    # Create a test module
    test_mod = app_registry.create_module('test_module', app)
    # Register session middleware
    test_mod.use_middleware(SessionMiddleware)
    test_mod.register_routes(register_routes, orm)
    return app


@pytest.fixture
def client(app):
    return FrameworkTestClient(app)


def test_session_creation(client):
    response = client.get('/')
    assert response.status == '200 OK'
    print(f"Response headers: {response.headers}")
    cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    assert cookies, "No Set-Cookie header found"
    session_id = cookies[0][1].split('=')[1].split(';')[0]
    assert session_id, "No session ID found in Set-Cookie header"


def test_session_retrieval(client):
    response = client.get('/')
    cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    session_id = cookies[0][1].split('=')[1].split(';')[0]

    headers = {'Cookie': f'session_id={session_id}'}
    response = client.get('/', headers=headers)
    assert response.status == '200 OK'
    assert 'set-cookie' not in [header[0].lower() for header in response.headers], "Session should not be reset"


def test_session_expiry(client):
    response = client.get('/')
    cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    session_id = cookies[0][1].split('=')[1].split(';')[0]

    session_middleware = client.app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store
    session = session_store.get_session_by_id(session_id)
    session.expiry_time = time.time() - 1
    session_store.write(session)

    headers = {'Cookie': f'session_id={session.id}'}
    response = client.get('/', headers=headers)
    assert response.status == '200 OK'
    new_cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    new_session_id = new_cookies[0][1].split('=')[1].split(';')[0]
    assert new_session_id != session_id, "Expired session should be replaced with a new session"


def test_single_session_data(client):
    response = client.get('/')
    cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    assert cookies, "No Set-Cookie header found"
    session_id = cookies[0][1].split('=')[1].split(';')[0]

    headers = {'Cookie': f'session_id={session_id}'}
    session_middleware = client.app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store
    session = session_store.get_session_by_id(session_id)
    assert session is not None, "Session not found after initial creation"

    session.set('key', 'value')
    session_store.write(session)

    response = client.get('/', headers=headers)
    assert response.status == '200 OK'
    session = session_store.get_session_by_id(session_id)
    assert session is not None, "Session not found after setting data"
    assert session.get('key') == 'value', "Session data not retrieved correctly"
    assert len(session_store) == 1


def test_modifying_same_session(client):
    # Create initial session
    response1 = client.get('/')
    assert response1.status == '200 OK'
    cookies1 = [header for header in response1.headers if header[0].lower() == 'set-cookie']
    assert cookies1, "No Set-Cookie header found for initial session"
    session_id1 = cookies1[0][1].split('=')[1].split(';')[0]

    # Set session cookie for subsequent requests
    headers = {'Cookie': f'session_id={session_id1}'}

    session_middleware = client.app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store

    # Retrieve the session and set data
    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session not found after initial creation"
    session1.set('key', 'initial_value')
    session_store.write(session1)

    # Modify the session with a new request
    response2 = client.get('/', headers=headers)
    assert response2.status == '200 OK'

    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session not found after setting initial data"
    assert session1.get('key') == 'initial_value', "Initial session data not retrieved correctly"

    # Update the session data
    session1.set('key', 'updated_value')
    session_store.write(session1)

    # Verify the updated session data with another request
    response3 = client.get('/', headers=headers)
    assert response3.status == '200 OK'

    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session not found after updating data"
    assert session1.get('key') == 'updated_value', "Updated session data not retrieved correctly"
    assert len(session_store) == 1


# We are not setting cookies we make both requests without a session cookie.
def test_multiple_sessions(client):
    # Create first session
    response1 = client.get('/')
    assert response1.status == '200 OK'
    cookies1 = [header for header in response1.headers if header[0].lower() == 'set-cookie']
    assert cookies1, "No Set-Cookie header found for session 1"
    session_id1 = cookies1[0][1].split('=')[1].split(';')[0]

    # Create second session
    response2 = client.get('/')
    assert response2.status == '200 OK'
    cookies2 = [header for header in response2.headers if header[0].lower() == 'set-cookie']
    assert cookies2, "No Set-Cookie header found for session 2"
    session_id2 = cookies2[0][1].split('=')[1].split(';')[0]

    # Ensure session IDs are different
    assert session_id1 != session_id2, "Session IDs should be different for different sessions"

    session_middleware = client.app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store

    # Retrieve and set data for the first session
    headers1 = {'Cookie': f'session_id={session_id1}'}
    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session 1 not found after creation"
    session1.set('key1', 'value1')
    session_store.write(session1)

    # Retrieve and set data for the second session
    headers2 = {'Cookie': f'session_id={session_id2}'}
    session2 = session_store.get_session_by_id(session_id2)
    assert session2 is not None, "Session 2 not found after creation"
    session2.set('key2', 'value2')
    session_store.write(session2)

    # Validate data for the first session
    response1 = client.get('/', headers=headers1)
    assert response1.status == '200 OK'
    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session 1 not found after setting data"
    assert session1.get('key1') == 'value1', "Session 1 data not retrieved correctly"
    assert session1.get('key2') is None, "Session 1 should not have data from session 2"

    # Validate data for the second session
    response2 = client.get('/', headers=headers2)
    assert response2.status == '200 OK'
    session2 = session_store.get_session_by_id(session_id2)
    assert session2 is not None, "Session 2 not found after setting data"
    assert session2.get('key2') == 'value2', "Session 2 data not retrieved correctly"
    assert session2.get('key1') is None, "Session 2 should not have data from session 1"


def test_multiple_sessions_different_users(app):
    # Create two separate clients to simulate two different users
    client1 = FrameworkTestClient(app)
    client2 = FrameworkTestClient(app)

    # Simulate first user creating a session
    response1 = client1.get('/')
    assert response1.status == '200 OK'
    cookies1 = [header for header in response1.headers if header[0].lower() == 'set-cookie']
    assert cookies1, "No Set-Cookie header found for session 1"
    session_id1 = cookies1[0][1].split('=')[1].split(';')[0]

    headers1 = {'Cookie': f'session_id={session_id1}'}

    # Simulate a second user creating a different session
    response2 = client2.get('/')
    assert response2.status == '200 OK'
    cookies2 = [header for header in response2.headers if header[0].lower() == 'set-cookie']
    assert cookies2, "No Set-Cookie header found for session 2"
    session_id2 = cookies2[0][1].split('=')[1].split(';')[0]

    headers2 = {'Cookie': f'session_id={session_id2}'}

    # Ensure session IDs are different
    assert session_id1 != session_id2, "Session IDs should be different for different sessions"

    session_middleware = app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store

    # Retrieve and set data for the first session
    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session 1 not found after creation"
    session1.set('key1', 'value1')
    session_store.write(session1)

    # Retrieve and set data for the second session
    session2 = session_store.get_session_by_id(session_id2)
    assert session2 is not None, "Session 2 not found after creation"
    session2.set('key2', 'value2')
    session_store.write(session2)

    # Validate data for the first session
    response1 = client1.get('/', headers=headers1)
    assert response1.status == '200 OK'
    session1 = session_store.get_session_by_id(session_id1)
    assert session1 is not None, "Session 1 not found after setting data"
    assert session1.get('key1') == 'value1', "Session 1 data not retrieved correctly"
    assert session1.get('key2') is None, "Session 1 should not have data from session 2"

    # Validate data for the second session
    response2 = client2.get('/', headers=headers2)
    assert response2.status == '200 OK'
    session2 = session_store.get_session_by_id(session_id2)
    assert session2 is not None, "Session 2 not found after setting data"
    assert session2.get('key2') == 'value2', "Session 2 data not retrieved correctly"
    assert session2.get('key1') is None, "Session 2 should not have data from session 1"


def test_undo_redo_sessions(client):
    # Initial request to create a session
    response = client.get('/')
    assert response.status == '200 OK'
    cookies = [header for header in response.headers if header[0].lower() == 'set-cookie']
    assert cookies, "No Set-Cookie header found"
    session_id = cookies[0][1].split('=')[1].split(';')[0]

    headers = {'Cookie': f'session_id={session_id}'}

    session_middleware = client.app.middlewares[0]
    assert isinstance(session_middleware, SessionMiddleware)
    session_store = session_middleware.session_store

    # Modify session
    session = session_store.get_session_by_id(session_id)
    session.set('key', 'value1')
    session_store.write(session)
    assert session.get('key') == 'value1', "Session value not set correctly"

    # Save state (implicitly done in the store's write method)

    # Modify session again
    session.set('key', 'value2')
    session_store.write(session)
    assert session.get('key') == 'value2', "Session value not updated correctly"

    # Undo the last change
    session_store.undo()
    session = session_store.get_session_by_id(session_id)
    assert session.get('key') == 'value1', "Session value not reverted correctly"

    # Redo the last change
    session_store.redo()
    session = session_store.get_session_by_id(session_id)
    assert session.get('key') == 'value2', "Session value not restored correctly"
