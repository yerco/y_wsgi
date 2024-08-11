import jwt

from typing import Optional

from src.core.request_context import RequestContext
from src.middleware.middleware import Middleware
from src.core.response import Response

from user_app.config import config


class JWTAuthMiddleware(Middleware):
    def before_request(self, request_context):
        # We are lowercasing headers
        token = request_context.request.headers.get('authorization')

        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
            try:
                decoded = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
                request_context.user = decoded['user']  # Attach user info to request context
            except jwt.ExpiredSignatureError as e:
                return Response(status="401 Unauthorized", body=[b"Token has expired"])
            except jwt.InvalidTokenError as e:
                return Response(status="401 Unauthorized", body=[b"Invalid token"])
            except Exception as e:
                return Response(status="401 Unauthorized", body=[b"Unexpected error"])
        else:
            return Response(status="401 Unauthorized", body=[b"Authorization token is missing"])
