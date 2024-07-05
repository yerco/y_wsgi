from typing import Any, List, Optional, TypeVar, Type

T = TypeVar('T')


class ORMInterface:
    def create(self, model_class: Type[T], **kwargs: Any) -> T:
        raise NotImplementedError

    def all(self, model_class: Type[T]) -> List[T]:
        raise NotImplementedError

    def filter(self, model_class: Type[T], **kwargs: Any) -> List[T]:
        raise NotImplementedError

    def get_by_id(self, model_class: Type[T], id: int) -> Optional[T]:
        raise NotImplementedError

    def register(self, model_class: Type[T]) -> None:
        raise NotImplementedError
