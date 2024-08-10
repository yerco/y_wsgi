from src.plugins.base_plugin import BasePlugin
from src.core.response import Response


class DemoPlugin(BasePlugin):
    def register(self, app):
        # Ensure the route is registered in the correct module context
        @app.route('/demo-plugin', methods=['GET'])
        def demo_plugin_handler(request_context, *args, **kwargs):
            return Response(body=[b'Demo Plugin'], status='200 OK')
