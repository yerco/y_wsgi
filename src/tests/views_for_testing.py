from typing import List, Tuple

from src.database.orm import ORMInterface
from src.core.request import Request
from src.core.response import Response


def register_routes(module, orm: ORMInterface):
    @module.route('/public')
    def public_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Public Content'])

    @module.route('/private')
    def private_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Private Content'])
