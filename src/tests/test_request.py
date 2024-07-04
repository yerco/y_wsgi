from src.core.request import Request


def test_request_query_params():
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/test',
        'QUERY_STRING': 'name=John&age=30&age=40'
    }
    request = Request(environ)
    query_params = request.get_query_params()

    assert query_params['name'] == ['John']
    assert query_params['age'] == ['30', '40']


def test_request_query_params_empty():
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/test',
        'QUERY_STRING': ''
    }
    request = Request(environ)
    query_params = request.get_query_params()

    assert query_params == {}


def test_request_query_params_single():
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/test',
        'QUERY_STRING': 'single=param'
    }
    request = Request(environ)
    query_params = request.get_query_params()

    assert query_params['single'] == ['param']
