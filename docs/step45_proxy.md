# Proxy Design Pattern

The Proxy Design Pattern is a structural design pattern that provides a surrogate or placeholder for another 
object to control access to it. 
It is useful in scenarios where you need to control access to an object, perform additional operations before
or after accessing the object, or manage resources more efficiently.

The `RequestProxy` class (at `user_app/modules/user_module/proxy/request_proxy.py`) is an implementation
of the Proxy design pattern it acts as an intermediary between the client and the actual view, adding
functionality like logging, request validation, and response modification without altering the core logic
of the original view.

How It Works
1. Logging the Request:
   - The proxy logs the details of each incoming request, including the HTTP method, path, and headers.
2. Request Validation:
   - The proxy checks for the presence of a specific header (`X-Required-Header`). If the header is missing, 
      it returns a 400 Bad Request response with a message indicating the request is invalid.
3. Forwarding the Request:
   - If the validation passes, the proxy forwards the request to the original view to handle the request 
     and generate a response.
4. Modifying the Response:
   - The proxy adds a custom header (X-Custom-Header) to the response before sending it back to the client.
5. Logging the Response:
   - The proxy logs the details of the outgoing response, including the status and headers.

To use it we define a view
```python
class ProxyExampleHandler(View):
    def get(self, request_context: RequestContext, params: Dict[str, Any] = None) -> Response:
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'text/plain')]
        return Response(status=status, headers=headers, body=[b'Proxy', b' ', b'Example', b' ', b'Handler'])
```
and then use the `RequestProxy` to wrap the view
```python
def register_routes(module):
    @module.route('/proxy-example')
    def proxy_example_handler(request_context: RequestContext) -> Response:
        original_view = ProxyExampleHandler()
        proxied_view = RequestProxy(original_view)
        return proxied_view.execute(request_context)
```

We could test it using 
```bash
curl -vvv -X GET http://localhost:8000/proxy-example \
-H "X-Required-Header: MyValue" \
-H "x-username: john" \
-H "x-password: password"
```