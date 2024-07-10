# Y-WSGI
A Nano (Femto) framework for learning purposes

## Overview

Y-WSGI is a minimalistic web framework designed to help developers understand the core concepts of web
frameworks and the design patterns involved. It serves as an educational tool to demonstrate how various
components of a web framework come together.

Note: This project is by no means a project that has reached a minimal level of maturity. 
It is a didactic work in progress, intended for learning and teaching purposes.

## Tools of the trade
- Python 3.11.8

## Features
- Lightweight and minimalistic
- Demonstrates key design patterns and architecture
- Customizable and extensible
- Basic authentication and authorization
- Middleware support
- Routing with support for public and protected routes

## Getting started

### Installation
1. Clone the repository:
    ```bash
    $ git clone https://github.com/your-repo/y-wsgi.git
    $ cd y-wsgit
    ```
  
2. Install the required packages
    ```bash
    $ pip install -r requirements.txt
    ```

### Running the server
You can run the server using, for example, either Gunicorn or uWSGI.

####  Using gunicorn
    ```bash
    $ gunicorn wsgi:application [--reload] [--access-logfile -]
    ```

#### Using uWSGI
    ```bash
    $ uwsgi --http :8000 --wsgi-file wsgi.py --callable application [--py-autoreload=1]
    ```

### Accessing the server
Once the server is running, you can access it in your web browser at: http://127.0.0.1:8000

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
