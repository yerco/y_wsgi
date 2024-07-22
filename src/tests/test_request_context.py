from src.core.request import Request
from src.core.request_context import RequestContext
from src.core.app_context import AppContext


def test_request_context():
    environ = {
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/',
        'QUERY_STRING': '',
        'CONTENT_TYPE': 'application/json',
        'CONTENT_LENGTH': '0',
        'wsgi.input': b'',
    }
    app_context = AppContext()
    request = Request(environ)
    request_context = RequestContext(request, app_context)

    assert request_context.method == 'GET'
    assert request_context.path == '/'
    assert request_context.query_string == ''
    assert request_context.headers['Content-Type'] == 'application/json'
