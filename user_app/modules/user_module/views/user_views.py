import json

from typing import List, Tuple

from src.core.request_context import RequestContext
from src.core.response import Response
from src.database.orm_interface import ORMInterface

from user_app.modules.user_module.models.models import User
from user_app.modules.user_module.forms.form_factory import FormFactory
from user_app.modules.user_module.forms.composite_form import UserForm


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
    def json_handler(request_context: RequestContext) -> Response:
        data = {'message': 'Hello, JSON!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])

    @module.route('/greet')
    @module.route('/greet/<name>')
    def greet_handler(request_context: RequestContext, name: str = "Guest") -> Response:
        data = {'message': f'Hello, {name}!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])

    @module.route('/users')
    def list_users(request_context: RequestContext) -> Response:
        users = orm.all(User)
        users_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(
            status='200 OK',
            headers=[('Content-Type', 'application/json')],
            body=[json.dumps(users_data).encode('utf-8')]
        )

    @module.route('/create_user', methods=['POST'])
    def create_user_view(request_context: RequestContext) -> Response:
        data = request_context.get_json()

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
    def get_user(request_context: RequestContext, id: int) -> Response:
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
    def filter_users(request: RequestContext, username: str) -> Response:
        users = orm.filter(User, username=username)
        user_list = [user.__dict__ for user in users]
        return Response(status='200 OK', body=[json.dumps(user_list).encode('utf-8')])

    @module.route('/register', methods=['GET', 'POST'])
    @module.route('/register/admin', methods=['GET', 'POST'])
    def register_handler(request_context: RequestContext) -> Response:
        if request_context.path.endswith('/admin'):
            form_type = 'admin'
        else:
            form_type = 'user'

        form = FormFactory.create_form(form_type, request_context)

        if request_context.method == 'POST':
            if form.is_valid():
                # Process valid form data
                return Response(status='200 OK', body=[b'User registered successfully'])
            else:
                # Handle form errors
                return form.render_response(status='400 Bad Request')
        else:
            return form.render_response(status='200 OK')

    @module.route('/register/user', methods=['GET', 'POST'])
    def register_user_handler(request_context: RequestContext) -> Response:
        action_url = '/register/user'  # Or dynamically determine this

        csrf_token = request_context.get_csrf_token()
        composite_form = UserForm(action=action_url, include_submit_button=True, csrf_token=csrf_token)

        if request_context.method == 'POST':
            try:
                data = request_context.get_form_data()
                composite_form.validate(data)
                composite_form.render()
            except ValueError as e:
                return Response(status='400 Bad Request', body=[str(e).encode('utf-8')])
        else:
            return Response(status="200 OK", body=[composite_form.render().encode('utf-8')],
                            headers=[('Content-Type', 'text/html')])
