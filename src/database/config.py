from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._Base = declarative_base()

    @property
    def SessionLocal(self):
        return self._SessionLocal

    @property
    def Base(self):
        return self._Base

    def create_tables(self):
        self._Base.metadata.create_all(bind=self.engine)
