import hashlib
import hmac


class CSRFToken:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.token = None

    def generate_csrf_token(self, session_id: str) -> str:
        self.token = hmac.new(self.secret_key.encode(), session_id.encode(), hashlib.sha256).hexdigest()
        return self.token

    def is_valid_csrf_token(self, token: str, session_id: str) -> bool:
        return token == self.generate_csrf_token(session_id)
