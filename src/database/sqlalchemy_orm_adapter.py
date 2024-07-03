from typing import Any, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from src.database.orm_interface import ORMInterface
from src.database.config import SessionLocal, Base


T = TypeVar('T', bound=Base)


class SQLAlchemyORMAdapter(ORMInterface):
    def __init__(self):
        self.db: Session = SessionLocal()

    def create(self, model_class: Type[T], **kwargs: Any) -> T:
        instance = model_class(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def all(self, model_class: Type[T]) -> List[T]:
        return self.db.query(model_class).all()

    def filter(self, model_class: Type[T], **kwargs: Any) -> List[T]:
        query = self.db.query(model_class)
        for k, v in kwargs.items():
            query = query.filter(getattr(model_class, k) == v)
        return query.all()

    def get_by_id(self, model_class: Type[T], id: int) -> Optional[T]:
        return self.db.query(model_class).get(id)
