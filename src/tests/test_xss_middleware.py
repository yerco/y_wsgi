import base64
import os
import pytest

from src.middleware.xss_protection_middleware import XSSProtectionMiddleware
from src.core.request_context import RequestContext
from src.core.response import Response
from src.app import App
from src.core.request import Request


@pytest.fixture
def app():
    return App(name="test_app")


@pytest.fixture
def request_context(app):
    request = Request({
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "HEADERS": {}
    })
    return RequestContext(request, app.get_context())


def test_xss_protection_middleware_before_request(request_context):
    xss_protection_middleware = XSSProtectionMiddleware()
    response = xss_protection_middleware.before_request(request_context)
    assert response is None  # No specific before_request logic needed for XSS protection
    assert 'nonce' in request_context.request.environ  # Ensure nonce is generated


def test_xss_protection_middleware_after_request(request_context):
    xss_protection_middleware = XSSProtectionMiddleware()
    nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
    request_context.request.environ['nonce'] = nonce
    response = Response(body=b"Hello, world!")
    response = xss_protection_middleware.after_request(request_context, response)

    assert response.headers_dict["X-XSS-Protection"] == "1; mode=block"
    assert response.headers_dict[
               "Content-Security-Policy"
           ] == (f"default-src 'self'; style-src 'self' 'nonce-{nonce}'; script-src 'self' "
                 f"'nonce-{nonce}'; object-src 'none';")


def test_xss_protection_middleware_integration(app, request_context):
    app.use_middleware(XSSProtectionMiddleware)

    request = Request({
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "HEADERS": {}
    })
    request_context = RequestContext(request, app.get_context())

    # Ensure before_request is called to generate nonce
    app._apply_before_request_middlewares_and_hooks(request_context)
    nonce = request_context.request.environ['nonce']

    response = Response(body=b"Hello, world!")
    response = app._apply_after_request_middlewares_and_hooks(request_context, response)

    assert response.headers_dict["X-XSS-Protection"] == "1; mode=block"
    assert response.headers_dict[
               "Content-Security-Policy"
           ] == (f"default-src 'self'; style-src 'self' 'nonce-{nonce}'; script-src 'self' 'nonce-{nonce}'; "
                 f"object-src 'none';")
