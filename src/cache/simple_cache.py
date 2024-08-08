import time


class SimpleCache:
    def __init__(self, timeout: int = 60):
        self._cache = {}
        self.timeout = timeout

    def get(self, key):
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.timeout:
                return value
            else:
                del self._cache[key]  # Remove expired cache
        return None

    def set(self, key, value):
        self._cache[key] = (value, time.time())

    def clear(self):
        self._cache.clear()
