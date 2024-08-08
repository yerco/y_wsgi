import time

from src.cache.simple_cache import SimpleCache


def test_cache_set_and_get():
    cache = SimpleCache(timeout=5)
    cache.set('key', 'value')
    assert cache.get('key') == 'value', "Cache should return the stored value"


def test_cache_expiry():
    cache = SimpleCache(timeout=1)
    cache.set('key', 'value')
    time.sleep(2)
    assert cache.get('key') is None, "Cache should expire after the timeout"


def test_cache_with_timeout():
    cache = SimpleCache(timeout=1)
    cache.set('key', 'value')
    assert cache.get('key') == 'value', "Cache should return the stored value"
    time.sleep(2)
    assert cache.get('key') is None, "Cache should expire after the timeout"
