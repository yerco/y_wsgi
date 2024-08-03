from abc import ABC, abstractmethod
from typing import Dict, Any


# Component interface
class FieldComponent(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def render(self) -> str:
        pass


class CompositeField(FieldComponent):
    def __init__(self, label=None, action="", include_submit_button=False, csrf_token=None):
        self.label = label
        self.children = []
        self.action = action
        self.include_submit_button = include_submit_button  # Flag to control button rendering
        self.csrf_token = csrf_token

    def add_child(self, field: FieldComponent):
        self.children.append(field)

    def validate(self, data: Dict[str, Any]) -> None:
        for child in self.children:
            child.validate(data)

    def render(self) -> str:
        # Open form tag only if there's no parent form wrapping this composite
        if self.include_submit_button:
            html = f"<form method='post' action='{self.action}'>"
            # Include CSRF token as a hidden field
            if self.csrf_token:
                html += f"<input type='hidden' name='csrf_token' value='{self.csrf_token}'>"
        else:
            html = ""

        if self.label:
            html += f"<fieldset><legend>{self.label}</legend>"
        for child in self.children:
            html += child.render()
        if self.label:
            html += "</fieldset>"

        # Close form tag and add submit button if this is the top-level form
        if self.include_submit_button:
            html += "<button type='submit'>Submit</button>"
            html += "</form>"
        return html
