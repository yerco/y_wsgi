from typing import List, Tuple, Dict, Any

from src.core.view import View
from src.core.request import Request
from src.core.response import Response


class HelloWorldHandler(View):
    def get(self, request: Request, params: Dict[str, Any] = None) -> Response:
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]
        return Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World!'])
