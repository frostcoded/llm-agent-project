# utils/cache.py

import functools
import time
import hashlib

_cache_store = {}
_cache_expiry = {}

def _make_cache_key(func_name, args, kwargs):
    raw = f"{func_name}-{args}-{frozenset(kwargs.items())}"
    return hashlib.sha256(raw.encode()).hexdigest()

def cache(ttl: int = None):
    """
    Decorator to cache function results with optional TTL.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_cache_key(func.__name__, args, kwargs)
            now = time.time()

            if key in _cache_store:
                if ttl is None or _cache_expiry.get(key, 0) > now:
                    return _cache_store[key]

            result = func(*args, **kwargs)
            _cache_store[key] = result
            if ttl:
                _cache_expiry[key] = now + ttl
            return result
        return wrapper
    return decorator
