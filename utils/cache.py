# utils/cache.py

import functools

cache_store = {}

def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key in cache_store:
            return cache_store[key]
        result = func(*args, **kwargs)
        cache_store[key] = result
        return result
    return wrapper
