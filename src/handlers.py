from typing import List, Tuple

from src.view import View
from src.request import Request
from src.response import Response


class HelloWorldHandler(View):
    def get(self, request: Request) -> Response:
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]
        return Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World!'])
