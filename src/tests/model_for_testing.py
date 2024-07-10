from src.database.fields import IntegerField, CharField
from src.database.models import Model


class ModelForTesting(Model):
    id = IntegerField('id')
    username = CharField('username')
    password = CharField('password')
    role = CharField('role')

    def __repr__(self):
        return f'<ModelForTesting {self.id} {self.username} {self.role}>'
