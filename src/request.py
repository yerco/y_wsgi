class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def path(self):
        return self.environ['PATH_INFO']

    @property
    def query_string(self):
        return self.environ['QUERY_STRING']

    @property
    def headers(self):
        return self.environ.items()
