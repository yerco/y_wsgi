from src.core.response import Response


def test_response_initialization():
    response = Response(status='200 OK', headers=[('Content-Type', 'text/plain')], body=[b'Hello'])
    assert response.status == '200 OK'
    assert response.headers == [('Content-Type', 'text/plain')]
    assert b''.join(response.body) == b'Hello'
