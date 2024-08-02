from src.core.request_context import RequestContext
from src.forms.form import BaseForm

from user_app.modules.user_module.forms.custom_user_form import CustomUserForm
from user_app.modules.user_module.forms.admin_user_form import AdminUserForm


class FormFactory:
    @staticmethod
    def create_form(form_type: str, request_context: RequestContext) -> BaseForm:
        if form_type == 'user':
            return request_context.get_form(CustomUserForm)
        elif form_type == 'admin':
            return request_context.get_form(AdminUserForm)
        else:
            raise ValueError(f"Unknown form type: {form_type}")
