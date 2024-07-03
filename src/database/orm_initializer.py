from typing import Union
from src.database.orm_interface import ORMInterface
from src.database.models import User
from src.database.orm import ORM as MinimalORM


try:
    from src.database.sqlalchemy_orm_adapter import SQLAlchemyORMAdapter
    USE_SQLALCHEMY = True
except ImportError:
    from src.database.minimal_orm_adapter import MinimalORMAdapter
    USE_SQLALCHEMY = False


def initialize_orm() -> ORMInterface:
    if USE_SQLALCHEMY:
        return SQLAlchemyORMAdapter()
    else:
        minimal_orm = MinimalORM()
        minimal_orm.register(User)
        return MinimalORMAdapter(minimal_orm)
