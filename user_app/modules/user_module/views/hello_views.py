import datetime
import json
import jwt

from src.core.request_context import RequestContext
from src.core.response import Response

from user_app.modules.user_module.proxy.request_proxy import RequestProxy
from user_app.modules.user_module.views.common_handlers import HelloWorldHandler, ProxyExampleHandler
from user_app.config import config


def register_routes(module):
    @module.route('/')
    class HelloWorld(HelloWorldHandler):
        pass

    # At the moment not authorized by the middleware
    @module.route('/jinja2')
    def hello_handler(request_context: RequestContext) -> Response:
        template_vars = {
            'title': 'Jinja2 Integration',
            'features': ['Dynamic templating', 'Flexible design', 'Easy integration'],
            'user': 'John Doe',
            'nonce': request_context.request.environ.get('nonce')
        }
        current_app = request_context.current_app
        rendered_template = current_app.render_template('jinja2.html', template_vars)
        return Response(status='200 OK', body=[rendered_template.encode('utf-8')])

    @module.route('/proxy-example')
    def proxy_example_handler(request_context: RequestContext) -> Response:
        original_view = ProxyExampleHandler()
        proxied_view = RequestProxy(original_view)
        return proxied_view.execute(request_context)

    # Do not forget to deactivate CSRFMiddleware
    # To test you can use `curl -X POST http://localhost:8000/generate-token -H "Content-Type: application/json"
    # -d '{"username": "jwt-test-user"}'`
    @module.route('/generate-token', methods=['POST'])
    def generate_token_handler(request_context: RequestContext) -> Response:
        body = request_context.body.decode('utf-8')
        body_json = json.loads(body)
        if body_json and body_json.get('username') == 'jwt-test-user':
            payload = {
                'user': 'jwt-test-user',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=config.JWT_EXPIRATION_DELTA)
            }
            token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
            return Response(status='200 OK', body=[token.encode('utf-8')])
        else:
            return Response(status='401 Unauthorized', body=[b'Invalid credentials'])
