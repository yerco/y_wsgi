# Cache Decorator
The `cache_view` (ast `src/cache/cache_decorator.py`) decorator is used to cache the response of a view function, 
enabling quicker subsequent responses  for the same request. This is particularly useful for pages that 
do not change frequently. The decorator works by saving the response in an in-memory cache and using it
for subsequent requests until the cache expires.

## How It Works
1. Caching Mechanism:
   - The decorator uses the SimpleCache class to store and retrieve cached responses based on the request path.
   - When a request is made, the decorator checks if there is a cached response for that path.
     If found, it returns the cached response.
   - If no cached response is found, the original view function is called, and its response is 
     cached for future requests.
2. Conditional Requests:
   - The decorator also supports conditional GET requests using the `If-None-Match` and `If-Modified-Since` headers.
   - If a cached response is found and matches these headers, a 304 Not Modified response is returned, 
     indicating that the cached content is still valid and hasn’t changed.
3. Caching Headers:
   - `Cache-Control`: Specifies the maximum time (in seconds) the response is considered fresh. 
   This is set based on the timeout value passed to the decorator.
   - `Last-Modified`: Indicates the last time the content was modified, set to the current time when 
   the response is first cached.
   - `ETag`: A unique identifier for a specific version of the resource, generated using an MD5 hash 
   of the response body.

## Example Usage
To use the cache_view decorator, simply apply it to any view function you wish to cache:
```python
@module.route('/user_app_page', methods=['GET'])
@cache_view(timeout=300)  # Cache this view for 5 minutes
def user_app_page(request_context: RequestContext):
    template_vars = {
        'title': 'This is the user_app',
        'message': 'We are in the module user_module',
        'nonce': request_context.request.environ.get('nonce')
    }

    current_app = request_context.current_app
    rendered_template = current_app.render_template('user_app_page.html', template_vars)
    return Response(status='200 OK', body=[rendered_template.encode('utf-8')])
```

## Key Headers Managed by the Decorator
- `Cache-Control: max-age=<timeout>` specifies how long the response can be cached.
- `Last-Modified`: The timestamp when the content was last generated.
- `ETag`: A unique identifier for the content, based on its MD5 hash.

## Considerations
- Performance: The use of the cache can significantly improve performance for frequently requested, static content.
- Memory Usage: The cache is stored in memory, so be mindful of the cache size, especially with large responses 
  or a high number of unique requests.
- Consistency: Ensure that the content being cached is relatively static or set an appropriate timeout value to
  prevent serving outdated content.