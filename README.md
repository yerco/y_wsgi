# Y-WSGI
A Nano (Femto) framework for learning purposes

## Overview

Y-WSGI is a minimalistic web framework designed to help developers understand the core concepts of web
frameworks and the design patterns involved. It serves as an educational tool to demonstrate how various
components of a web framework come together.

Note: This project is by no means a project that has reached a minimal level of maturity. 
It is a didactic work in progress, intended for learning and teaching purposes.

## How This is Framework has been developed
This framework was developed incrementally, focusing on implementing design patterns as they emerged naturally
during the problem-solving process. The idea was to build a minimal but functional web framework while providing
a hands-on learning experience in applying design patterns.

Key Points:
- The framework is intentionally minimalistic, focusing on educational value rather than production-readiness.
- Decisions were made on the spot, leading to some architectural choices that may not be optimal. 
  The goal is to learn and teach, so these decisions are part of the learning process.
- The framework has not been extensively tested, and there may be flaws or areas for improvement.

## Tools of the trade
- Python 3.11.8

## Features
- Lightweight and minimalistic
- Demonstrates key design patterns and architecture
- Customizable and extensible
- Basic authentication and authorization
- Middleware support
- Routing with support for public and protected routes
- Integration of signals (observer)

## Some Design Patterns Implemented
- Factories
- Strategy
- Composite
- Observer
- Template
- Builder
- Register
- Memento
- etc.

## Getting started

### Installation
1. Clone the repository:
    $ git clone https://github.com/your-repo/y-wsgi.git
    $ cd y-wsgit
  
2. Install the required packages
    $ pip install -r requirements.txt

### Running the server
You can run the server using, for example, either Gunicorn or uWSGI.

####  Using gunicorn
    $ gunicorn wsgi:application [--reload] [--access-logfile -]

#### Using uWSGI
    $ uwsgi --http :8000 --wsgi-file wsgi.py --callable application [--py-autoreload=1]

### Accessing the server
Once the server is running, you can access it in your web browser at: http://127.0.0.1:8000

### Demo and Example Pages
To help you get started and see the framework in action, a pseudo demonstration is available under 
the `user_app` module. Once you’ve set up and run the web server, you can visit example pages
such as http://localhost:8000/user_app_page to explore the features and functionality of the framework.

## Usage

### Understanding Apps and Modules
In Y-WSGI, an **app** represents a standalone application with its own configuration, middleware, hooks, and routing
An app can have multiple **modules**, which are smaller units within the app, encapsulating specific features 
or functionalities. Modules can have their own middleware, hooks, views, and models.

### Creating and App
An app is created using the `AppRegistry`. Here is an example of how to create an app and add modules to it:
```python
from src.app_registry import AppRegistry
from src.database.orm_initializer import initialize_orm
from user_app.modules.user_module.views import hello_views, user_views
from user_app.modules.user_module.models.models import User
from user_app.config import config
from src.middleware.authentication_middleware import AuthenticationMiddleware

# Create an instance of AppRegistry
app_registry = AppRegistry()

# Create an application instance
app = app_registry.create_app('user_app')

# Initialize the ORM adapter
orm = initialize_orm([User])

# Create user module
user_mod = app_registry.create_module('user_module', app)

# Register user module middlewares
user_mod.use_middleware(AuthenticationMiddleware, public_routes=config.PUBLIC_ROUTES)

# Register routes
user_mod.register_routes(user_views.register_routes, orm)
user_mod.register_routes(hello_views.register_routes)
```

### Creating a View
Views are the functions or classes that handle requests and return responses. 
Here is an example of how to create views and register them with a module:
```python
# user_app/modules/user_module/views/user_views.py
import json
from typing import List, Tuple

from src.core.request import Request
from src.core.response import Response
from src.database.orm_interface import ORMInterface

def register_routes(module, orm: ORMInterface):
    @module.route('/json', methods=['GET'], public=True)
    def json_handler(request: Request) -> Response:
        data = {'message': 'Hello, JSON!'}
        status: str = '200 OK'
        headers: List[Tuple[str, str]] = [('Content-type', 'application/json')]
        return Response(status=status, headers=headers, body=[json.dumps(data).encode('utf-8')])
```
In this example, the `json_handler` view is registered with the user_module and is accessible via the `/json route.

### Setting Up Assets and Templates

#### Templates
In this framework, templates are organized within each module of your app. 
This structure allows for modular and organized template management. 
Here’s how you should set up your templates:
1. Module Templates: Each module should have its own templates directory.
2. Template Files: Place your HTML template files within the templates directory of each module.
Example Directory Structure
```bash
your_app/
    ├── __init__.py
    ├── config.py
    ├── modules/
    │   ├── module1/
    │   │   ├── __init__.py
    │   │   ├── views.py
    │   │   └── templates/
    │   │       └── template1.html
    │   ├── module2/
    │   │   ├── __init__.py
    │   │   ├── views.py
    │   │   └── templates/
    │   │       └── template2.html
    │   └── module3/
    │       ├── __init__.py
    │       ├── views.py
    │       └── templates/
    │           └── template3.html
```

#### Assets
Assets such as images, CSS, and JavaScript files should be placed in a single `assets` directory within each app. 
This centralizes the management of static files for easier access and better performance.
1. App Assets: Create an assets directory within your app directory.
2. Static Files: Place your static files (images, CSS, JavaScript) within this directory.
Example Directory Structure
```bash
your_app/
    ├── __init__.py
    ├── config.py
    ├── assets/
    │   ├── css/
    │   │   └── styles.css
    │   ├── js/
    │   │   └── scripts.js
    │   └── images/
    │       └── logo.png
    ├── modules/
    │   ├── module1/
    │   │   ├── __init__.py
    │   │   ├── views.py
    │   │   └── templates/
    │   │       └── template1.html
    │   ├── module2/
    │   │   ├── __init__.py
    │   │   ├── views.py
    │   │   └── templates/
    │   │       └── template2.html
    │   └── module3/
    │       ├── __init__.py
    │       ├── views.py
    │       └── templates/
    │           └── template3.html
```

#### Signals and Middleware
To showcase the Observer pattern, a custom `SignalManager` was implemented, allowing different parts of
the framework to react to events such as `request_started` and `request_finished`. This feature is demonstrated
through the `ResponseTimeMiddleware`, which tracks the response time of each request and appends it to 
the response headers.

## Feedback and Contributions

Criticism, doubts, and comments are welcome! Your feedback is invaluable in improving and refining this framework. 
If you’d like to share your thoughts, report issues, or contribute to the project, feel free to reach out 
through GitHub.
You can contact me by opening an issue or starting a discussion here on GitHub. I’m looking forward to hearing from you!
