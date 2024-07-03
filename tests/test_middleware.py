from typing import Optional
from src.middleware.middleware import Middleware
from src.core.request import Request
from src.core.response import Response
from src.app import App


class TestMiddleware(Middleware):
    def before_request(self, request: Request) -> Optional[Response]:
        request.environ['TEST_BEFORE'] = 'before_request'
        return None

    def after_request(self, request: Request, response: Response) -> Response:
        response.add_header('X-Test-After', 'after_request')
        return response


def test_middleware_registration():
    app = App()
    app.use_middleware(TestMiddleware)

    assert len(app.middlewares) == 1
    assert isinstance(app.middlewares[0], TestMiddleware)


def test_middleware_execution():
    app = App()
    app.use_middleware(TestMiddleware)

    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'})
    response = Response(status='200 OK', body=[b'Test'])

    # Simulate before_request
    app._apply_before_request_middlewares_and_hooks(request)
    assert request.environ['TEST_BEFORE'] == 'before_request'

    # Simulate after_request
    response = app._apply_after_request_middlewares_and_hooks(request, response)
    assert response.headers[-1] == ('X-Test-After', 'after_request')
