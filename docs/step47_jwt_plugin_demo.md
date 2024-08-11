# JWT Plugin
## Demo Plugin
The JWT Demo Plugin showcases how to use the JWT middleware to protect specific routes. 
It registers a protected route `/jwt-demo` that requires a valid JWT token for access.

- Location: `user_app/modules/user_module/plugins/jwt_demo_plugin.py`
- Key Features:
  - Registers the `/jwt-demo` route.
  - Applies the `JWTAuthMiddleware` to the route to enforce JWT protection.

## Middleware
The `JWTAuthMiddleware` is responsible for protecting routes by ensuring that incoming requests contain
a valid JWT token. The middleware checks for the Authorization header and verifies the token’s validity and expiration.
- Location: user_app/modules/user_module/middleware/jwt_auth_middleware.py
- Key Features:
  - Extracts the JWT token from the Authorization header.
  - Verifies the token using the secret key and checks its expiration.
  - If the token is missing, invalid, or expired, it returns a 401 Unauthorized response.

## Generate Token Route
The `/generate-token` route allows users to obtain a JWT token by providing valid credentials 
(e.g., username and password). This token can then be used to access protected routes.
- Location: Defined within the app’s route registration logic.
- Key Features:
  - Accepts POST requests with JSON payload containing username and password.
  - Authenticates the user and generates a JWT token if the credentials are valid.

## Notes
- Headers were lowercased
- Tests required some path adjustments because at `src/app_registry.py`'s `create_module` we fixed `module_dir`:
`module_dir = os.path.join(base_dir, 'modules', module_name)`including the `modules` subfolder as 
a requirement
