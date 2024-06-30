import json
from typing import List, Tuple

from src.app import App
from src.middlewares.logging_middleware import LoggingMiddleware
from src.middlewares.authentication_middleware import AuthenticationMiddleware
from src.response import Response
from src.request import Request
from src.handlers import HelloWorldHandler
from src.hookses import some_hooks

app = App()

# Register Middlewares
app.use_middleware(LoggingMiddleware)
app.use_middleware(AuthenticationMiddleware)

# Register hooks
app.before_request(some_hooks.before_request_hook)
app.after_request(some_hooks.after_request_hook)
app.teardown_request(some_hooks.teardown_request_hook)
app.before_first_request(some_hooks.before_first_request_hook)


@app.route('/')
class HelloWorld(HelloWorldHandler):
    pass


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


@app.route('/hello')
def hello_handler(request: Request) -> Response:
    return Response(status='200 OK', body=[b'Hello, World!'])
# Equivalent to:
# app.route('/hello')(hello_handler)
# `route`factory
