import json
from typing import List, Tuple


from src.core.request import Request
from src.core.response import Response


def register_routes(app):
    @app.route('/json')
    def json_handler(request: Request) -> Response:
        data = {'message': 'Hello, JSON!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])

    @app.route('/greet')
    @app.route('/greet/<name>')
    def greet_handler(request: Request, name: str = "Guest") -> Response:
        data = {'message': f'Hello, {name}!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])