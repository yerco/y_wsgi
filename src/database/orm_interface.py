from typing import Any, List, Optional, TypeVar

T = TypeVar('T')


class ORMInterface:
    def create(self, model_class: T, **kwargs: Any) -> T:
        raise NotImplementedError

    def all(self, model_class: T) -> List[T]:
        raise NotImplementedError

    def filter(self, model_class: T, **kwargs: Any) -> List[T]:
        raise NotImplementedError

    def get_by_id(self, model_class: T, id: int) -> Optional[T]:
        raise NotImplementedError
