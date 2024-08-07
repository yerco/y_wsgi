# Asynchronous Task Handling

While staying within WSGI, we can introduce a simple way to offload tasks to a background worker. This can be 
done using a threading or multiprocessing approach. 
For this example, let’s use threading to demonstrate how you might handle background tasks.

I tried to use a queue this way below, but some tests didn't pass:
```python
import queue
import time
import threading

class BackgroundWorker:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self._stop_event = threading.Event()
        self.thread.start()

    def add_task(self, task, *args, **kwargs):
        self.task_queue.put((task, args, kwargs))

    def _worker(self):
        while not self._stop_event.is_set() or not self.task_queue.empty():
            try:
                task, args, kwargs = self.task_queue.get(timeout=0.1)
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing task: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                pass  # If queue is empty, just continue and check the stop event

    def wait_for_completion(self, timeout=None):
        if timeout is not None:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    self._stop_event.set()
                    self.thread.join()
                    raise TimeoutError("Task did not complete within the timeout period")
                if self.task_queue.empty():
                    break
                time.sleep(0.1)
        else:
            self.task_queue.join()

        self._stop_event.set()
        self.thread.join()
```
Apparently:
- Responsiveness to `_stop_event`: The list-based implementation is more responsive to the `_stop_event` being set because there is 
  no blocking `get()` call. This makes it easier to stop task processing immediately when the timeout occurs.
- Blocking Nature of Queue: In the queue-based implementation, the blocking behavior of `get(timeout=0.1)` 
  could cause a delay in stopping the task processing. Even though the timeout is reached, the worker thread 
  may still be processing a task that it retrieved from the queue before the timeout occurred.
