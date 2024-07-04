from typing import Type, List

from src.database.models import Model
from src.database.orm_interface import ORMInterface
from src.database.orm import ORM as MinimalORM
from src.database.sqlalchemy_orm_adapter import SQLAlchemyORMAdapter
from src.database.minimal_orm_adapter import MinimalORMAdapter
from src.database.config import Database


def initialize_orm(models: List[Type[Model]], database_url: str = None) -> ORMInterface:
    if database_url:
        db = Database(database_url)
        orm = SQLAlchemyORMAdapter(db)
    else:
        minimal_orm = MinimalORM()
        orm = MinimalORMAdapter(minimal_orm)

    for model in models:
        orm.register(model)

    return orm
