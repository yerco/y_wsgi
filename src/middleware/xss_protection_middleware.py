import html
import base64
import os

from typing import Optional

from src.core.request_context import RequestContext
from src.middleware.middleware import Middleware
from src.core.response import Response


class XSSProtectionMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        # Generate a nonce for this request
        nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        request_context.request.environ['nonce'] = nonce
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Optional[Response]:
        nonce = request_context.request.environ.get('nonce', '')

        if isinstance(response.body, list):
            sanitized_body = [self.sanitize_output(part) for part in response.body]
            response.body = sanitized_body
        elif isinstance(response.body, bytes):
            response.body = self.sanitize_output(response.body)

        # Add Content Security Policy (CSP) header
        csp = (
            f"default-src 'self'; "
            f"style-src 'self' 'nonce-{nonce}'; "
            f"script-src 'self' 'nonce-{nonce}'; "
            "object-src 'none';"
        )
        response.set_header('Content-Security-Policy', csp)

        # Add X-XSS-Protection header
        response.set_header('X-XSS-Protection', '1; mode=block')

        return response

    def sanitize_output(self, output: bytes) -> bytes:
        return output  # Do not escape the entire HTML - html.escape(output.decode('utf-8')).encode('utf-8')
