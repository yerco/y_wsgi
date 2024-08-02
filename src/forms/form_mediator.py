from typing import Optional, TYPE_CHECKING

from src.forms.mediator import Mediator
from src.middleware.csrf_token import CSRFToken

if TYPE_CHECKING:
    from src.forms.form import BaseForm


class FormMediator(Mediator):
    def __init__(self):
        self.forms = {}
        self.csrf_token: Optional[CSRFToken] = None
        self.session_id = None

    def register_form(self, form):
        self.forms[id(form)] = form

    def set_csrf_token(self, csrf_token: CSRFToken, session_id: str):
        self.csrf_token = csrf_token
        self.session_id = session_id

    def notify(self, sender: 'BaseForm', event: str) -> None:
        if event == "set_csrf":
            csrf_token = sender.request_context.session_context.csrf_token
            if csrf_token:
                sender.embed_csrf_token(csrf_token)
        if event == "csrf_check":
            self._handle_csrf_check(sender)
        # idea
        # if event == "submit":
        #     self._handle_form_submission(sender)

    def _handle_csrf_check(self, sender):
        form_id = id(sender)
        form: 'BaseForm' = self.forms.get(form_id)
        if form:
            if form.csrf_token != sender.request_context.session_context.csrf_token:
                form.errors['csrf_token'] = "Invalid CSRF token"
