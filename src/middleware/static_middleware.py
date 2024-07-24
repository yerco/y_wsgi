import os
from typing import Optional

from src.core.request_context import RequestContext
from src.utils.template_scanner import TemplateScanner
from src.middleware.middleware import Middleware
from src.core.response import Response


class StaticMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        app = request_context.current_app
        current_config = request_context.current_configuration
        scanner = TemplateScanner(base_dir=current_config.get('base_dir', '.'))
        template_directory = scanner.scan()
        module, module_templates_dir = list(template_directory.items())[0]
        assets_dir = os.path.abspath(os.path.join(module_templates_dir, '..', 'assets'))

        path_info = request_context.request.environ.get('PATH_INFO', '')
        if path_info.startswith('/assets/'):
            relative_path = path_info.lstrip('/')
            file_path = os.path.join(assets_dir, os.path.relpath(relative_path, 'assets'))

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    content_type = self.get_content_type(file_path)
                return Response(body=file_content, status='200 OK', headers=[('Content-Type', content_type)])
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
