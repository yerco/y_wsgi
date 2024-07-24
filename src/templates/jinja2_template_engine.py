from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader

from src.templates.template_engine import TemplateEngine


class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template: str, template_vars: Dict[str, Any]) -> str:
        template = self.env.get_template(template)
        return template.render(template_vars)
