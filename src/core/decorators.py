from src.core.view_decorator import ViewDecorator
from src.core.request_context import RequestContext
from src.core.response import Response


class LogRequestDecorator(ViewDecorator):
    def execute(self, request_context: RequestContext, **params) -> Response:
        print(f"Logging request: {request_context.path}")
        return super().execute(request_context, **params)


class CustomHeadersDecorator(ViewDecorator):
    def execute(self, request_context: RequestContext, **params) -> Response:
        response = super().execute(request_context, **params)
        response.set_header("X-Custom-Header", "A Custom Value")
        return response
