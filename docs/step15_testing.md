# Testing
To spot issues.

## pytest
```bash
% pip install pytest==8.2.2
```

## Database
the in-memory database dictionary is retaining its state between different requests within the same runtime. 
This is expected behavior when the application is running within a single process, and the state is kept in memory.
Here’s a breakdown of why this happens and how it works:

Why the In-Memory Database Retains State
- Single Process: When you run your application, it typically runs in a single process.
  The in-memory database (`database` dictionary) is part of this process's memory space.
- Persistent Memory State: As long as the process is running, the memory state is retained. 
  This means the `database` dictionary keeps its data between different requests as long as the application is running.

Gunicorn
If we use the `-w` flag to run multiple worker processes, each process will have its own separate memory space. 
This means that the in-memory `database` dictionary will not be shared across different worker processes. 
As a result, any changes made to the database in one worker process will not be visible to other worker processes.

## More on Design Patterns

### Observer
- Publisher:
  - The `App` class acts as the publisher. It is responsible for triggering the events and notifying all the
  registered subscribers (hooks) when a particular event occurs.
  - The specific events are the points in the request lifecycle, such as before a request is processed, 
  after a request is processed, before the first request is processed, and when a request is being torn down.

- Subscribers:
  - The hooks (functions or methods) that are registered with the `App` class are the subscribers. 
  These hooks are added to the hooks lists (`before_request_hooks`, `after_request_hooks`, etc.) in the `Hooks`

Example Usage
1. Defining a Hook:
    ```python
    def log_request():
        print("Logging request...")
    
    def authenticate():
        print("Authenticating request...")
    ```
2. Registering Hooks:
    ```python
    app = App()
    app.before_request(log_request)
    app.before_request(authenticate)
    ```
3. Triggering Hooks (Events):
    ```python
    response = self._apply_before_request_middlewares_and_hooks(request)
    ```

### Composite
The Composite Pattern was used to combine various components like middleware and hooks into a unified 
structure that the framework processes in a cohesive manner.

- Nodes (Composites):
  - These are the classes that can have children and define behaviors for handling groups of objects.
  - In our case, the `App` class and the `Hooks` class act as composites because they manage and apply a 
    collection of middlewares and hooks respectively.

- Leaves (Components):
  - These are the classes that do not have children and define behaviors for individual objects.
  - In our case, the `Middleware` and `Hook` classes act as leaves because they define the behavior for 
    individual middleware and hooks respectively.
  - In our framework, each middleware class (e.g., `LoggingMiddleware`, `AuthenticationMiddleware`) 
    and each individual hook function (e.g., `log_request`, `authenticate`) act as leaves.
  
    ```bash
    App (Composite)
      ├── Hooks (Composite)
      │    ├── before_request_hook (Leaf)
      │    ├── after_request_hook (Leaf)
      │    ├── teardown_request_hook (Leaf)
      │    └── before_first_request_hook (Leaf)
      ├── LoggingMiddleware (Leaf)
      ├── AuthenticationMiddleware (Leaf)
      └── other middlewares (Leaves)
    ```