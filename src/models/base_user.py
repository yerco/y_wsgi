from src.database.fields import CharField, IntegerField
from src.database.models import Model


class BaseUser(Model):
    id = IntegerField()
    username = CharField()
    password = CharField()  # In a real-world scenario, this should be hashed.

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username=username, password=password)

    def check_password(self, password: str) -> bool:
        return self.password == password
