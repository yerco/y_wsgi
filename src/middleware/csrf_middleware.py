from typing import Optional

from src.core.request_context import RequestContext
from src.core.session_context import SessionContext
from src.core.response import Response
from src.middleware.middleware import Middleware
from src.middleware.csrf_token import CSRFToken
from src.config_loader import load_config


class CSRFMiddleware(Middleware):
    def __init__(self, config, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.config = config if config else load_config()
        secret_key = config.SECRET_KEY
        self.csrf_token = CSRFToken(secret_key)

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        session_context: SessionContext = request_context.session_context
        if not hasattr(session_context, 'csrf_token'):
            if hasattr(session_context, 'id'):
                session_context.csrf_token = self.csrf_token.generate_csrf_token(session_context.id)
            else:
                return Response(b"Session not initialized", status="500 Internal Server Error")

        if request_context.request.headers.get('Content-Type') == 'application/json':
            return None

        if request_context.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            token = request_context.form_data.get("csrf_token")
            if not token or token != self.csrf_token.generate_csrf_token(request_context.session_context.id):
                return Response(b"Invalid CSRF Token", status="403 Forbidden")
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Optional[Response]:
        if request_context.method == "GET":
            token: str = self.csrf_token.generate_csrf_token(request_context.session_context.id)
            request_context.set_csrf_token(token)
            response.headers_dict["X-CSRF-Token"] = token
        return response
