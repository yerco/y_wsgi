from typing import List, Optional

from src.database.repository_interface import RepositoryInterface
from src.database.orm_interface import ORMInterface
from user_app.modules.user_module.models.models import User


class UserRepository(RepositoryInterface[User]):
    def __init__(self, orm: ORMInterface):
        self.orm = orm

    def add(self, entity: User) -> None:
        self.orm.create(User, **entity.__dict__)

    def get(self, id: int) -> Optional[User]:
        return self.orm.get_by_id(User, id)

    def all(self) -> List[User]:
        return self.orm.all(User)

    def filter(self, **kwargs) -> List[User]:
        return self.orm.filter(User, **kwargs)

    def delete(self, entity: User) -> None:
        # Implement deletion logic here if needed
        pass
