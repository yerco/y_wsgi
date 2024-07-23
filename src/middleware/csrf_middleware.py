import os
import hmac
import hashlib
from typing import Optional
from src.core.request_context import RequestContext
from src.core.response import Response
from src.middleware.middleware import Middleware


class CSRFMiddleware(Middleware):
    def __init__(self, secret_key: str, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.secret_key = secret_key

    def generate_csrf_token(self, session_id: str) -> str:
        return hmac.new(self.secret_key.encode(), session_id.encode(), hashlib.sha256).hexdigest()

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        if request_context.request.headers.get('Content-Type') == 'application/json':
            return None

        if request_context.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            token = request_context.get_form_data().get("csrf_token")
            if not token or token != self.generate_csrf_token(request_context.session_context.id):
                return Response(b"Invalid CSRF Token", status="403 Forbidden")
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Optional[Response]:
        if request_context.method == "GET":
            csrf_token = self.generate_csrf_token(request_context.session_context.id)
            response.headers_dict["X-CSRF-Token"] = csrf_token
        return response
