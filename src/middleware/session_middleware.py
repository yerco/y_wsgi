import time

from src.core.response import Response
from src.middleware.middleware import Middleware
from src.session.session_store import SessionStore
from src.session.session import Session
from src.config_loader import load_config
from src.core.request_context import RequestContext
from src.core.session_context import SessionContext
from src.core.app_context import AppContext


class SessionMiddleware(Middleware):
    def __init__(self):
        super().__init__()
        self.session_store = SessionStore()
        self.config = load_config()

    def before_request(self, request_context: RequestContext) -> None:
        app_context: AppContext = request_context.app_context  # Ensure app context is loaded

        session_id = request_context.request.extract_session_id()
        session = self.session_store.get_session_by_id(session_id) if session_id else None
        session_context = SessionContext(session)

        if session_context.is_valid():
            session_context.session.update_last_accessed()
            if self._should_regenerate_id(session_context):
                session_context.regenerate_id()
                self.session_store.write(session_context.session)
                self._set_session_id(request_context, session_context.session.id)
        else:
            session = Session(user_id='guest')
            self.session_store.write(session)
            self._set_session_id(request_context, session.id)
            session_context.session = session

        request_context.session_context = session_context

    def after_request(self, request_context: RequestContext, response: Response) -> Response:
        if hasattr(request_context.request, 'session_id_to_set'):
            response.set_header('Set-Cookie', request_context.request.session_id_to_set)
        return response

    def _set_session_id(self, request_context: RequestContext, session_id: str):
        path = request_context.request.path or '/'
        # SameSite=Lax is used to protect against CSRF attacks while allowing the cookie to be sent
        # with top-level navigation.
        # We are hard-coding Path to / (instead of {path}) in the session cookie to ensure it is sent with requests to
        # all paths on the site.
        cookie = f'session_id={session_id}; Path=/; HttpOnly; SameSite=Lax; Secure'
        request_context.request.session_id_to_set = cookie

    def _should_regenerate_id(self, session_context: SessionContext) -> bool:
        rotation_interval = self.config.get('SESSION_ID_ROTATION_INTERVAL', 1800)
        return (time.time() - session_context.created_at) > rotation_interval
