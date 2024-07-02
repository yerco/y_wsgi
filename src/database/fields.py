from typing import Any, Type


class Field:
    def __init__(self, default: Any = None) -> None:
        self.default = default

    # Automatically called when the class is created. It sets the attribute name on the field.
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    # Called to retrieve the attribute's value. If accessed from the class (not an instance),
    # it returns the descriptor itself.
    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    # Called to set the attribute's value.
    def __set__(self, instance: Any, value: Any) -> None:
        instance.__dict__[self.name] = value

    # Called to delete the attribute's value.
    def __delete__(self, instance: Any) -> None:
        del instance.__dict__[self.name]


class IntegerField(Field):
    pass


class CharField(Field):
    pass
