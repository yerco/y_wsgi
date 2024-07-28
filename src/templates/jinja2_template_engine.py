from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader

from src.templates.template_engine import TemplateEngine


class Jinja2TemplateEngine(TemplateEngine):
    def render(self, template_dir: str, template_name: str, template_vars: Dict[str, Any]) -> str:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template.render(template_vars)
