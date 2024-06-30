Design Patterns Used in the Nano Framework up to this point

- Template Method Pattern:
Where: In the `Middleware` class.
How: The Middleware class provides template methods `before_request` and `after_request`, which can be overridden by
subclasses to provide specific behavior. 
This allows the framework to define the skeleton of the request processing algorithm while enabling subclasses to
customize certain steps.

- Strategy Pattern:
Where: In the routing mechanism and request handling.
How: The Router class allows dynamic selection of the handler function or view class based on the request path. 
This decouples the routing logic from the actual handlers, allowing different routing strategies to be used without
changing the core request processing logic.

- Chain of Responsibility Pattern:
Where: In the middleware and hooks processing.
How: The `_apply_before_request_middlewares_and_hooks`, `_apply_after_request_middlewares_and_hooks`, and 
`_apply_teardown_request_hooks` methods implement a chain of responsibility. 
Each middleware or hook in the chain has an opportunity to process the request or response and pass it along to
the next component in the chain.

- Simple Factory Pattern:
Where: In the creation and registration of routes and middleware.
  1. Route Registration: The `route` decorator method acts as a factory for creating and registering route handlers.
  2. Middleware Registration: The `use_middleware` method acts as a factory for creating and registering middleware
  instances.
How: The route decorator and use_middleware method act as factories for creating and registering route
handlers and middleware instances. This provides a clean and consistent way to configure the application's behavior.

- Command Pattern:
Where: In the way request handling is executed.
How: Each request can be seen as a command object that is executed by the framework. 
The handlers (function-based or class-based views) represent the commands that process the requests.

