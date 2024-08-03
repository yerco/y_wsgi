from src.forms.fields import CharField
from src.forms.composite import CompositeField


class AddressForm(CompositeField):
    def __init__(self):
        super().__init__("Address")
        self.add_child(CharField("Street", required=True))
        self.add_child(CharField("City", required=True))
        self.add_child(CharField("Zip Code", required=True))


class UserForm(CompositeField):
    def __init__(self, action="", include_submit_button=True, csrf_token=None):
        super().__init__("User Information", action=action, include_submit_button=include_submit_button,
                         csrf_token=csrf_token)
        self.add_child(CharField("First Name", required=True))
        self.add_child(CharField("Last Name", required=True))
        self.add_child(AddressForm())
