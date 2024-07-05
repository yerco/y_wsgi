from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class RepositoryInterface(Generic[T]):
    def add(self, entity: T) -> None:
        raise NotImplementedError

    def get(self, id: int) -> Optional[T]:
        raise NotImplementedError

    def all(self) -> List[T]:
        raise NotImplementedError

    def filter(self, **kwargs) -> List[T]:
        raise NotImplementedError

    def delete(self, entity: T) -> None:
        raise NotImplementedError
