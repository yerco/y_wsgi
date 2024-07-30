from src.forms.fields import BaseForm, CharField, EmailField


class UserForm(BaseForm):
    username = CharField(label="Username", required=True)
    password = CharField(label="Password", required=True)
    email = EmailField(label="Email", required=True)
