from typing import Any, Dict, Optional

from src.core.request import Request
from src.core.session_context import SessionContext
from src.core.app_context import AppContext


class RequestContext:
    def __init__(self, request: Request, app_context: AppContext):
        self.request = request
        self._session_context: Optional[SessionContext] = None
        self._app_context = app_context
        self._user: Optional[Dict[str, Any]] = None

    @property
    def method(self) -> str:
        return self.request.method

    @property
    def path(self) -> str:
        return self.request.path

    @property
    def query_string(self) -> str:
        return self.request.query_string

    @property
    def headers(self) -> Dict[str, str]:
        return self.request.headers

    @property
    def body(self) -> bytes:
        return self.request.body

    @property
    def session_context(self) -> Optional[SessionContext]:
        return self._session_context

    @session_context.setter
    def session_context(self, session_context: SessionContext) -> None:
        self._session_context = session_context

    @property
    def app_context(self) -> AppContext:
        return self._app_context

    def get_query_params(self) -> Dict[str, list[str]]:
        return self.request.get_query_params()

    def get_json(self) -> Dict[str, Any]:
        return self.request.get_json()

    @property
    def user(self) -> Optional[Dict[str, Any]]:
        return self._user

    @user.setter
    def user(self, user: Dict[str, Any]) -> None:
        self._user = user

    # Add other methods to manage context-specific data
    # ...
