import time

from src.core.request import Request
from src.core.response import Response
from src.middleware.middleware import Middleware
from src.session.session_store import SessionStore
from src.session.session import Session
from src.config import config


class SessionMiddleware(Middleware):
    def __init__(self):
        super().__init__()
        self.session_store = SessionStore()

    def before_request(self, request: Request) -> None:
        session_id = request.extract_session_id()
        session = None
        if session_id:
            session = self.session_store.get_session_by_id(session_id)

        if session and not session.is_expired():
            session.update_last_accessed()
            if self._should_regenerate_id(session):
                session.regenerate_id()
                self.session_store.write(session)
                self._set_session_id(request, session.id)
        else:
            session = Session(user_id='guest')
            self.session_store.write(session)
            self._set_session_id(request, session.id)

        request.session = session

    def after_request(self, request: Request, response: Response) -> Response:
        if hasattr(request, 'session_id_to_set'):
            response.headers.append(('Set-Cookie', request.session_id_to_set))
        return response

    def _set_session_id(self, request: Request, session_id: str):
        path = request.path or '/'
        # SameSite=Lax is used to protect against CSRF attacks while allowing the cookie to be sent
        # with top-level navigation.
        # We are hard-coding Path to / (instead of {path}) in the session cookie to ensure it is sent with requests to
        # all paths on the site.
        cookie = f'session_id={session_id}; Path=/; HttpOnly; SameSite=Lax; Secure'
        request.session_id_to_set = cookie

    def _should_regenerate_id(self, session: Session) -> bool:
        # Use config.SESSION_ID_ROTATION_INTERVAL if defined, otherwise use 1800
        rotation_interval = config.SESSION_ID_ROTATION_INTERVAL if (config.SESSION_ID_ROTATION_INTERVAL
                                                                    is not None) else 1800
        return (time.time() - session.created_at) > rotation_interval
