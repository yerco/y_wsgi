from typing import Any, Dict, Optional, TYPE_CHECKING
from urllib.parse import parse_qs

from src.core.request import Request
from src.core.session_context import SessionContext
from src.core.app_context import AppContext

if TYPE_CHECKING:
    from src.app import App


class RequestContext:
    def __init__(self, request: Request, app_context: AppContext):
        self.request = request
        self._session_context: Optional[SessionContext] = None
        self._app_context = app_context
        self._user: Optional[Dict[str, Any]] = None
        self.current_module_dir: Optional[str] = None

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

    @property
    def current_app(self) -> Optional['App']:
        app_name = self.app_context.get_current_app_name()
        if app_name:
            return self.app_context.get_app_instance(app_name)
        raise ValueError("No current app set in context.")

    @property
    def current_configuration(self) -> Dict[str, Any]:
        app_name = self.app_context.get_current_app_name()
        if app_name:
            return self.app_context.get_config(app_name)
        raise ValueError("No current app set in context.")

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

    def get_form_data(self) -> Dict[str, str]:
        if self.method in ("POST", "PUT", "PATCH", "DELETE"):
            content_type = self.headers.get("Content-Type", "")
            if 'application/x-www-form-urlencoded' in content_type:
                return self.parse_form_urlencoded()
            elif 'multipart/form-data' in content_type:
                return self.parse_multipart()
        return {}

    def parse_form_urlencoded(self) -> Dict[str, str]:
        return {k: v[0] for k, v in parse_qs(self.request.body.decode()).items()}

    def parse_multipart(self) -> Dict[str, str]:
        raise NotImplementedError("Multipart form data parsing is not implemented yet")

    def set_current_module_dir(self, module_dir: str) -> None:
        self.current_module_dir = module_dir

    def get_current_module_dir(self) -> Optional[str]:
        return self.current_module_dir
