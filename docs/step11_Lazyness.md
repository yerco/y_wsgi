# Lazy Loading
Lazy loading is a design pattern commonly used to defer initialization of an object until it is actually needed. 
This can improve the efficiency and performance of a system by:

- Reducing Memory Usage: By not initializing objects until necessary, memory usage is minimized.
- Improving Load Times: Especially in web applications, lazy loading can defer the loading of certain components until 
they are actually needed by the user, resulting in faster initial load times.
- Enhanced Performance: Deferred initialization can lead to better overall performance, particularly in 
resource-constrained environments.

https://www.geeksforgeeks.org/what-is-lazy-loading/
For example, say a user requests for the logo of GeeksForGeeks from a search engine. The entire web page, 
populated with the requested content, is loaded. Now if the user opens the first image and is satisfied with it, 
he will probably close the web page thus, rest of the images so loaded will be left unseen. 
This will result in the wastage of the resources so consumed in the bulk load of that page. 
Thus, the solution to this is Lazy Loading.

## Real-world Analogy
Consider a restaurant kitchen:

### Without Lazy Loading (Eager Loading):
The kitchen prepares every possible dish on the menu at the start of the day.
This means that when a customer orders any dish, it is ready to be served immediately.
However, preparing all dishes in advance takes a lot of time and resources, 
and many dishes might go to waste if not ordered.

### With Lazy Loading:
The kitchen prepares dishes only when customers order them.
The first customer who orders a particular dish has to wait while it is prepared.
Once a dish has been prepared, subsequent orders for the same dish can be served more quickly, 
as the preparation steps have already been completed.

## What happens in our nano-framework
Sequence Explanation

1. Initialization:
   - In `main.py`, we initialize our `App` instance. As the `main.py` file is parsed, it encounters the handler
   functions (FBVs) or classes (CBVs). These handlers are registered with the App instance 
   via the `@app.route()` decorator.
2. Lazy Loading Handlers:
   - When we decorate a handler function or class with @app.route(), the route method in App is called:
     ```python
     def route(self, path: str) -> Callable[[HandlerType], HandlerType]:
         def wrapper(handler: HandlerType) -> HandlerType:
             self.router.add_route(path, handler)
             return handler
         return wrapper
     ```
   - This method registers the route with the `Router` and uses the `LazyRoute` class to ensure that the handler 
   is lazily loaded.
   - The `add_route` method of the Router class adds the route with a `handler_factory`, which is a `lambda` function
   that returns the handler.
3. First Request to Endpoint:
   - When a request is made to an endpoint for the first time, the App instance's `__call__` method processes
   the request:
    ```python
    handler, params = self.router.match(request.path)
    if handler:
        if isinstance(handler, type) and issubclass(handler, View):
            handler_instance = handler()
            response = handler_instance(request, **params)
        elif callable(handler):
            response = handler(request, **params)
        else:
            response = Response(status='500 Internal Server Error', headers=[('Content-type', 'text/plain')],
                                body=[b'Internal Server Error'])
    else:
        response = Response(status='404 Not Found', headers=[('Content-type', 'text/plain')], body=[b'Not Found'])
   ```
   - The `match` method of the `Router` class finds the appropriate `LazyRoute`.
   - The `handler` **property** of the `LazyRoute` class is accessed for the first time, triggering the instantiation
   of the handler:
   ```python
    @property
    def handler(self) -> HandlerType:
        if self._handler is None:
            print(f"Instantiating handler for path: {self.path}")
            self._handler = self._handler_factory()
        return self._handler
   ```
   - The handler is then executed with the request and any extracted parameters.
4. Subsequent Requests to Endpoint:
   - For subsequent requests to the same endpoint, the `handler` property of the LazyRoute class returns 
   the already instantiated handler without re-instantiating it: 
   ```python
    @property
    def handler(self) -> HandlerType:
        if self._handler is None:
            print(f"Instantiating handler for path: {self.path}")
            self._handler = self._handler_factory()
        return self._handler
   ```
   - The `App` class processes the request as usual, and the handler is executed immediately:
   ```python
    handler, params = self.router.match(request.path)
    print(f"Matched handler: {handler}, Params: {params}")
    if handler:
        if isinstance(handler, type) and issubclass(handler, View):
            handler_instance = handler()
            response = handler_instance(request, **params)
        elif callable(handler):
            response = handler(request, **params)
        else:
            response = Response(status='500 Internal Server Error', headers=[('Content-type', 'text/plain')],
                                body=[b'Internal Server Error'])
    else:
        response = Response(status='404 Not Found', headers=[('Content-type', 'text/plain')], body=[b'Not Found'])
   ```
### Summary
1. Initialization: The application is initialized, and handlers are registered via decorators.
2. Lazy Loading Handlers: Handlers are registered with a factory function to ensure they are lazily loaded.
3. First Request: The first request to an endpoint triggers the instantiation of the handler.
4. Subsequent Requests: Subsequent requests use the already instantiated handler, providing a performance boost.

This sequence ensures efficient resource usage by only creating handlers when they are needed and reusing them for
subsequent requests.

## Key question: how come `__call__` is executed again each time a request arrives?
The `__call__` method in the `App` class is executed every time a request arrives because the `App` instance itself is 
designed to act as the WSGI application.

### Explanation:
In WSGI (Web Server Gateway Interface), the web server passes the request to the application object, which is 
typically an instance of a class that implements the `__call__` method. 
This method is executed for each incoming HTTP request.

### WSGI Flow
1. Application Initialization:
   - When you start the web server (e.g., Gunicorn), it loads the App instance as the WSGI application.
   - The App instance is created and set up with routes, middleware, and hooks.
2. Request Handling:
   - Each time an HTTP request is received, the web server calls the `__call__` method of the App instance.
   - The `__call__` method is responsible for processing the request and returning the response.

### Example of the Flow:
Application Initialization (Run Once)
In `main.py`:
```python
from src.app import App

app = App()

@app.route('/')
def home_handler(request):
    return Response(status='200 OK', body=[b'Welcome to the home page!'])

# When running with a WSGI server like Gunicorn, you would use:
# gunicorn main:app --reload
```

#### Request Handling (Run for Each Request)
When a request arrives at the server, the WSGI server calls the `__call__` method of the `app` instance:
```python
# src/app.py
class App:
    # ... other methods ...

    def __call__(self, environ: Dict[str, Any], start_response: StartResponseType) -> Iterable[bytes]:
        request = Request(environ)
        handler, params = self.router.match(request.path)

        if handler:
            response = handler(request, **params)
        else:
            response = Response(status='404 Not Found', body=[b'Not Found'])

        start_response(response.status, response.headers)
        return response.body
```
1. Incoming Request: The WSGI server receives an HTTP request and calls `app.__call__(environ, start_response)`.
2. Request Processing: The `__call__` method processes the request:
   - Creates a Request object from environ.
   - Matches the request path to a handler using the Router.
   - Executes the matched handler.
3. Response Generation: The handler generates a `Response` object.
4. Response Sending: The `__call__` method sends the response back to the client using `start_response`.

### Summary
- The `App` instance is created once when the server starts.
- The `__call__` method is executed each time a request arrives.
- This method processes the request and returns the response, ensuring that each request is handled independently.

- By following the WSGI protocol, the application ensures efficient and scalable request handling, 
allowing the same `App` instance to handle multiple requests concurrently.

In a way, we can think of the web server (e.g., Gunicorn) treating the App instance as a singleton.