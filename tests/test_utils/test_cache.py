# tests/test_utils/test_cache.py

import time
from utils.cache import cache


def test_basic_cache():
    calls = {"count": 0}

    @cache()
    def compute(x):
        calls["count"] += 1
        return x * 2

    assert compute(2) == 4
    assert compute(2) == 4
    assert calls["count"] == 1  # second call used cache


def test_cache_with_ttl():
    calls = {"count": 0}

    @cache(ttl=1)
    def compute(x):
        calls["count"] += 1
        return x + 1

    compute(5)
    compute(5)
    assert calls["count"] == 1

    time.sleep(1.1)
    compute(5)
    assert calls["count"] == 2  # TTL expired
