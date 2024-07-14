from urllib.parse import parse_qs
from typing import Dict, Any, Optional, Union


class Request:
    def __init__(self, environ: Dict[str, Any]) -> None:
        self.environ: Dict[str, Any] = environ

    @property
    def method(self) -> str:
        return self.environ['REQUEST_METHOD']

    @property
    def path(self) -> str:
        return self.environ['PATH_INFO']

    @property
    def query_string(self) -> str:
        return self.environ['QUERY_STRING']

    @property
    def headers(self) -> Dict[str, str]:
        headers = {}
        for key, value in self.environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].replace('_', '-').lower()] = value
            elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                # First letter of each work capitalized, e.g. 'content-type' becomes 'Content-Type'.
                headers[key.replace('_', '-').title()] = value

        return headers

    @property
    def body(self) -> bytes:
        try:
            length = int(self.environ.get('CONTENT_LENGTH', '0'))
        except (ValueError, TypeError):
            length = 0
        if length > 0:
            return self.environ['wsgi.input'].read(length)
        return b''

    @property
    def wsgi_version(self) -> Optional[tuple]:
        return self.environ.get('wsgi.version')

    @property
    def url_scheme(self) -> Optional[str]:
        return self.environ.get('wsgi.url_scheme')

    @property
    def input(self) -> Any:
        return self.environ.get('wsgi.input')

    @property
    def errors(self) -> Any:
        return self.environ.get('wsgi.errors')

    @property
    def multithread(self) -> Optional[bool]:
        return self.environ.get('wsgi.multithread')

    @property
    def multiprocess(self) -> Optional[bool]:
        return self.environ.get('wsgi.multiprocess')

    @property
    def run_once(self) -> Optional[bool]:
        return self.environ.get('wsgi.run_once')

    @property
    def forwarded_proto(self) -> Optional[str]:
        return self.environ.get('HTTP_X_FORWARDED_PROTO')

    @property
    def forwarded_host(self) -> Optional[str]:
        return self.environ.get('HTTP_X_FORWARDED_HOST')

    # These are part of the CGI (Common Gateway Interface) environment variables
    # that provide information about the server and client connection.
    @property
    def server_name(self) -> Optional[str]:
        return self.environ.get('SERVER_NAME')

    @property
    def server_port(self) -> Optional[str]:
        return self.environ.get('SERVER_PORT')

    @property
    def remote_addr(self) -> Optional[str]:
        return self.environ.get('REMOTE_ADDR')

    @property
    def remote_host(self) -> Optional[str]:
        return self.environ.get('REMOTE_HOST')

    # E.g. handling http://example.com/search?query=python&sort=asc&sort=desc&page=1
    # Returns {'query': ['python'], 'sort': ['asc', 'desc'], 'page': ['1']}
    def get_query_params(self) -> Dict[str, list[str]]:
        return parse_qs(self.query_string)

    def get_json(self) -> Optional[Union[Dict[str, Any], list]]:
        import json
        if 'application/json' in self.headers.get('Content-Type', ''):
            return json.loads(self.body)
        return None

    @property
    def all_headers(self) -> Dict[str, str]:
        headers = self.headers.copy()
        for key in self.environ:
            if key not in headers and not key.startswith('wsgi.') and not key.startswith('HTTP_'):
                headers[key.replace('_', '-').title()] = self.environ[key]
        return headers

    def extract_session_id(self) -> Optional[str]:
        cookies = self.environ.get('HTTP_COOKIE', '')
        session_id = None
        for cookie in cookies.split(';'):
            if cookie.strip().startswith('session_id='):
                session_id = cookie.split('=')[1].strip()
        return session_id
