import sys


class TemporarySysPath:
    def __init__(self, path):
        self.path = path
        self.original_sys_path = sys.path.copy()

    def __enter__(self):
        if self.path and self.path not in sys.path:
            sys.path.insert(0, self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        sys.path = self.original_sys_path
