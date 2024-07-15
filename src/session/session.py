import uuid
import time
from typing import Any, Optional

from src.config import config


class Session:
    def __init__(self, user_id: str, expiry_time: Optional[float] = None, ip_address: Optional[str] = None,
                 user_agent: Optional[str] = None, csrf_token: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.signed_id = None
        self.user_id = user_id
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.expiry_time = expiry_time or self.created_at + config.SESSION_EXPIRY
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.csrf_token = csrf_token
        self.data = {}

    def is_expired(self) -> bool:
        return time.time() > self.expiry_time

    def update_last_accessed(self) -> None:
        self.last_accessed = time.time()

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.last_accessed = time.time()

    def get(self, key: str) -> Any:
        self.last_accessed = time.time()
        return self.data.get(key)

    def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]
            self.last_accessed = time.time()

    def clear(self) -> None:
        self.data = {}
        self.last_accessed = time.time()

    def regenerate_id(self):
        self.id = str(uuid.uuid4())
        self.signed_id = None  # This will be re-signed when written to the store

    def __repr__(self):
        return (f"Session(id={self.id}, signed_id={self.signed_id} , user_id={self.user_id}, "
                f"created_at={self.created_at}, "
                f"last_accessed={self.last_accessed}, expiry_time={self.expiry_time}, "
                f"ip_address={self.ip_address}, user_agent={self.user_agent}, "
                f"csrf_token={self.csrf_token}, data={self.data})")
