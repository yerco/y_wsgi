import re

from typing import Any, Dict

from src.templates.template_engine import TemplateEngine


class SimpleTemplateEngine(TemplateEngine):
    def __init__(self, template_dir: str):
        self.template_dir = template_dir

    def load_template(self, template_name: str) -> str:
        with open(f"{self.template_dir}/{template_name}", "r") as template_file:
            return template_file.read()

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        template = self.load_template(template_name)

        def replace_placeholder(match):
            key = match.group(1).strip()
            return str(context.get(key, f"{{{{ {key} }}}}"))  # Keep the placeholder if key not found

        pattern = re.compile(r"{{\s*(\w+)\s*}}")
        rendered_template = re.sub(pattern, replace_placeholder, template)
        return rendered_template
