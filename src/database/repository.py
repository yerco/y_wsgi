from typing import List

from src.database.models import User


class UserRepository:
    def __init__(self, orm):
        self.orm = orm

    def add(self, user: User) -> None:
        self.orm.create('user', **user.__dict__)

    def get_by_username(self, username: str) -> User:
        users = self.orm.filter('user', username=username)
        return users[0] if users else None

    def get_all(self) -> List[User]:
        return self.orm.all('user')


# Usage
# repository = UserRepository(orm)
# repository.add(user)
# user = repository.get_by_username('john_doe')
