# Session Middleware

SessionMiddleware finished and tested: some fixes are included to make the Memento work properly.

Our memento at this point works using a listy of `Session`.
Test include testing as with different users and different sessions and undo/redo leveraging the memento pattern.

## Things to notice

- At `src/middleware/session_middleware.py`
```python
    ...
    def _set_session_id(self, request: Request, session_id: str):
        path = request.path or '/'
        cookie = f'session_id={session_id}; Path=/; HttpOnly; SameSite=Lax; Secure'
        request.session_id_to_set = cookie
    ...
```
  - We are hard-coding `Path=/` to have a session for the whole site. including `{path}` would generate sessions 
    as per paths specific paths. Maybe we can configure it by app as a TODO.

- At `src/tests/test_session_middleware.py`
  - The test works and results in different session IDs for each request because each request to the endpoint
    `client.get('/')` does not send any session cookie, thus simulating a new user or a new session request. 
    As a result, the server treats each request as a new session request, generating a new session ID each time.

### How Cookies Work in Browsers:

1. Initial Request:
    - When you visit a website for the first time, your browser makes a request without any session cookies.
    - The server generates a new session and sends a Set-Cookie header in the response to set the session ID in your browser.
2. Subsequent Requests:
   - For all subsequent requests to the same site, your browser includes the Cookie header with the session ID.
   - This allows the server to identify your session and retrieve your session data.

Example:
1. Initial Request (no session cookie)
    ```bash
    GET / HTTP/1.1
    Host: example.com
    ```
    Response with `Set-Cookie`:
    ```bash
    HTTP/1.1 200 OK
    Set-Cookie: session_id=abcd1234; Path=/; HttpOnly; SameSite=Lax; Secure
    ```

2. Subsequent Request (with session cookie)
    ```bash
    GET /dashboard HTTP/1.1
    Host: example.com
    Cookie: session_id=abcd1234
    ```

### Middleware Order Considerations:
1. Session Middleware: Should generally be applied before the authentication middleware.
   This is because authentication typically relies on session data (e.g., checking if a user is logged in), 
   so the session needs to be initialized first.
2. Authentication Middleware: Should come after session middleware, as it may need to access session data
   to authenticate the user.

As an example in `user_app/main.py` we do
```python
# Register user module middlewares, order matters!
# Apply SessionMiddleware first
user_mod.use_middleware(SessionMiddleware)
# Apply AuthenticationMiddleware after SessionMiddleware
user_mod.use_middleware(AuthenticationMiddleware, public_routes=config.PUBLIC_ROUTES)
```

### Cookie names
- The name `session_id` is not mandatory; it can be any valid string that you choose to represent the session ID. 
  However, it’s a common convention to use a name like `session_id` or `sid` for clarity.
- Example: `session_id=abcd1234` could be changed to `my_session=abcd1234` if desired.

### `SameSite` Attribute
- The `SameSite` attribute in the cookie header is used to prevent certain types of cross-site request 
  forgery (CSRF) attacks by controlling when cookies are sent with cross-site requests.

#### Possible Values:
1. `SameSite=Strict`:
   - Behavior: Cookies are only sent in a first-party context (i.e., the request originates from the same site).
   - Use Case: Ideal for highly sensitive applications where strict control over cookie sharing is needed.
   - Example: A cookie with `SameSite=Strict` will not be sent when a user clicks a link to your site from
    another site or when loading your site in an iframe on another site.
2. `SameSite=Lax`:
   - Behavior: Cookies are sent with top-level navigations and will be sent along with GET requests initiated 
     by third-party websites.
   - Use Case: Provides a balance between security and usability. It protects against most CSRF attacks while
     allowing the cookie to be sent during normal user navigation.
   - Example: A cookie with `SameSite=Lax` will be sent when a user clicks a link to your site from another 
     site but will not be sent with requests triggered by other means (like loading an image or iframe).
3. `SameSite=None`:
    - Behavior: Cookies are sent with both cross-site and same-site requests (first-party and third-party requests).
    - Use Case: Used for cross-site requests where the cookie is required (e.g., for Single Sign-On).
    - Note: Requires the `Secure` attribute to be set as well to ensure the cookie is only sent over HTTPS connections.
    - Example: A cookie with `SameSite=None; Secure` will be sent with both first-party and third-party requests.

### Additional Security Measures
1. Session ID Rotation:
   - Implemented a mechanism to rotate session IDs periodically and upon sensitive actions.
2. Expiration Time:
   - Ensure session cookies have a reasonable expiration time to limit the duration of a potential hijack.

### Other
- Changes some shallow copies to deep copies to avoid issues with mutable objects.
