import pytest
from typing import Dict, Any

from src.app import App
from src.core.request import Request
from src.core.response import Response
from src.routing.router import Router
from src.routing.lazy_route import LazyRoute
from src.core.view import View


@pytest.fixture
def app():
    app = App("test_app")
    return app


def start_response(status, headers, exc_info=None):
    return


def test_route_registration(app):
    router = Router()

    def test_handler(req: Request) -> Response:
        return Response(status='200 OK', body=[b'Test'])

    router.add_route('/test', test_handler, methods=['GET'])
    assert len(router.routes) == 1
    assert isinstance(router.routes[0], LazyRoute)


def test_request_processing(app):
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/test',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '8000',
        'wsgi.input': b'',
        'wsgi.url_scheme': 'http',
        'CONTENT_LENGTH': '0'
    }

    def test_handler(req: Request) -> Response:
        return Response(status='200 OK', body=[b'Test'])

    app.router.add_route('/test', test_handler, methods=['GET'])

    response = app(environ, start_response)
    assert response is not None
    assert b'Test' in b''.join(response)


def test_view_execution(app):
    class TestView(View):
        def get(self, request: Request, params: Dict[str, Any] = None) -> Response:
            return Response(status='200 OK', body=[b'Hello from View'])

    app.router.add_route('/view', TestView, methods=['GET'])

    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/view',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '8000',
        'wsgi.input': b'',
        'wsgi.url_scheme': 'http',
        'CONTENT_LENGTH': '0'
    }

    response = app(environ, start_response)
    assert response is not None
    assert b'Hello from View' in b''.join(response)





