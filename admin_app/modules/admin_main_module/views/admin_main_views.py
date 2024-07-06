from typing import List, Tuple

from src.core.request import Request
from src.core.response import Response
from src.database.orm_interface import ORMInterface


def register_routes(module, orm: ORMInterface = None):
    @module.route('/admin')
    def admin_main_handler(request: Request) -> Response:
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]
        return Response(status=status, headers=headers, body=[b'We are at the', b' ', b'ADMIN', b' ', b'Realm!'])