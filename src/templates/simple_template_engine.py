import re
import os

from typing import Any, Dict

from src.templates.template_engine import TemplateEngine


class SimpleTemplateEngine(TemplateEngine):
    def render(self, template_dir: str, template_name: str, template_vars: Dict[str, Any]) -> str:
        template_path = os.path.join(template_dir, template_name)
        with open(template_path, "r") as template_file:
            template = template_file.read()

        def replace_placeholder(match):
            key = match.group(1).strip()
            return str(template_vars.get(key, f"{{{{ {key} }}}}"))  # Keep the placeholder if key not found

        pattern = re.compile(r"{{\s*(\w+)\s*}}")
        rendered_template = re.sub(pattern, replace_placeholder, template)
        return rendered_template
