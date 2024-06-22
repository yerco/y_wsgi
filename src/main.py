import json
from typing import List, Tuple

from src.app import App
from src.response import Response
from src.request import Request

app = App()


@app.route('/')
def hello_world_handler(request: Request) -> Response:
    # Define the status and headers explicitly
    status: str = '200 OK'  # HTTP Status
    headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]  # HTTP Headers
    # byte strings for the response body to handle any kind of content (images, videos, or binary data)
    return Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World'])


@app.route('/json')
def json_handler(request: Request) -> Response:
    data = {'message': 'Hello, JSON!'}
    status: str = '200 OK'
    headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
    return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])
