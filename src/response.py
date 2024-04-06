class Response:
    def __init__(self, body=b'', status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or []

    def __iter__(self):
        # Convert the body to an iterable
        if isinstance(self.body, bytes):
            yield self.body
        else:
            for chunk in self.body:
                yield chunk
