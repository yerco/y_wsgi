# DRAFT!
import os
from typing import Optional
from src.core.request_context import RequestContext
from src.middleware.middleware import Middleware
from src.core.response import Response


class ProtectedStaticMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        path_info = request_context.request.environ.get('PATH_INFO', '').lstrip('/')

        # Check if the request is for a protected static file
        if path_info.startswith('protected-assets/'):
            if not self.is_valid(request_context):
                return Response(body=[b"Unauthorized"], status='401 Unauthorized', headers=[('Content-Type', 'text/plain')])

            app_context = request_context.current_app.context
            app_config = app_context.get_config(request_context.current_app.name)
            base_dir = app_config.get('BASE_DIR', '.')
            target_asset = f"{base_dir}/{path_info}"

            if os.path.exists(target_asset):
                with open(target_asset, 'rb') as f:
                    file_content = f.read()
                content_type = self.get_content_type(target_asset)
                return Response(body=[file_content], status='200 OK', headers=[('Content-Type', content_type)])
        return None

    def is_valid(self, request_context: RequestContext) -> bool:
        # Implement more authentication check logic here
        session_context = request_context.session_context
        return session_context.is_valid()

    def get_content_type(self, file_path: str) -> str:
        if file_path.endswith('.css'):
            return 'text/css'
        elif file_path.endswith('.js'):
            return 'application/javascript'
        elif file_path.endswith('.png'):
            return 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            return 'image/jpeg'
        elif file_path.endswith('.gif'):
            return 'image/gif'
        elif file_path.endswith('.svg'):
            return 'image/svg+xml'
        return 'application/octet-stream'
