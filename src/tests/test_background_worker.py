import time
import pytest

from src.background_worker import BackgroundWorker


def test_background_worker():
    worker = BackgroundWorker()
    result = []

    def sample_task(data):
        time.sleep(1)  # Simulate a small delay
        result.append(data)

    worker.add_task(sample_task, data="test data")
    worker.wait_for_completion()

    assert result == ["test data"], "Task did not complete as expected"


def test_background_worker_multiple_tasks():
    worker = BackgroundWorker()
    result = []

    def sample_task(data):
        result.append(data)

    worker.add_task(sample_task, data="task 1")
    worker.add_task(sample_task, data="task 2")
    worker.add_task(sample_task, data="task 3")
    worker.wait_for_completion()

    assert result == ["task 1", "task 2", "task 3"], "Multiple tasks did not complete as expected"


def test_background_worker_task_completion():
    worker = BackgroundWorker()
    result = []

    def delayed_task(data):
        time.sleep(1)
        result.append(data)

    worker.add_task(delayed_task, data="delayed task")
    start_time = time.time()
    worker.wait_for_completion()
    elapsed_time = time.time() - start_time

    assert result == ["delayed task"], "Delayed task did not complete as expected"
    assert elapsed_time >= 1, "Task did not take the expected amount of time"


def test_background_worker_completion_after_delay():
    worker = BackgroundWorker()
    result = []

    def long_task(data):
        time.sleep(5)
        result.append(data)

    worker.add_task(long_task, data="long task")
    worker.wait_for_completion()

    assert result == ["long task"], "Task should have completed despite the delay"


def test_background_worker_timeout():
    worker = BackgroundWorker()
    result = []

    def long_task(data):
        time.sleep(5)
        result.append(data)

    worker.add_task(long_task, data="long task")

    # Wait for completion with a timeout
    timeout_occurred = False
    try:
        worker.wait_for_completion(timeout=1)
        assert False, "Expected TimeoutError but none was raised"
    except TimeoutError:
        timeout_occurred = True
        print("Timeout occurred")

    # Ensure that timeout occurred
    assert timeout_occurred, "Expected a TimeoutError to be raised"

    # Check that the task eventually completed even after the timeout
    assert result == [] or result == ["long task"], "Unexpected task completion after timeout"
