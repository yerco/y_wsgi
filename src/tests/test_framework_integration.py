import pytest
from src.app import App
from src.tests.test_client import FrameworkTestClient
from src.core.request import Request
from src.core.response import Response
from user_app.modules.user_module.middleware.logging_middleware import LoggingMiddleware
from src.core.view import View
from typing import Dict, Any


@pytest.fixture
def app():
    app = App()
    return app


@pytest.fixture
def client(app):
    return FrameworkTestClient(app)


def test_client_get_request(client):
    @client.app.route('/test')
    def test_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Test GET Response'])

    response = client.get('/test')
    assert response.status == '200 OK'
    assert b'Test GET Response' in response.body


def test_client_post_request(client):
    @client.app.route('/test', methods=['POST'])
    def test_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Test POST Response'])

    response = client.post('/test', data={'key': 'value'})
    assert response.status == '200 OK'
    assert b'Test POST Response' in response.body


def test_client_with_query_params(client):
    @client.app.route('/search')
    def search_handler(request: Request) -> Response:
        query_params = request.get_query_params()
        print("Query Params:", query_params)  # Debugging output
        return Response(status='200 OK', body=[f'Search query: {query_params["query"][0]}'.encode()])

    response = client.get('/search?query=test')
    assert response.status == '200 OK'
    assert b'Search query: test' in response.body


def test_client_with_headers(client):
    @client.app.route('/header-test')
    def headers_handler(request: Request) -> Response:
        custom_header = request.headers.get('x-custom-header')
        return Response(status='200 OK', body=[f'Custom Header: {custom_header}'.encode()])

    headers = {'X-Custom-Header': 'TestValue'}
    response = client.get('/header-test', headers=headers)
    assert response.status == '200 OK'
    assert b'Custom Header: TestValue' in response.body


def test_client_with_middleware(client):
    client.app.use_middleware(LoggingMiddleware)

    @client.app.route('/middleware')
    def middleware_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Middleware Response'])

    response = client.get('/middleware')
    assert response.status == '200 OK'
    assert b'Middleware Response' in response.body


def test_client_with_view(client):
    class TestView(View):
        def get(self, request: Request, params: Dict[str, Any] = None) -> Response:
            return Response(status='200 OK', body=[b'Hello from View'])

    client.app.router.add_route('/view', TestView, methods=['GET'])

    response = client.get('/view')
    assert response.status == '200 OK'
    assert b'Hello from View' in response.body
