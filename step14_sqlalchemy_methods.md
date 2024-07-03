# Summary of Work from ORM Interface Adapter to Implementing Authentication and Views

## 1. Introduction of ORM Interface Adapter
- Goal: Abstract the ORM to allow easy switching between a minimal custom ORM and a fully-featured ORM like SQLAlchemy.
- Implementation:
  - Created `ORMInterface` to define common operations like `create`, `all`, `filter`, and `get_by_id`.
  - Implemented `MinimalORMAdapter` and `SQLAlchemyORMAdapter` to conform to `ORMInterface`.

## 2. Configuring the Framework to Use Either ORM
- Goal: Allow the framework to use either the minimal ORM or SQLAlchemy based on availability.
- Implementation:
  - Created a configuration file to manage which ORM to use.
  - Modified the app initialization to check for SQLAlchemy and fallback to the minimal ORM if not available.
```python
try:
    from src.database.sqlalchemy_orm_adapter import SQLAlchemyORMAdapter
    USE_SQLALCHEMY = True
except ImportError:
    from src.database.minimal_orm_adapter import MinimalORMAdapter
    USE_SQLALCHEMY = False
```

## 3. Implementing Views with ORM Integration
- Goal: Demonstrate how to use the ORM within the views.
- Implementation:
  - Created views to handle routes like `/create_user`, `/users`, `/user/<int:id>`, and `/filter_users/<username>`.
  - Injected the ORM into views to perform operations like creating and fetching users.

To try `/create_user` we can use the following: (the rest are GETs from the browser)
```bash
% curl -X POST http://localhost:8000/create_user \
     -H "Content-Type: application/json" \
     -d '{"username": "new_user", "password": "password123"}'
```

## 4. Handling HTTP Methods in Routing
- Goal: Extend the routing system to support different HTTP methods.
- Implementation:
  - Updated the `LazyRoute` and `Router` classes to handle HTTP methods.
  - Allowed function-based views (FBVs) to specify methods.

To extend the routing system to support different HTTP methods, we need to ensure that the `LazyRoute` and `Router` 
classes  can handle and match routes based on the HTTP method (e.g., GET, POST, DELETE, etc.).

## 5. Updating Middleware for Authentication
- Goal: Whitelist specific routes for public access.
- Implementation:
  - Modified AuthenticationMiddleware to use regex patterns for public routes.

## Key Takeaways
- ORM Abstraction: By using the ORMInterface, we can switch between different ORMs without changing the rest of the codebase.
- Dynamic Routing: Our framework now supports dynamic path segments and multiple HTTP methods.
- Middleware and Security: We have implemented a flexible middleware system that allows for authentication and route whitelisting.
- View Integration: Views can now interact with the ORM seamlessly, demonstrating both class-based and function-based views.