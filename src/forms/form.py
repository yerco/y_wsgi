from src.core.response import Response
from src.forms.fields import Field
from src.core.request_context import RequestContext
from src.forms.form_mediator import FormMediator


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
    def __init__(self, data, request_context: RequestContext):
        self._data = data
        self._errors = {}
        self.request_context = request_context
        self.mediator: FormMediator = request_context.app_context.get_form_mediator()
        self.csrf_token = None
        if self.mediator:
            self.mediator.register_form(self)
            # Notify mediator to update CSRF token after registration
            self.mediator.notify(self, 'set_csrf')

    @property
    def data(self):
        return self._data

    def is_valid(self) -> bool:
        self._errors = {}

        if self.mediator:
            self.mediator.notify(self, 'csrf_check')

        for field_name, field in self._fields.items():
            try:
                field_value = self._data.get(field_name)
            except KeyError:
                field_value = None
            try:
                field.validate(field_value)
            except ValueError as e:
                self._errors[field_name] = str(e)
        return not self._errors  # True if no errors

    @property
    def errors(self):
        return self._errors

    def render(self):
        # Render form as HTML (simplified)
        html = "<form method='post'>"
        html += f"<input type='hidden' name='csrf_token' value='{self.csrf_token}'>"
        for name, field in self._fields.items():
            html += f"<label>{field.label}</label>"
            html += f"<input type='text' name='{name}' required={field.required}>"
            if name in self._errors:
                html += f"<span>{self._errors[name]}</span>"
            html += "<br>"
        html += "<button type='submit'>Submit</button>"
        html += "</form>"
        return html

    def render_response(self, status: str = '200 OK') -> Response:
        return Response(
            status=status,
            body=[self.render().encode('utf-8')],
            headers=[('Content-Type', 'text/html')]
        )

    def embed_csrf_token(self, csrf_token: str):
        self.csrf_token = csrf_token
