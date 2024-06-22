from typing import Callable, Dict, Any, List, Tuple, Iterable

from src.request import Request
from src.response import Response
from src.router import Router

"""
A string (str) for the status.
A list of tuples (List[Tuple[str, str]]) for the response headers.
An optional third argument of any type (Any) for exception information.
"""
StartResponseType = Callable[[str, List[Tuple[str, str]], Any], None]

router = Router()


def hello_world_handler(request: Request) -> Response:
    # Define the status and headers explicitly
    status: str = '200 OK'  # HTTP Status
    headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]  # HTTP Headers
    # byte strings for the response body to handle any kind of content (images, videos, or binary data)
    return Response(status=status, headers=headers, body=[b'Hello', b' ', b'YWSGI', b' ', b'World'])


router.add_route('/', hello_world_handler)


def application(environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
    request = Request(environ)
    print('request method: ', request.method)
    print('request.path', request.path)
    print('request.headers', request.headers)

    handler = router.match(request.path)
    if handler:
        response = handler(request)
    else:
        response = Response(status='404 Not Found', headers=[('Content-type', 'text/plain')], body=[b'Not Found'])

    response_status: str = response.status
    response_headers: List[Tuple[str, str]] = response.headers

    # Ensure that the response status and headers are correctly typed
    assert isinstance(response_status, str), f"Expected str, got {type(response_status).__name__}"
    assert isinstance(response_headers, list) and all(isinstance(header, tuple) for header in response_headers), \
        "Headers should be a list of tuples"

    start_response(response_status, response_headers, None)

    # An iterable yielding byte strings
    return response
