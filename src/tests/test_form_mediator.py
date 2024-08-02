import pytest

from src.core.session_context import SessionContext
from src.forms.form_mediator import FormMediator
from src.middleware.csrf_token import CSRFToken
from src.forms.form import BaseForm
from src.core.request_context import RequestContext
from src.core.request import Request
from src.core.app_context import AppContext


class DummyForm(BaseForm):
    def __init__(self, data, request_context):
        super().__init__(data, request_context)
        csrf = CSRFToken("test_secret")
        csrf_token = csrf.generate_csrf_token("test_session_id")
        self.request_context.session_context.csrf_token = csrf_token
        self.csrf_token = "test_csrf_token"


@pytest.fixture
def form_mediator():
    return FormMediator()


@pytest.fixture
def csrf_token():
    return CSRFToken(secret_key="test_secret")


@pytest.fixture
def _request():  # otherwise Failed: 'request' is a reserved word for fixtures, use another name:
    return Request(environ={})


@pytest.fixture
def app_context():
    return AppContext()


@pytest.fixture
def session_context():
    session_context = SessionContext()
    session_context.csrf_token = "test_csrf_token"
    return SessionContext()


@pytest.fixture
def request_context(_request, app_context, session_context):
    request_context = RequestContext(_request, app_context)
    request_context.session_context = session_context
    return request_context


@pytest.fixture
def dummy_form(request_context):
    return DummyForm(data={}, request_context=request_context)


def test_register_form(form_mediator, dummy_form):
    dummy_form.csrf_token = "test_csrf_token"
    form_mediator.register_form(dummy_form)
    assert id(dummy_form) in form_mediator.forms


def test_set_csrf_token(form_mediator, csrf_token):
    session_id = "test_session_id"
    form_mediator.set_csrf_token(csrf_token, session_id)
    assert form_mediator.csrf_token == csrf_token
    assert form_mediator.session_id == session_id


def test_notify_csrf_check(form_mediator, dummy_form, csrf_token):
    session_id = "test_session_id"
    form_mediator.set_csrf_token(csrf_token.generate_csrf_token(session_id), session_id)

    # Set the CSRF token for the form
    form_mediator.register_form(dummy_form)
    form_mediator.notify(dummy_form, 'set_csrf')

    # Test valid CSRF token
    dummy_form.csrf_token = csrf_token.generate_csrf_token(session_id)
    form_mediator.notify(dummy_form, 'csrf_check')
    assert not dummy_form.errors

    # Test invalid CSRF token
    dummy_form.csrf_token = "invalid_token"
    form_mediator.notify(dummy_form, 'csrf_check')
    assert 'csrf_token' in dummy_form.errors
    assert dummy_form.errors['csrf_token'] == "Invalid CSRF token"
