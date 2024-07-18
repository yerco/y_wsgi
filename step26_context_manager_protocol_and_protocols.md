## **Protocols in Python**
1. **Descriptor Protocol**: Involves `__get__`, `__set__`, and `__delete__` methods for controlling attribute access.
2. **Iterator Protocol**: Involves `__iter__` and `__next__` methods for creating iterators.
3. **Async/Await Protocol**: Involves `__await__`, `__aiter__`, and `__anext__` methods for asynchronous programming.
4. **Number Protocol**: Involves methods like `__add__`, `__sub__`, `__mul__`, etc., for implementing arithmetic operations.
5. **Container Protocol**: Involves methods like `__len__`, `__getitem__`, and `__contains__` for sequence types.
6. **Callable Protocol**: Involves the `__call__` method to make an object callable like a function.

## **Context Manager Protocol**

1. **Context Manager Protocol**: Involves `__enter__` and `__exit__` methods for managing resources.
2. **Context Manager**: A context manager is an object that defines the runtime context to be established when executing
   a `with` statement.
3. **`with` Statement**: The `with` statement simplifies resource management by encapsulating common preparation and
   cleanup tasks.
4. **`contextlib` Module**: Provides utilities for working with context managers and the `with` statement.
5. **`contextlib.contextmanager` Decorator**: Used to define a factory function for creating context managers.
6. **`@contextmanager` Decorator**: A decorator that simplifies the creation of context managers using generator
   functions.

`src/utils/context_managers.py`
```python
import sys


class TemporarySysPath:
    def __init__(self, path):
        self.path = path
        self.original_sys_path = sys.path.copy()

    def __enter__(self):
        if self.path and self.path not in sys.path:
            sys.path.insert(0, self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        sys.path = self.original_sys_path
```

The intent is to temporarily add a path to `sys.path` and then restore the original `sys.path` when the context manager
exits.

We could have used the `contextlib` module to create a context manager using the `@contextmanager` decorator.

