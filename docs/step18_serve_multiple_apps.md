# Serve Multiple Applications

At this point we can serve just one app (our apps contain modules). We can extend our framework
To serve multiple applications within a single WSGI server setup, we need a way to dispatch requests 
to the correct application based on the request URL or other criteria. 
This can be done using a WSGI middleware that acts as a router for different applications.

## Dispatcher
The Dispatcher class we implemented is responsible for directing incoming requests to the appropriate 
application based on the URL path prefix. This allows you to run multiple applications within a single server
process, each handling different parts of the URL space.

### Dispatcher Implementation
Here's the Dispatcher class we used:
```python
from typing import Callable, Dict
from src.core.response import Response


class Dispatcher:
    def __init__(self):
        self.apps: Dict[str, Callable] = {}

    def add_app(self, path_prefix: str, app: Callable):
        # Ensure the root application is always checked last to handle overlapping paths
        if path_prefix == '/':
            self.apps[path_prefix] = app
        else:
            self.apps = {path_prefix: app, **self.apps}

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for prefix, app in self.apps.items():
            if path.startswith(prefix):
                return app(environ, start_response)
        response = Response(status='404 Not Found', body=[b'Not Found'])
        return response
```
Explanation
- Initialization: The `Dispatcher` class maintains a dictionary of applications, where each application is associated 
  with a path prefix.
- Adding Applications: The `add_app` method allows adding applications with specific path prefixes. 
  Applications with root paths (i.e., /) are added last to ensure they don't override more specific paths.
- Request Handling: The `__call__` method is the entry point for WSGI requests. 
  It checks the request path against the registered path prefixes and delegates the request to the 
  appropriate application. If no matching application is found, it returns a 404 Not Found response.

## Front Controller Pattern
The Front Controller pattern is used to provide a centralized entry point for handling requests. 
In our framework, the `Dispatcher` class serves as the front controller:
- Centralized Request Handling: The dispatcher handles all incoming requests and decides 
  which application should process the request based on the URL path.
- Single Entry Point: The Dispatcher class ensures that all requests go through a single point, 
  making it easier to manage cross-cutting concerns like logging, authentication, and error handling.

```python
# src/dispatcher.py
from typing import Callable, Dict
from src.core.response import Response

class Dispatcher:
    def __init__(self):
        self.apps: Dict[str, Callable] = {}

    def add_app(self, path_prefix: str, app: Callable):
        self.apps[path_prefix] = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for path_prefix, app in self.apps.items():
            if path.startswith(path_prefix):
                environ['SCRIPT_NAME'] = path_prefix
                environ['PATH_INFO'] = path[len(path_prefix):]
                return app(environ, start_response)
        response = Response(status='404 Not Found', body=[b'Not Found'])
        return response(environ, start_response)

# Usage in wsgi.py
from user_app.main import app_registry
from src.dispatcher import Dispatcher

dispatcher = Dispatcher()

# Register applications with the dispatcher
user_app = app_registry.get_app('user_app')
dispatcher.add_app('/user_app', user_app)

# WSGI application entry point
application = dispatcher
```
In this setup:
- The `Dispatcher` acts as the Front Controller, providing a single entry point for all incoming requests.
- The routing logic within the `Dispatcher` implements the **Router** pattern by mapping URL path prefixes
  to specific applications.

## Response
Now we are implementing the `Response` object as a callable WSGI application this technique offers several benefits, 
primarily rooted in simplicity, consistency, and adherence to the WSGI specification.
At `Dispatcher` we had:
```python
def __call__(self, environ, start_response):
    path = environ.get('PATH_INFO', '')
    for prefix, app in self.apps.items():
        if path.startswith(prefix):
            request = Request(environ)
            response = app(request, start_response)
            return response
    return Response(status='404 Not Found', body=[b'Not Found'])
```
We changed it to a more standard way (like Werkzeug 
https://github.com/pallets/werkzeug/blob/main/src/werkzeug/wrappers/response.py which says
The response object is itself a WSGI application callable.
)
```python
def __call__(self, environ, start_response):
    path = environ.get('PATH_INFO', '')
    for prefix, app in self.apps.items():
        if path.startswith(prefix):
            return app(environ, start_response)
    response = Response(status='404 Not Found', body=[b'Not Found'])
    return response(environ, start_response)
```

We added the `__call__` method to the `Response` class to make it a callable WSGI application.
```python
    def __call__(self, environ, start_response):
        # Start the WSGI response
        start_response(self._status, self.headers)
        # Return the body as an iterable
        return self
```

### Why Make the Response Object Callable?
1. Adherence to WSGI Specification:
   - The WSGI specification requires applications and middleware to be callables that accept `environ` and 
   `start_response` arguments. By making the Response object itself a callable, it naturally fits 
   into the WSGI ecosystem.

2. Simplified Error Handling:
   - Making the `Response` object callable allows for straightforward error handling. We can create a 
   response object for any HTTP status (e.g., 404 Not Found) and directly return it without 
   additional boilerplate code.

3. Consistency in Response Handling:
   - This approach ensures a uniform way of handling all responses, whether they are normal or error responses.
   The same mechanism is used to create and return responses, reducing the chance of errors and inconsistencies.

4. Enhanced Reusability and Encapsulation:
   - The `Response` object encapsulates all the details required to generate a proper HTTP response. 
   This encapsulation promotes reuse and reduces redundancy, as the same `Response` object can be used 
   in different parts of the application.

While this approach doesn't directly correspond to a specific design pattern, it leverages principles
of **encapsulation** and **interface alignment**. 
It is akin to the Adapter Pattern in that it adapts the `Response` object to fit the WSGI interface, 
but it is primarily a pragmatic solution for simplifying response handling in WSGI applications.
