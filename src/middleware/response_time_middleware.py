import time

from typing import Optional

from src.middleware.middleware import Middleware
from src.core.response import Response
from src.core.request_context import RequestContext
from src.signals.signal_manager import SignalManager


class ResponseTimeMiddleware(Middleware):
    def __init__(self, signal_manager: SignalManager):
        super().__init__()
        self.start_time = None
        self.signal_manager = signal_manager
        self.start_time = None

    def before_request(self, request_context: RequestContext) -> Optional[Response]:
        # To have it available at view level
        request_context.signal_manager = self.signal_manager
        self.signal_manager.connect('request_started', self.on_request_started)
        self.signal_manager.connect('request_finished', self.on_request_finished)
        return None

    def after_request(self, request_context: RequestContext, response: Response) -> Optional[Response]:
        self.signal_manager.disconnect('request_started', self.on_request_started)
        self.signal_manager.disconnect('request_finished', self.on_request_finished)
        return response

    def on_request_started(self, request_context):
        self.start_time = time.time()

    def on_request_finished(self, request_context, response):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            print(f"Request for {request_context.path} took {elapsed_time:.8f} seconds")
            response.set_header('X-Response-Time', f'{elapsed_time:.8f} seconds')
