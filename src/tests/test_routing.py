from src.routing.router import Router
from src.core.request import Request
from src.core.response import Response


def test_route_matching():
    router = Router()
    methods = ['GET']

    def test_handler(req):
        return Response(status='200 OK', body=[b'Test Route'])

    router.add_route('/test', test_handler, methods=methods)
    handler, params = router.match('/test', 'GET')

    assert handler is not None
    assert params == {}

    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'})
    response = handler(request)
    assert response.status == '200 OK'
    assert b''.join(response.body) == b'Test Route'


def test_route_not_found():
    router = Router()
    methods = ['GET']
    router.add_route('/test', lambda req: Response(status='200 OK', body=[b'Test Route']), methods=methods)

    handler, params = router.match('/notfound', 'GET')
    assert handler is None
    assert params == {}


def test_method_not_allowed():
    router = Router()
    methods = ['GET']
    router.add_route('/test', lambda req: Response(status='200 OK', body=[b'Test Route']), methods=methods)

    handler, params = router.match('/test', 'POST')
    assert handler is None
    assert params == {}


def test_dynamic_route_matching():
    router = Router()
    methods = ['GET']

    def user_handler(req: Request, id: int) -> Response:
        return Response(status='200 OK', body=[f'User {id}'.encode()])

    router.add_route('/user/<int:id>', user_handler, methods=methods)

    handler, params = router.match('/user/42', 'GET')
    assert handler is not None
    assert params == {'id': '42'}

    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/user/42'})
    response = handler(request, **params)
    assert response.status == '200 OK'
    assert b''.join(response.body) == b'User 42'


def test_multiple_methods():
    router = Router()
    methods = ['GET', 'POST']
    router.add_route('/test', lambda req: Response(status='200 OK', body=[b'Test Route']), methods=methods)

    handler, params = router.match('/test', 'GET')
    assert handler is not None
    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'})
    response = handler(request)
    assert response.status == '200 OK'

    handler, params = router.match('/test', 'POST')
    assert handler is not None
    request = Request({'REQUEST_METHOD': 'POST', 'PATH_INFO': '/test'})
    response = handler(request)
    assert response.status == '200 OK'


def test_route_with_query_parameters():
    router = Router()
    methods = ['GET']
    router.add_route('/test', lambda req: Response(status='200 OK', body=[b'Test Route']), methods=methods)

    handler, params = router.match('/test?query=param', 'GET')
    assert handler is not None
    assert params == {}

    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test', 'QUERY_STRING': 'query=param'})
    response = handler(request)
    assert response.status == '200 OK'
    assert b''.join(response.body) == b'Test Route'
    assert request.get_query_params() == {'query': ['param']}
