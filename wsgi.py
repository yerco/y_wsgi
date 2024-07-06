from src.core.dispatcher import Dispatcher

from user_app.main import app_registry as user_app_registry
from admin_app.main import app_registry as admin_app_registry

dispatcher = Dispatcher()

user_app = user_app_registry.get_app('user_app')
dispatcher.add_app('/', user_app)

# Register admin_app with the dispatcher
admin_app = admin_app_registry.get_app('admin_app')
dispatcher.add_app('/admin', admin_app)

# WSGI application entry point
application = dispatcher
