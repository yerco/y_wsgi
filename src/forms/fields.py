from src.core.response import Response


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


class FormMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._fields = fields
        return new_class


class BaseForm(metaclass=FormMeta):
    def __init__(self, data):
        self._data = data
        self._errors = {}

    def is_valid(self):
        self._errors = {}
        for field_name, field in self._fields.items():
            try:
                field_value = self._data.get(field_name)
            except KeyError:
                field_value = None
            try:
                field.validate(field_value)
            except ValueError as e:
                self._errors[field_name] = str(e)
        return not self._errors

    @property
    def errors(self):
        return self._errors

    def render(self):
        # Render form as HTML (simplified)
        html = "<form method='post'>"
        for name, field in self._fields.items():
            html += f"<label>{field.label}</label>"
            html += f"<input type='text' name='{name}' required={field.required}>"
            if name in self._errors:
                html += f"<span>{self._errors[name]}</span>"
            html += "<br>"
        html += "<button type='submit'>Submit</button>"
        html += "</form>"
        return html

    def get_response(self, status: str = '200 OK') -> Response:
        return Response(
            status=status,
            body=[self.render().encode('utf-8')],
            headers=[('Content-Type', 'text/html')]
        )
