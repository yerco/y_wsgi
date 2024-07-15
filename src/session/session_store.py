import copy
import hmac
import hashlib

from typing import List, Optional

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

    def get_session_by_id(self, session_id: str) -> Optional[Session]:
        signed_session_id = self._sign_session_id(session_id)
        # Here, we'll check the current state from the memento pattern
        current_sessions = self._caretaker.get_current_memento().get_state()
        for session in current_sessions:
            if session.id == session_id and session.signed_id == signed_session_id and not session.is_expired():
                return session
        return None

    def write(self, session: Session) -> None:
        # Security
        session.signed_id = self._sign_session_id(session.id)
        # Clone the session to create a new state
        new_session = copy.deepcopy(session)

        for i, existing_session in enumerate(self._sessions):
            if existing_session.id == session.id:
                self._sessions[i] = new_session
                self._caretaker.save_memento(self.create_memento())
                return
        self._sessions.append(session)
        self._caretaker.save_memento(self.create_memento())

    def create_memento(self) -> SessionMemento:
        # deep copy better
        return SessionMemento(copy.deepcopy(self._sessions))

    def get_from_memento(self, memento: SessionMemento) -> List[Session]:
        if memento:
            return memento.get_state()
        return self._sessions

    def undo(self) -> None:
        previous_state = self._caretaker.undo()
        if previous_state:
            self._sessions = previous_state.get_state()  # Restore the previous state

    def redo(self) -> None:
        next_state = self._caretaker.redo()
        if next_state:
            self._sessions = next_state.get_state()

    def _sign_session_id(self, session_id: str) -> str:
        return hmac.new(
            self.secret_key.encode(),
            msg=session_id.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

    def __len__(self):
        return len(self._sessions)
