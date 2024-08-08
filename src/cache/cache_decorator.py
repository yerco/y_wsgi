from functools import wraps
from datetime import datetime
from hashlib import md5

from src.cache.simple_cache import SimpleCache
from src.core.request_context import RequestContext
from src.core.response import Response


def cache_view(timeout=None):
    cache = SimpleCache(timeout=timeout)

    def decorator(func):
        @wraps(func)
        def wrapped(request_context: RequestContext, *args, **kwargs):
            # Save the current module directory
            current_module_dir = request_context.current_app.context.get_current_module_dir()

            cache_key = f"{request_context.path}"
            cached_response = cache.get(cache_key)

            if cached_response:
                # print("Cache hit, returning cached response.")
                # Restore the module directory for cached responses
                request_context.current_app.context.set_current_module_dir(current_module_dir)

                # Check for conditional headers (If-None-Match, If-Modified-Since)
                if 'If-None-Match' in request_context.request.headers:
                    if request_context.request.headers['If-None-Match'] == cached_response.headers_dict.get('ETag'):
                        return Response(status='304 Not Modified', headers=cached_response.headers_dict)

                if 'If-Modified-Since' in request_context.request.headers:
                    last_modified = cached_response.headers_dict.get('Last-Modified')
                    if last_modified and request_context.request.headers['If-Modified-Since'] == last_modified:
                        return Response(status='304 Not Modified', headers=cached_response.headers_dict)

                return cached_response

            # print("Cache miss, calling the original view function.")
            # Call the original view function
            response: Response = func(request_context, *args, **kwargs)

            # Generate and set caching headers
            response.set_header("Cache-Control", f"max-age={timeout}")

            # Set Last-Modified header
            last_modified = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            response.set_header("Last-Modified", last_modified)

            # Generate ETag based on the response body
            data = response.body[0]
            if isinstance(data, int):
                data = str(data).encode('utf-8')  # Convert int to str and then encode to bytes
            etag = md5(data).hexdigest()
            response.set_header("ETag", etag)

            # Restore the module directory after the view function is executed
            request_context.current_app.context.set_current_module_dir(current_module_dir)

            cache.set(cache_key, response)
            # print("Response cached.")
            return response
        return wrapped
    return decorator
