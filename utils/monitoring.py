# utils/monitoring.py

import logging
import time

logger = logging.getLogger(__name__)

def monitor(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{func.__name__} executed in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper
