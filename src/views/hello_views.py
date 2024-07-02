from src.views.common_handlers import HelloWorldHandler
from src.core.request import Request
from src.core.response import Response


def register_routes(app):
    @app.route('/')
    class HelloWorld(HelloWorldHandler):
        pass

    @app.route('/hello')
    def hello_handler(request: Request) -> Response:
        return Response(status='200 OK', body=[b'Hello, World!'])
    # Equivalent to:
    # app.route('/hello')(hello_handler)
    # `route`factory
