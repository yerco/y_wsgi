from typing import Any

from src.core.view import View
from src.core.request_context import RequestContext
from src.core.response import Response


class ViewDecorator(View):
    def __init__(self, view: View):
        super().__init__()
        self._view = view

    def execute(self, request_context: RequestContext, **params: Any) -> Response:
        return self._view.execute(request_context, **params)
