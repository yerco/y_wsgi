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
