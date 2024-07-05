from typing import Any, List, Optional, Type, TypeVar
from src.database.orm_interface import ORMInterface
from src.database.orm import ORM

T = TypeVar('T')


class MinimalORMAdapter(ORMInterface):
    def __init__(self, orm: ORM):
        self.orm = orm

    def register(self, model_class: Type[T]) -> None:
        self.orm.register(model_class)

    def create(self, model_class: Type[T], **kwargs: Any) -> Any:
        return self.orm.create(model_class, **kwargs)

    def all(self, model_class: Type[T]) -> List[Any]:
        return self.orm.all(model_class)

    def filter(self, model_class: Type[T], **kwargs: Any) -> List[Any]:
        return self.orm.filter(model_class, **kwargs)

    def get_by_id(self, model_class: Type[T], id: int) -> Optional[Any]:
        return next((item for item in self.orm.all(model_class) if item.id == id), None)
