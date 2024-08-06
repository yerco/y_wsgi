# Implementing Mediator
We can use it for different things later but for now it's going to be a Mediator to handle forms and particularly
CSRF tokens at the moment.

Most examples show a Mediator used for a class but here we create the Mediator (`FormMediator`) inside the `BaseForm`.
As of now as we will use it for CSRF, we dispatch events 
- We "store" a CSRF token at the `SessionContext` to have it available, which can be seen at `CSRFMiddleware`
- At `BaseForm` having the mediator we send an event `set_csrf` which allows us to use `embed_csrf_token` 
  which allows us to set the csrf token:
  ```html
  html += f"<input type='hidden' name='csrf_token' value='{self.csrf_token}'>"
  ```
  This loop can be a bit overkill but the reason is that we can do other things at the Mediator communicating that 
  when that event happens some other class can do something else.
- The same way we emit the event `csrf_check` when checking the token for validation (there we use the token available
  at `SessionContext`.
- The Mediator is made lazy at `get_form_mediator` so we create it when we need it.
- This approach was chosen because it clearly shows how the mediator coordinates actions between different
  parts of the system (like setting the CSRF token and handling validation) and emphasizes the decoupling between 
  the form and the token generation logic.

