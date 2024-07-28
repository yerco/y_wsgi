import json

from typing import List, Tuple

from src.core.request import Request
from src.core.request_context import RequestContext
from src.core.response import Response
from src.database.orm_interface import ORMInterface

from user_app.modules.user_module.models.models import User


def register_routes(module, orm: ORMInterface):
    @module.route('/user_app_page', methods=['GET'])
    def user_app_page(request_context: RequestContext):
        template_vars = {
            'title': 'This is the user_app',
            'message': 'We are in the module user_module',
            'nonce': request_context.request.environ.get('nonce')
        }

        current_app = request_context.current_app
        # current_configuration = request_context.current_configuration
        rendered_template = current_app.render_template('user_app_page.html', template_vars)
        return Response(status='200 OK', body=[rendered_template.encode('utf-8')])

    @module.route('/json')
    def json_handler(request: Request) -> Response:
        data = {'message': 'Hello, JSON!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])

    @module.route('/greet')
    @module.route('/greet/<name>')
    def greet_handler(request: Request, name: str = "Guest") -> Response:
        data = {'message': f'Hello, {name}!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])

    @module.route('/users')
    def list_users(request: Request) -> Response:
        users = orm.all(User)
        users_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(
            status='200 OK',
            headers=[('Content-Type', 'application/json')],
            body=[json.dumps(users_data).encode('utf-8')]
        )

    @module.route('/create_user', methods=['POST'])
    def create_user_view(request: Request) -> Response:
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return Response(
                status='400 Bad Request',
                headers=[('Content-Type', 'application/json')],
                body=[json.dumps({'error': 'Invalid input'}).encode('utf-8')]
            )

        username = data['username']
        password = data['password']
        user = orm.create(User, username=username, password=password)
        return Response(
            status='201 Created',
            headers=[('Content-Type', 'application/json')],
            body=[json.dumps({'id': user.id, 'username': user.username}).encode('utf-8')]
        )

    @module.route('/user/<int:id>')
    def get_user(request: Request, id: int) -> Response:
        id = int(id)  # Ensure id is an integer
        user = orm.get_by_id(User, id)
        if user:
            user_data = {'id': user.id, 'username': user.username}
            return Response(
                status='200 OK',
                headers=[('Content-Type', 'application/json')],
                body=[json.dumps(user_data).encode('utf-8')]
            )
        else:
            return Response(
                status='404 Not Found',
                headers=[('Content-Type', 'application/json')],
                body=[json.dumps({'error': 'User not found'}).encode('utf-8')]
            )

    @module.route('/filter_users/<str:username>', methods=['GET'])
    def filter_users(request: Request, username: str) -> Response:
        users = orm.filter(User, username=username)
        user_list = [user.__dict__ for user in users]
        return Response(status='200 OK', body=[json.dumps(user_list).encode('utf-8')])
