import re

from typing import Union, Dict, List

from src.auth.state import AuthContext, AuthenticatedState, UnauthenticatedState, LockedState
from src.core.request import Request
from src.core.response import Response
from src.middleware.middleware import Middleware
from src.config import config


class AuthenticationMiddleware(Middleware):

    def __init__(self, public_routes: List[str]):
        super().__init__()
        self.auth_context = AuthContext()
        self.public_routes = public_routes
        self.MAX_FAILED_ATTEMPTS = config.MAX_FAILED_ATTEMPTS

    def before_request(self, request: Request):
        for public_route in self.public_routes:
            if re.fullmatch(public_route, request.path):
                print(f"Framework's Middleware: Path {request.path} matches public route {public_route}")
                return None  # Skip authentication for public routes

        # if request.path not in self.public_routes:
        #     return Response(status="401 Unauthorized", body=[b"Unauthorized"])  # Block access

        username = request.headers.get("x-username")
        password = request.headers.get("x-password")

        if isinstance(self.auth_context.state, LockedState):
            return self.auth_context.handle_request(request)

        if username and password:
            user = self._authenticate(username, password)
            if user:
                self.auth_context.user = user
                self.auth_context.change_state(AuthenticatedState())
            else:
                self.auth_context.failed_attempts += 1
                if self.auth_context.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
                    self.auth_context.lock()
                    return self.auth_context.handle_request(request)
                self.auth_context.change_state(UnauthenticatedState())
        else:
            self.auth_context.change_state(UnauthenticatedState())
            return self.auth_context.handle_request(request)

    def after_request(self, request: Request, response: Response) -> Response:
        self.auth_context.change_state(UnauthenticatedState())
        return response

    def _authenticate(self, username: str, password: str) -> Union[Dict, None]:
        # This is a placeholder implementation, add other logic
        if username == "user" and password == "password":
            return {"username": username}
        return None
