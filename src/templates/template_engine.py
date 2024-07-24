from abc import ABC, abstractmethod
from typing import Any, Dict


class TemplateEngine(ABC):
    @abstractmethod
    def render(self, template: str, template_vars: Dict[str, Any]) -> str:
        pass
