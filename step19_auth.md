# Authentication

![Screenshot 2024-07-08 at 5.10.11 PM.png](..%2F..%2F..%2F..%2FLibrary%2FCloudStorage%2FOneDrive-SoftServe%2CInc%2FDesktop%2FScreenshot%202024-07-08%20at%205.10.11%E2%80%AFPM.png)

```python
from typing import Optional

from abc import ABC, abstractmethod

from src.core.request import Request
from src.core.response import Response
from src.models.base_user import BaseUser


class AuthState(ABC):
    @abstractmethod
    def handle_request(self, context: 'AuthContext', request: Request) -> Response:
        pass


class UnauthenticatedState(AuthState):
    def handle_request(self, context: 'AuthContext', request: Request) -> Response:
        return Response(status='401 Unauthorized', body=[b'Unauthorized'])


class AuthenticatedState(AuthState):
    def handle_request(self, context: 'AuthContext', request: Request) -> Response:
        return Response(status="200 OK", body=[f"Welcome, {context.user.username}".encode()])


# E.g. account is temporarily locked due to multiple failed login attempts
class LockedState(AuthState):
    def handle_request(self, context: 'AuthContext', request: Request) -> Response:
        return Response(status='403 Forbidden', body=[b'Account Locked'])


class AuthContext:
    def __init__(self):
        self.state: AuthState = UnauthenticatedState()
        self.user: Optional[BaseUser] = None
        self.failed_attempts: int = 0

    # set state
    def change_state(self, state: AuthState):
        self.state = state

    def authenticate(self, user: BaseUser):
        self.user = user
        self.failed_attempts = 0
        self.change_state(AuthenticatedState())

    def lock(self):
        self.change_state(LockedState())

    def handle_request(self, request: Request) -> Response:
        return self.state.handle_request(self, request)
```
We then integrate it with the authentication middleware at src/middleware/authentication_middleware.py

We need to handle how to deal with the public routes to make it easier to set them
