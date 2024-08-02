from src.forms.fields import CharField, EmailField
from src.forms.form import BaseForm


class UserForm(BaseForm):
    username = CharField(label="Username", required=True)
    password = CharField(label="Password", required=True)
    email = EmailField(label="Email", required=True)
