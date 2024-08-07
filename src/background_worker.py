import time
import threading


class BackgroundWorker:
    def __init__(self):
        self.tasks = []
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self._stop_event = threading.Event()
        self._task_lock = threading.Lock()
        self.thread.start()

    def add_task(self, task, *args, **kwargs):
        with self._task_lock:
            self.tasks.append((task, args, kwargs))

    def _worker(self):
        while not self._stop_event.is_set() or self.tasks:
            with self._task_lock:
                if self.tasks:
                    task, args, kwargs = self.tasks.pop(0)
                else:
                    task = None

            if task:
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing task: {e}")
            else:
                time.sleep(0.1)

    def wait_for_completion(self, timeout=None):
        if timeout is not None:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    self._stop_event.set()
                    self.thread.join()
                    raise TimeoutError("Task did not complete within the timeout period")
                time.sleep(0.1)

        self._stop_event.set()
        self.thread.join()
