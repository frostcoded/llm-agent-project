# utils/metrics.py

import time
import functools
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_metrics = {}

def track_agent(name: str):
    """
    Decorator to track execution time and invocation count of an agent method.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start

            if name not in _metrics:
                _metrics[name] = {"calls": 0, "total_time": 0}

            _metrics[name]["calls"] += 1
            _metrics[name]["total_time"] += duration

            logger.info(f"[Metrics] {name} ran in {duration:.2f}s (call #{_metrics[name]['calls']})")
            return result
        return wrapper
    return decorator

def report_metrics():
    """
    Returns current metrics snapshot.
    """
    return _metrics
