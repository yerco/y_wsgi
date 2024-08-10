from typing import Any

from src.core.view import View
from src.core.request_context import RequestContext
from src.core.response import Response
from src.http.http_response_builder import HTTPResponseBuilder


class RequestProxy(View):
    def __init__(self, view: View):
        super().__init__()
        self._view = view

    def execute(self, request_context: RequestContext, **params: Any) -> Response:
        # Step 1: Log the incoming request details
        self.log_request(request_context)

        # Step 2: Validate the request (e.g., check for a required header)
        if not self.validate_request(request_context):
            return self.request_invalid_response()

        # Step 3: Forward the request to the actual view
        response = self._view.execute(request_context, **params)

        # Step 4: Modify the response if necessary
        modified_response = self.modify_response(response)

        # Step 5: Log the outgoing response details
        self.log_response(modified_response)

        return modified_response

    def log_request(self, request_context: RequestContext):
        print(
            f"Logging Request: Method={request_context.method}, Path={request_context.path}, "
            f"Headers={request_context.headers}"
        )

    def validate_request(self, request_context: RequestContext) -> bool:
        # Example validation: Ensure a specific header is present
        required_header = "X-Required-Header".lower()
        if required_header not in request_context.headers:
            print(f"Validation Failed: Missing header {required_header}")
            return False
        return True

    def request_invalid_response(self) -> Response:
        response = (HTTPResponseBuilder()
                    .set_status(400)
                    .set_body("Request is invalid due to missing or incorrect headers.")
                    .build())
        return response

    def modify_response(self, response: Response) -> Response:
        # Example modification: Add a custom header to the response
        response.headers.append(('X-Custom-Header', 'CustomValue'))
        return response

    def log_response(self, response: Response):
        print(f"Logging Response: Status={response.status}, Headers={response.headers}")
