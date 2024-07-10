from src.database.models import Model
from src.database.fields import IntegerField, CharField


class User(Model):
    id = IntegerField('id')
    username = CharField('username')
    password = CharField('password')
    role = CharField('role')

    def __repr__(self):
        return f'<User {self.id} {self.username} {self.role}>'
