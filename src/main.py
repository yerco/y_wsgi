import json
from typing import List, Tuple

from src.app import App
from src.response import Response
from src.request import Request
from src.handlers import HelloWorldHandler

app = App()


@app.route('/')
class HelloWorld(HelloWorldHandler):
    pass


@app.route('/json')
def json_handler(request: Request) -> Response:
    data = {'message': 'Hello, JSON!'}
    status: str = '200 OK'
    headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
    return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])
