import os


class TemplateScanner:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def scan(self):
        template_directory = {}
        for root, dirs, files in os.walk(self.base_dir):
            if 'templates' in dirs:
                module_name = os.path.basename(root)
                template_path = os.path.join(root, 'templates')
                template_directory[module_name] = template_path
                return template_directory
        raise FileNotFoundError("No templates directory found.")
