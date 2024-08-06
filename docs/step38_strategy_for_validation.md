# Current scenario:
Up to this point we have all the validation logic tightly coupled with the `Field` classes which
might not be the best approach, especially if you want to make the validation logic more flexible and reusable.
```python
# src/forms/fields.py
class Field:
    def __init__(self, label, required=False):
        self.label = label
        self.required = required

    def validate(self, value):
        if self.required and not value:
            raise ValueError(f"{self.label} is required")
        return value


class CharField(Field):
    def validate(self, value):
        value = super().validate(value)
        if not isinstance(value, str):
            raise ValueError(f"{self.label} must be a string")
        return value


class EmailField(CharField):
    def validate(self, value):
        value = super().validate(value)
        if "@" not in value:
            raise ValueError(f"{self.label} must be a valid email address")
        return value


class IntegerField(Field):
    def validate(self, value):
        value = super().validate(value)

        # Attempt to convert the value to an integer
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError(f"{self.label} must be an integer")

        return value
```

Modifying `src/forms/fields.py` while using `src/forms/validation_strategy.py` makes `Field` classes 
now more flexible and adhere to the Single Responsibility Principle better.
