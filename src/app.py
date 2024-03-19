def application(environ, start_response):
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain')]  # HTTP Headers
    start_response(status, headers)

    # An iterable yielding byte strings
    # - enables response to be streamed
    # - app can produce response parts on the fly
    # - byte strings for the response body to handle any kind of content
    #   (images, videos, or binary data)
    return [b"Hello WSGI World"]
