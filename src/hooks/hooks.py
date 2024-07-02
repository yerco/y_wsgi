from typing import Callable, List


class Hooks:
    def __init__(self):
        self.before_request_hooks: List[Callable] = []
        self.after_request_hooks: List[Callable] = []
        self.teardown_request_hooks: List[Callable] = []
        self.before_first_request_hooks: List[Callable] = []
        self.first_request = True

    def add_before_request(self, hook: Callable):
        self.before_request_hooks.append(hook)

    def add_after_request(self, hook: Callable):
        self.after_request_hooks.append(hook)

    def add_teardown_request(self, hook: Callable):
        self.teardown_request_hooks.append(hook)

    def add_before_first_request(self, hook: Callable):
        self.before_first_request_hooks.append(hook)
