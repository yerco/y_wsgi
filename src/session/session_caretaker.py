from typing import List, Optional

from src.session.session_memento import SessionMemento


class SessionCaretaker:
    def __init__(self):
        self._undo_mementos: List[SessionMemento] = []
        self._redo_mementos: List[SessionMemento] = []

    def save_memento(self, memento: SessionMemento) -> None:
        self._undo_mementos.append(memento)
        self._redo_mementos.clear()

    def undo(self) -> Optional[SessionMemento]:
        if len(self._undo_mementos) > 1:
            self._redo_mementos.append(self._undo_mementos.pop())
            return self._undo_mementos[-1]
        elif self._undo_mementos:
            return self._undo_mementos[0]
        return None

    def redo(self) -> Optional[SessionMemento]:
        if self._redo_mementos:
            memento = self._redo_mementos.pop()
            self._undo_mementos.append(memento)
            return memento
        return None

    def get_current_memento(self) -> Optional[SessionMemento]:
        if self._undo_mementos:
            return self._undo_mementos[-1]
        return None

    @property
    def undo_mementos(self):
        return self._undo_mementos
