from typing import Any, Dict, Type

from src.database.fields import Field


class ModelMeta(type):
    def __new__(cls: Type['ModelMeta'], name: str, bases: tuple, dct: dict) -> 'ModelMeta':
        # Collect field definitions
        fields = {key: value for key, value in dct.items() if isinstance(value, Field)}
        # Remove field definitions from the class dictionary
        for field_name in fields:
            dct.pop(field_name)
        # Store fields in _fields attribute
        dct['_fields'] = fields
        return super().__new__(cls, name, bases, dct)


class Model(metaclass=ModelMeta):
    _fields: Dict[str, Field] = {}  # This helps the IDE understand _fields is an attribute

    def __init__(self, **kwargs: Any) -> None:
        for field_name, field_value in self._fields.items():
            setattr(self, field_name, kwargs.get(field_name, field_value.default))

    def __repr__(self) -> str:
        field_values = ", ".join(f"{name}={getattr(self, name)!r}" for name in self._fields)
        return f"<{self.__class__.__name__}({field_values})>"
