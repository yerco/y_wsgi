import hmac
import hashlib

from typing import List

from src.session.session import Session
from src.session.session_memento import SessionMemento
from src.session.session_caretaker import SessionCaretaker
from src.config import config


class SessionStore:
    def __init__(self):
        self._sessions: List[Session] = []
        self._caretaker = SessionCaretaker()
        self._caretaker.save_memento(self.create_memento())
        self.secret_key = config.SECRET_KEY

    def get_session(self) -> Session:
        if self._sessions:
            return self._sessions[-1]
        raise IndexError("No sessions available")

    def write(self, session: Session) -> None:
        # Security
        session.id = self._sign_session_id(session.id)
        self._sessions.append(session)
        self._caretaker.save_memento(self.create_memento())

    def create_memento(self) -> SessionMemento:
        # shallow copy
        return SessionMemento(self._sessions.copy())

    def get_from_memento(self, memento: SessionMemento) -> List[Session]:
        if memento:
            return memento.get_state()
        return self._sessions

    def undo(self) -> None:
        if len(self._caretaker.undo_mementos) > 1:
            self._sessions = self.get_from_memento(self._caretaker.undo())

    def redo(self) -> None:
        self._sessions = self.get_from_memento(self._caretaker.redo())

    def _sign_session_id(self, session_id: str) -> str:
        return hmac.new(
            self.secret_key.encode(),
            msg=session_id.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

    def __len__(self):
        return len(self._sessions)
