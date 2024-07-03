from src.core.view import View
from src.core.request import Request
from src.core.response import Response


class FrameworkTestView(View):
    def get(self, request: Request, params=None) -> Response:
        return Response(status='200 OK', body=[b'Test View'])


def test_view_get():
    view = FrameworkTestView()
    request = Request({'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'})
    response = view.get(request)
    assert response.status == '200 OK'
    assert b''.join(response.body) == b'Test View'
