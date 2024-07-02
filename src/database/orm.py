from typing import Any, Dict, List, Type, TypeVar

from src.database.models import Model


# Simple in-memory storage/database
database: Dict[str, List[Model]] = {
    'users': []
}

T = TypeVar('T', bound=Model)


class ORM:
    def __init__(self):
        self.models: Dict[str, Type[Model]] = {}
        self.counters: Dict[str, int] = {}

    def register(self, model_class: Type[T]) -> None:
        model_name = model_class.__name__.lower()
        self.models[model_class.__name__.lower()] = model_class
        self.counters[model_name] = 1

    def create(self, model_name: str, **kwargs: Any) -> T:
        model = self.models[model_name]
        instance = model(**kwargs)

        # Auto-increment id handling
        if hasattr(instance, 'id') and instance.id is None:
            instance.id = self.counters[model_name]
            self.counters[model_name] += 1

        # Appending 's': To clearly indicate that the dictionary entry stores multiple instances of the model.
        # This is a common practice to differentiate between collections of objects versus single instances.
        database[model_name.lower() + 's'].append(instance)
        return instance

    def all(self, model_name: str) -> List[T]:
        return database[model_name.lower() + 's']

    def filter(self, model_name: str, **kwargs: Any) -> List[T]:
        result = []
        for instance in database[model_name.lower() + 's']:
            if all(getattr(instance, k) == v for k, v in kwargs.items()):
                result.append(instance)
        return result
