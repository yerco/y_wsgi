from src.forms.user_form import UserForm
from src.forms.fields import CharField


class CustomUserForm(UserForm):
    first_name = CharField(label="First Name", required=False)
    last_name = CharField(label="Last Name", required=False)
