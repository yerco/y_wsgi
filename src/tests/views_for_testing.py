from typing import List, Tuple

from src.database.orm import ORMInterface
from src.core.request_context import RequestContext
from src.core.response import Response


def register_routes(module, orm: ORMInterface):
    @module.route('/public')
    def public_handler(request: RequestContext) -> Response:
        return Response(status='200 OK', body=[b'Public Content'])

    @module.route('/private')
    def private_handler(request_context: RequestContext) -> Response:
        return Response(status='200 OK', body=[b'Private Content'])

    @module.route('/')
    def index_handler(request_context: RequestContext) -> Response:
        session_context = request_context.session_context
        body = f"Session ID: {session_context.session.id}, User ID: {session_context.session.user_id}".encode('utf-8')
        return Response(status='200 OK', body=[body])
