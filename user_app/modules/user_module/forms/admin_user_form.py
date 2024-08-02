from src.forms.user_form import UserForm
from src.forms.fields import CharField, IntegerField


class AdminUserForm(UserForm):
    first_name = CharField(label="First Name", required=False)
    last_name = CharField(label="Last Name", required=False)
    extra_security_code = IntegerField(label="Extra security code", required=True)
