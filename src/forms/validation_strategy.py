from abc import ABC, abstractmethod


class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, value, label: str):
        pass


class RequiredValidationStrategy(ValidationStrategy):
    def validate(self, value, label: str):
        if not value:
            raise ValueError(f"{label} is required")


class StringValidationStrategy(ValidationStrategy):
    def validate(self, value, label: str):
        if not isinstance(value, str):
            raise ValueError(f"{label} must be a string")


class EmailValidationStrategy(ValidationStrategy):
    def validate(self, value, label: str):
        if "@" not in value:
            raise ValueError(f"{label} must be a valid email address")


class IntegerValidationStrategy(ValidationStrategy):
    def validate(self, value, label: str):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"{label} must be an integer")
