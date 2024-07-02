import re
from typing import Optional, List

from src.middleware.middleware import Middleware
from src.core.request import Request
from src.core.response import Response


class AuthenticationMiddleware(Middleware):
    public_routes: List[str] = ["/", "/greet", "/greet/[^/]+", "/json", "/login", "/about"]

    def before_request(self, request: Request) -> Optional[Response]:
        for public_route in self.public_routes:
            if re.fullmatch(public_route, request.path):
                return None  # Skip authentication for public routes

        token = request.headers.get("X-API-Token")
        if not token or token != "valid_token":
            return Response(status="401 Unauthorized", body=[b"Unauthorized"])
        return None
