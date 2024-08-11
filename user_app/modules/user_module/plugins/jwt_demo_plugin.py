from src.app import App
from src.core.request_context import RequestContext
from src.plugins.base_plugin import BasePlugin
from src.core.response import Response

from user_app.modules.user_module.middleware.jwt_auth_middleware import JWTAuthMiddleware


class JWTDemoPlugin(BasePlugin):
    def register(self, app: App):
        @app.route("/jwt-demo", methods=["GET"])
        def jwt_demo_handler(request_context: RequestContext, *args, **kwargs):
            middleware = JWTAuthMiddleware()
            response = middleware.before_request(request_context)
            if response:  # If middleware returns a response, something went wrong (e.g., missing/invalid token)
                return response

            return Response(body=[b"This is protected content. You have a valid JWT!"], status="200 OK")
