from typing import List

from src.forms.validation_strategy import ValidationStrategy, RequiredValidationStrategy, StringValidationStrategy, \
    EmailValidationStrategy, IntegerValidationStrategy
from src.forms.composite import FieldComponent


class Field(FieldComponent):
    def __init__(self, label, required=False):
        super().__init__()
        self.label = label
        self.required = required
        self.strategies: List[ValidationStrategy] = []
        if self.required:
            self.strategies.append(RequiredValidationStrategy())

    def add_strategy(self, strategy: ValidationStrategy):
        self.strategies.append(strategy)

    def validate(self, value):
        for strategy in self.strategies:
            strategy.validate(value, self.label)
        return value

    def render(self):
        return f"<label>{self.label}</label><input type='text' required={self.required}>"


class CharField(Field):
    def __init__(self, label, required=False):
        super().__init__(label, required)
        self.add_strategy(StringValidationStrategy())


class EmailField(CharField):
    def __init__(self, label, required=False):
        super().__init__(label, required)
        self.add_strategy(EmailValidationStrategy())


class IntegerField(Field):
    def __init__(self, label, required=False):
        super().__init__(label, required)
        self.add_strategy(IntegerValidationStrategy())
