from src.middleware.middleware import Middleware
from src.core.request import Request
from src.core.response import Response
from typing import Optional


class LoggingMiddleware(Middleware):
    def before_request(self, request: Request) -> Optional[Response]:
        print(f'Processing request: {request.method} {request.path}')
        return None

    def after_request(self, request: Request, response: Response) -> Response:
        print(f'Processing response: {response.status_code}')
        return response
