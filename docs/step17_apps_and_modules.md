# Apps and Modules

The framework will be organized in apps and modules. 
Each app will contain its own modules for handling different parts of the application logic.
The modules are similar to the apps of django or the blueprints of flask.
Why I included apps as a bigger concept than modules is because I was just coding that idea popped up to showcase
the Registry Pattern more clearly :P

## Registry Pattern
The Registry Pattern is used to keep track of objects, typically singletons, and provide a global point of 
access to them, it  provides methods to create, retrieve, and list these instances. The `AppRegistry` class
is an example of this pattern. we have a centralized way to manage and access multiple application instances, 
making the framework more modular and flexible. We can manage multiple applications and their configurations.
Each application can be configured independently, and the WSGI entry point can dynamically select which 
application to serve based on the request.

Key Characteristics of the Registry Pattern:
- Centralized Access: Provides a single point of access to multiple instances.
- Global State: Acts as a global repository for managing instances.
- Singleton Management: Often used to manage singleton instances or shared resources.

### Specific Example:

**Step 1: Define the AppRegistry Class**

We created a `AppRegistry` class to manage the applications.
```python
# src/app_registry.py
from src.app import App

class AppRegistry:
def __init__(self):
self.apps = {}

    def create_app(self, name: str) -> App:
        app = App()
        self.apps[name] = app
        return app

    def get_app(self, name: str) -> Optional[App]:
        return self.apps.get(name)
```

**Step 2: Register Applications**

We use `AppRegistry` in the user application to create and manage multiple application instances.
```python
# user_app/main.py
from src.app_registry import AppRegistry
from user_app.middleware.logging_middleware import LoggingMiddleware
from user_app.middleware.authentication_middleware import AuthenticationMiddleware
from user_app.hooks import some_hooks
from user_app.views import user_views, hello_views
from user_app.models.models import User
from src.database.orm_initializer import initialize_orm
from src.database.repository import UserRepository

# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('user_app')

# Register Middlewares
app.use_middleware(LoggingMiddleware)
app.use_middleware(AuthenticationMiddleware)

# Register hooks
app.before_request(some_hooks.before_request_hook)
app.after_request(some_hooks.after_request_hook)
app.teardown_request(some_hooks.teardown_request_hook)
app.before_first_request(some_hooks.before_first_request_hook)

# Initialize the ORM adapter
orm = initialize_orm([User])

# Register model (example)
orm.register(User)

# Register routes
user_views.register_routes(app, orm)
hello_views.register_routes(app)

# Example usage
user_repo = UserRepository(orm)
user = orm.create(User, username='john_doe', password='password123')
print(user)
user = orm.create(User, username='jane_doe', password='password123')
print(user)

users = orm.all(User)
print("All of them:\n", users)
```

**Step 3: Retrieve and Use Applications**

In the WSGI file, we retrieve the application instance from the registry.
```python
# wsgi.py
from user_app.main import app_registry

# Get the application instance
app = app_registry.get_app('user_app')

# WSGI application entry point
application = app
```

## Usefulness
Having a structure that allows for both applications and modules within those applications can be beneficial, 
especially for large projects. Here's a breakdown of why this might be a good thing and when it can be 
particularly useful:

Benefits of Applications Containing Modules
1. Scalability:
   - Large Projects: For very large projects, having an additional layer of organization can help manage complexity.
   Applications can represent major sections of the project, while modules can handle specific features or components 
   within those sections.
2. Separation of Concerns:
   - Clear Boundaries: Applications can have clear boundaries, with each application handling a distinct domain
   or functionality. Modules within these applications can then encapsulate specific tasks or features, 
   promoting a clear separation of concerns.

3. Reusability:
   - Modular Design: Modules can be designed to be reusable across different applications. 
   This is particularly useful if you have common functionality that needs to be shared across multiple parts 
   of the project.

4. Maintainability:
    - Easier Maintenance: With a clear hierarchy, it’s easier to maintain and update parts of the project. 
    We can focus on a specific module without worrying about the entire application.

5. Team Collaboration:
    - Parallel Development: Different teams can work on different applications or modules in parallel, 
    - reducing bottlenecks and improving development speed.

## Comparison with Django and Flask
Django:
Django projects are divided into apps, which is a practical way to organize code. 
Each app is a self-contained module that can be reused in different projects. 
Django apps are great for medium to large projects but can become complex in very large projects.

Flask:
Flask uses blueprints to organize code. Blueprints allow you to split your application into smaller pieces,
making it easier to manage. This is very flexible and lightweight, but for extremely large projects, 
you might end up with many blueprints, which can be challenging to manage.

Nano Framework:
By introducing both applications and modules, you create a hierarchical structure that can scale with the project size.
It combines the modularity of Django apps and Flask blueprints but adds a layer for better organization.

I'm not saying that our is better, not at all! It's just a different approach to organize the code.

## When to Use This Hierarchy
1. Large Enterprise Applications:
    When building large enterprise applications with multiple teams working on different parts of the project.

2. Microservices Architecture:
    When implementing a microservices architecture, where each service could be an application with its own modules.

3. Multi-Tenant Applications:
    For multi-tenant applications where each tenant might have its own application with shared and specific modules.
