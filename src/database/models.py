from typing import Any

from src.database.fields import IntegerField, CharField


class Model:
    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


class User(Model):
    id = IntegerField('id')
    username = CharField('username')
    password = CharField('password')

    def __repr__(self):
        return f'<User {self.id} {self.username}>'


# Usage
# user = User(username='john_doe', password='password123')
# This calls the `Model` constructor with kwargs:
# super().__init__(username='john_doe', password='password123')
