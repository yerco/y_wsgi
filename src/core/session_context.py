from typing import Optional

from src.session.session import Session


class SessionContext:
    def __init__(self, session: Optional[Session] = None):
        self._session = session

    @property
    def session(self) -> Optional[Session]:
        return self._session

    @session.setter
    def session(self, session: Session) -> None:
        self._session = session

    def is_valid(self) -> bool:
        return self._session is not None and not self._session.is_expired()

    def regenerate_id(self) -> None:
        self._session.regenerate_id()

    @property
    def created_at(self) -> float:
        return self._session.created_at
