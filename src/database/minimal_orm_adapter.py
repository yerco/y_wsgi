from typing import Any, List, Optional, Type
from src.database.orm_interface import ORMInterface
from src.database.orm import ORM
from src.database.models import Model


class MinimalORMAdapter(ORMInterface):
    def __init__(self, orm: ORM):
        self.orm = orm

    def create(self, model_class: Type[Model], **kwargs: Any) -> Any:
        return self.orm.create(model_class, **kwargs)

    def all(self, model_class: Type[Model]) -> List[Any]:
        return self.orm.all(model_class)

    def filter(self, model_class: Type[Model], **kwargs: Any) -> List[Any]:
        return self.orm.filter(model_class, **kwargs)

    def get_by_id(self, model_class: Type[Model], id: int) -> Optional[Any]:
        return next((item for item in self.orm.all(model_class) if item.id == id), None)
