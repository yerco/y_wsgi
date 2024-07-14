from typing import List

from src.session.session import Session


class SessionMemento:
    def __init__(self, state: List[Session]):
        self._state = state

    def get_state(self) -> List[Session]:
        return self._state
