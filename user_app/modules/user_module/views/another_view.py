from typing import Dict, Any

from src.core.view import View
from src.core.decorators import LogRequestDecorator, CustomHeadersDecorator
from src.http.http_response_builder import HTTPResponseBuilder


class AnotherView(View):
    def get(self, request_context, params: Dict[str, Any] = None):
        response_builder = HTTPResponseBuilder()
        response = (response_builder
                    .set_status(200)
                    .set_body(b"Another view")
                    .set_header("Content-type", "text/plain")
                    .build())
        return response


another_view = AnotherView()
decorated_view = LogRequestDecorator(CustomHeadersDecorator(another_view))


class ExampleAsView(View):
    def get(self, request_context, params: Dict[str, Any] = None):
        response_builder = HTTPResponseBuilder()
        response = (response_builder
                    .set_status(200)
                    .set_body(b"Hello from Example view")
                    .set_header("Content-type", "text/plain")
                    .build())
        return response


example_as_view = ExampleAsView()


def register_routes(module):
    @module.route('/another', methods=['GET'])
    def another_view_handler(request_context, **kwargs):
        return decorated_view(request_context, **kwargs)

    @module.route('/example-as-view', methods=['GET'])
    def example_as_view_handler(request_context, **kwargs):
        return example_as_view(request_context, **kwargs)
