# Observer
- The `Signal` class would manage the connections between signals and their **listeners** (**observers**). 
  It would allow components to subscribe to certain events and get notified when those events occur.
- We will create functions or methods that _handle_ the signals when they are emitted. 
  These `handlers` will be the `observers` in the Observer pattern.
- We will connect Signals to Handlers
- In views or models we will emit signals when certain actions occur

So we created a Middleware where we connect to the signals and handle them. 
```python
class ResponseTimeMiddleware(Middleware):
  def __init__(self, signal_manager: SignalManager):
    super().__init__()
    self.start_time = None
    self.signal_manager = signal_manager
    self.start_time = None

  def before_request(self, request_context: RequestContext) -> Optional[Response]:
    # To have it available at view level
    request_context.signal_manager = self.signal_manager
    self.signal_manager.connect('request_started', self.on_request_started)
    self.signal_manager.connect('request_finished', self.on_request_finished)
    return None

  def after_request(self, request_context: RequestContext, response: Response) -> Optional[Response]:
    self.signal_manager.disconnect('request_started', self.on_request_started)
    self.signal_manager.disconnect('request_finished', self.on_request_finished)
    return response

  def on_request_started(self, request_context):
    self.start_time = time.time()

  def on_request_finished(self, request_context, response):
    if self.start_time:
      elapsed_time = time.time() - self.start_time
      print(f"Request for {request_context.path} took {elapsed_time:.8f} seconds")
      response.set_header('X-Response-Time', f'{elapsed_time:.8f} seconds')
```

Then at a view we emit the signals
```python
request_context.signal_manager.emit('request_started', request_context=request_context)

request_context.signal_manager.emit('request_finished', request_context=request_context, response=response)
```

The `ResponseTimeMiddleware` should be placed at the top of the middleware stack in `main.py`.
This ensures that it connects to the signals and starts tracking the request time as early as possible
in the request lifecycle, and that it has the chance to finalize and calculate the response time
after other middlewares just before the final response is sent back.
