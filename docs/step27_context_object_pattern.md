# Context Object Pattern 

The best implementation for `RequestContext` depends on how we want to encapsulate the request-related data
and how you plan to use the context throughout your application. 

Here are two main options to consider:

## Option 1: RequestContext Accepting Request in Constructor
This approach tightly integrates the `RequestContext` with the `Request` object by passing the `Request` object in 
the constructor. This allows the context to directly delegate to the Request object for request-specific information.
```python
# src/context/request_context.py
from typing import Optional
from src.core.request import Request
from src.session.session import Session

class RequestContext:
    def __init__(self, request: Request):
        self.request = request
        self._session: Optional[Session] = None
        self.user = None
        self.config = load_config().config  # Load the config for the current app

    @property
    def method(self) -> str:
        return self.request.method

    @property
    def path(self) -> str:
        return self.request.path

    # Add more properties as needed, delegating to the underlying request object
    # ...

    @property
    def session(self) -> Optional[Session]:
        return self._session

    @session.setter
    def session(self, session: Session) -> None:
        self._session = session
```
- Pros:
    - Easier to implement as it directly delegates to the Request object.
    - Keeps the context class clean and focused on its role.
    - Ensures that the request-related properties and methods are always up-to-date with the actual `Request` object.
- Cons:
    - Tightly couples the `RequestContext` with the `Request` object.
    - Slightly less flexible in terms of modification and extension.

## Option 2: RequestContext Without Request Object
This approach decouples the `RequestContext` from the `Request` object. Instead, it directly stores all 
relevant data and state.
```python
# src/context/request_context.py
from typing import Optional
from src.session.session import Session

class RequestContext:
    def __init__(self):
        self.method = None
        self.path = None
        self.query_string = None
        self.headers = {}
        self.body = None
        self.session: Optional[Session] = None
        self.user = None
        self.config = load_config().config  # Load the config for the current app

    def initialize_from_request(self, request):
        self.method = request.method
        self.path = request.path
        self.query_string = request.query_string
        self.headers = request.headers
        self.body = request.body

    # Add more properties and methods as needed to handle request data
```
- Pros:
    - Fully decoupled from the Request object.
    - More flexible in terms of modification and extension.
    - Can be used in contexts where the Request object is not available or necessary.
- Cons:
    - Requires more boilerplate code to copy and maintain the request data.
    - Potentially duplicative, as the RequestContext might need to replicate functionality already present 
      in the `Request` object.

## Threading Considerations
(at least as I understand it) the creation of threads is typically managed by the web server
(e.g., Gunicorn, uWSGI) or the web framework itself if it supports asynchronous processing. 
This means that you don’t have to manually create threads for handling each request; the web server does that for you.

Simplified Flow

1. Web Server: When a web server like Gunicorn receives a request, it spawns a new thread
   (or uses an existing one from a thread pool) to handle the request.
2. Dispatcher: The Dispatcher receives the request and determines which application should handle it.
3. AppContext: Within the application, AppContext uses thread-local storage to ensure the correct context 
   is set for the thread handling the request.
4. Request Handling: The application processes the request within its context.

Example Request Flow
1. Request Received: A request for `/admin/some/endpoint` is received.
2. Thread Assigned: The web server assigns a thread to handle the request.
3. Dispatcher: The Dispatcher routes the request to `admin_app`.
4. Set Context: `admin_app.context.set_current_app('admin_app')` sets the context for the current thread.
5. Process Request: The request is processed within the admin_app context.
6. Reset Context: After processing, the context is reset to avoid affecting future requests.

Analogy: Runners and Oranges

1. Basket of Oranges:
   - Represents the incoming requests to the web server.
2. Runners:
   - Represent the threads. Each runner/thread is responsible for picking up one orange/request and handling it.
3. Picking Up an Orange:
   - When a request comes in, a runner (thread) is assigned to pick it up. In this analogy, this is like the web 
   server assigning a thread to handle a request.
4. Running with the Orange:
   - The runner then processes the request. This involves setting the context (like ensuring the runner knows 
   which path to take, which in your framework is setting the current application context).
5. Depositing the Orange in Another Basket:
   - Finally, the runner deposits the orange in the destination basket. This is akin to the thread completing 
   the request and sending back a response.
6. Thread-Local Storage:
   Just as each runner keeps track of their own orange and path, each thread has its own local storage 
   (`using threading.local()`) to maintain the current context without interfering with other threads.

Detailed Steps in the Analogy

1. Basket of Oranges (Requests): Each orange in the basket is a new request that needs to be processed.
2. Runners (Threads): When an orange is picked up, a runner is assigned. This represents a thread being assigned
   to handle the request.
3. Context (Path):
   Each runner needs to know the path they should take. This is like setting the current application context
   (`app_context.set_current_app(app.name)`).
4. Running with the Orange (Processing the Request):
   The runner follows the path, processing the request within the correct context. This ensures they know 
   where to go and what to do (the configurations and context-specific data are properly set).
5. Depositing the Orange (Sending Response):
   The runner reaches the destination and deposits the orange, completing the task. This is like the thread
   finishing processing the request and sending back the response.
6. Isolation with Thread-Local Storage:
   Each runner maintains their own path and orange, without mixing up with others. This is achieved with
   thread-local storage in your implementation, ensuring each thread has its own isolated context.

Benefits of Using Threading
- Isolation: Each thread handles a single request independently, maintaining its own context.
- Concurrency: Multiple requests can be processed simultaneously, improving performance.
- Context Management: Thread-local storage ensures that each thread has the correct context, preventing
  data leakage between requests.

Example Request Handling with Analogy
- Request Received: An orange is added to the basket.
- Thread Assigned: A runner picks up the orange.
- Setting Context: The runner gets the path they need to take.
- Processing Request: The runner follows the path with the orange.
- Sending Response: The runner deposits the orange in the destination basket.
- Resetting Context: The runner is ready to pick up a new orange without residual data from the previous run.
