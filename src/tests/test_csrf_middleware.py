import pytest
from src.core.request_context import RequestContext
from src.core.response import Response
from src.core.request import Request
from src.core.session_context import SessionContext
from src.middleware.csrf_middleware import CSRFMiddleware
from unittest.mock import MagicMock


@pytest.fixture
def csrf_middleware():
    secret_key = "test-secret-key"
    return CSRFMiddleware(secret_key=secret_key)


@pytest.fixture
def session_context():
    session_id = "session123"
    session_mock = MagicMock(id=session_id)
    return SessionContext(session=session_mock)


@pytest.fixture
def app_context():
    app_context = MagicMock()
    return app_context


@pytest.fixture
def request_context(app_context, session_context):
    environ = {'REQUEST_METHOD': 'POST'}  # Default to POST
    request = Request(environ)
    request_context = RequestContext(request=request, app_context=app_context)
    request_context.session_context = session_context  # Set the session context directly
    return request_context


@pytest.fixture
def response():
    return Response()


def test_generate_csrf_token(csrf_middleware):
    token = csrf_middleware.generate_csrf_token("session123")
    assert isinstance(token, str)
    assert token != ''


def test_before_request_valid_token(csrf_middleware, request_context):
    token = csrf_middleware.generate_csrf_token(request_context.session_context.id)
    request_context.get_form_data = MagicMock(return_value={'csrf_token': token})
    response = csrf_middleware.before_request(request_context)
    assert response is None


@pytest.mark.parametrize("method", ['POST', 'PUT', 'PATCH', 'DELETE'])
def test_before_request_invalid_token(csrf_middleware, request_context, method):
    request_context.request.environ = {'REQUEST_METHOD': method}
    request_context.get_form_data = MagicMock(return_value={'csrf_token': 'invalid_token'})
    response = csrf_middleware.before_request(request_context)
    assert isinstance(response, Response)
    assert response.body == b"Invalid CSRF Token"
    assert response._status == '403 Forbidden'


def test_after_request_adds_csrf_token(csrf_middleware, request_context, response):
    request_context.request.environ['REQUEST_METHOD'] = 'GET'
    response = csrf_middleware.after_request(request_context, response)
    headers = dict(response.headers)
    assert 'X-CSRF-Token' in headers
