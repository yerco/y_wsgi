from typing import Optional

from src.core.request import Request
from src.core.response import Response


class Middleware:
    def before_request(self, request: Request) -> Optional[Response]:
        """
        Process the request before it reaches the view.
        Return a Response to short-circuit the view, or None to continue.
        """
        pass

    def after_request(self, request: Request, response: Response) -> Response:
        """Process the response after the view has been called."""
        return response
