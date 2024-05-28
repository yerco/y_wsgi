from typing import Callable, Dict, Any, List, Tuple, Iterable

from src.request import Request
from src.response import Response

"""
A string (str) for the status.
A list of tuples (List[Tuple[str, str]]) for the response headers.
An optional third argument of any type (Any) for exception information.
"""
StartResponseType = Callable[[str, List[Tuple[str, str]], Any], None]


def application(environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
    request = Request(environ)
    print('request method: ', request.method)
    print('request.path', request.path)
    print('request.headers', request.headers)
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain')]  # HTTP Headers
    # byte strings for the response body to handle any kind of content (images, videos, or binary data)
    response = Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World'])
    status = response.status
    headers = response.headers
    start_response(status, headers)

    # An iterable yielding byte strings
    return response
