from src.core.response import Response


def test_response_initialization():
    response = Response(status='200 OK', headers=[('Content-Type', 'text/plain')], body=[b'Hello'])
    assert response.status == '200 OK'
    assert response.headers == [('Content-Type', 'text/plain')]
    assert b''.join(response.body) == b'Hello'


def test_response_set_header():
    response = Response(headers=[('Content-Type', 'text/plain'), ('Content-Length', '5')])
    response.set_header('Content-Type', 'application/json')
    response.set_header('Content-Encoding', 'gzip')
    assert response.headers == [('Content-Type', 'application/json'), ('Content-Length', '5'), ('Content-Encoding', 'gzip')]

