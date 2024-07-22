from typing import List, Tuple, Dict, Any

from src.core.view import View
from src.core.request_context import RequestContext
from src.core.response import Response


class HelloWorldHandler(View):
    def get(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]
        return Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World!'])
