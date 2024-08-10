import os

from typing import Optional

from src.core.request_context import RequestContext
from src.middleware.middleware import Middleware
from src.core.response import Response


class StaticMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        path_info = request_context.request.environ.get('PATH_INFO', '').lstrip('/')

        # Check if the request is for a static file
        if path_info.startswith('assets/'):
            app_context = request_context.current_app.context
            app_config = app_context.get_config(request_context.current_app.name)
            base_dir = app_config.BASE_DIR
            target_asset = f"{base_dir}/{path_info}"
            if os.path.exists(target_asset):
                with open(target_asset, 'rb') as f:
                    file_content = f.read()
                content_type = self.get_content_type(target_asset)
                return Response(body=[file_content], status='200 OK', headers=[('Content-Type', content_type)])

        return None

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
