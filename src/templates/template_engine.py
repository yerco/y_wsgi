from abc import ABC, abstractmethod
from typing import Any, Dict


class TemplateEngine(ABC):
    @abstractmethod
    def render(self, template_dir: str, template_name: str, template_vars: Dict[str, Any]) -> str:
        pass
