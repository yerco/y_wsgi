from typing import Any, Dict, List, Type, TypeVar, Optional

from src.database.orm_interface import ORMInterface
from src.database.models import Model
from user_app.database.database import database

T = TypeVar('T', bound=Model)


class ORM(ORMInterface):
    def __init__(self) -> None:
        self.models: Dict[str, Type[Model]] = {}
        self.last_id: Dict[str, int] = {}
        self.database: Dict[str, List[Model]] = {}

    def register(self, model_class: Type[T]) -> None:
        model_name = model_class.__name__.lower()
        self.models[model_class.__name__.lower()] = model_class
        self.last_id[model_name] = 0
        self.database[model_name + 's'] = []

    def create(self, model_class: Type[T], **kwargs: Any) -> T:
        model_name = model_class.__name__.lower()
        model = self.models[model_name]
        instance = model(**kwargs)

        # Handle auto-increment ID
        self.last_id[model_name] += 1
        instance.id = self.last_id[model_name]

        # Appending 's': To clearly indicate that the dictionary entry stores multiple instances of the model.
        # This is a common practice to differentiate between collections of objects versus single instances.
        self.database[model_name.lower() + 's'].append(instance)
        return instance

    def all(self, model_class: Type[T]) -> List[T]:
        model_name = model_class.__name__.lower()
        return self.database[model_name + 's']

    def filter(self, model_class: Type[T], **kwargs: Any) -> List[T]:
        model_name = model_class.__name__.lower()
        result = []
        for instance in self.database[model_name.lower() + 's']:
            if all(getattr(instance, k) == v for k, v in kwargs.items()):
                result.append(instance)
        return result

    def get_by_id(self, model_class: Type[T], id: int) -> Optional[T]:
        model_name = model_class.__name__.lower()
        for instance in self.database[model_name + 's']:
            if instance.id == id:
                return instance
        return None

    def wipe_database(self) -> None:
        for key in database:
            self.database[key] = []
