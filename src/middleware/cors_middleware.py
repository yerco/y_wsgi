from typing import List, Optional

from src.core.request_context import RequestContext
from src.core.response import Response
from src.middleware.middleware import Middleware


class CORSMiddleware(Middleware):
    def __init__(self, allowed_origins: Optional[list[str]] = None, allowed_methods: Optional[list[str]] = None,
                 allowed_headers: Optional[list[str]] = None, max_age: int = 3600):
        super().__init__()
        self.allowed_origins = allowed_origins if allowed_origins else ["*"]
        self.allowed_methods = allowed_methods if allowed_methods else ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allowed_headers = allowed_headers if allowed_headers else ["Content-Type", "Authorization"]  # customizable
        self.max_age = max_age

    # Preflight request
    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        print(f"Incoming request: {request_context.method} {request_context.path}")
        print(f"Headers: {request_context.headers}")
        origin = request_context.headers.get("Origin") or request_context.headers.get("origin", "")
        if origin and (origin in self.allowed_origins or "*" in self.allowed_origins):
            if request_context.method == "OPTIONS":
                response = Response(status=200)
                self._set_cors_headers(request_context, response)
                return response
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Response:
        print(f"Response: {response.status_code}")
        print(f"Response Headers: {response.headers_dict}")
        self._set_cors_headers(request_context, response)
        return response

    def _set_cors_headers(self, request_context: RequestContext, response: Response) -> None:
        origin = request_context.headers.get("Origin") or request_context.headers.get("origin", "")
        if "*" in self.allowed_origins or origin in self.allowed_origins:
            response.set_header("Access-Control-Allow-Origin", origin if "*" not in self.allowed_origins else "*")
            response.set_header("Access-Control-Allow-Methods", ", ".join(self.allowed_methods))
            response.set_header("Access-Control-Allow-Headers", ", ".join(self.allowed_headers))
            response.set_header("Access-Control-Allow-Credentials", "true")
            response.set_header("Access-Control-Max-Age", str(self.max_age))
