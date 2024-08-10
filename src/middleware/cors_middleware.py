from typing import Optional

from src.core.request_context import RequestContext
from src.core.response import Response
from src.middleware.middleware import Middleware
from src.config_loader import load_config
from src.utils.merge_configs import BaseConfig, merge_configs


class CORSMiddleware(Middleware):
    def __init__(self, config=None, max_age: int = 3600):
        super().__init__()
        self.config = merge_configs(config if config else BaseConfig(), load_config())
        self.allowed_origins = self.config.ALLOWED_ORIGINS if self.config.ALLOWED_ORIGINS else ["*"]
        self.allowed_methods = self.config.ALLOWED_METHODS if self.config.ALLOWED_METHODS else ["GET", "POST", "PUT",
                                                                                                "DELETE", "OPTIONS"]
        self.allowed_headers = self.config.ALLOWED_HEADERS if self.config.ALLOWED_HEADERS else ["Content-Type",
                                                                                                "Authorization"]
        self.max_age = max_age

    # Preflight request
    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        origin = request_context.headers.get("Origin") or request_context.headers.get("origin", "")
        if origin and (origin in self.allowed_origins or "*" in self.allowed_origins):
            if request_context.method == "OPTIONS":
                response = Response(status=200)
                self._set_cors_headers(request_context, response)
                return response
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Response:
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
