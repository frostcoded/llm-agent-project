# orchestrator/monitoring.py

import time
import logging
from typing import List, Dict

logger = logging.getLogger("monitoring")
logging.basicConfig(level=logging.INFO)

_start_time = time.time()
_errors: List[Dict] = []
_events: List[Dict] = []

def log_event(event: str, details: dict = None):
    record = {
        "timestamp": time.time(),
        "event": event,
        "details": details or {}
    }
    _events.append(record)
    logger.info(f"[Event] {event} - {details or ''}")

def log_error(source: str, message: str, context: dict = None):
    record = {
        "timestamp": time.time(),
        "source": source,
        "message": message,
        "context": context or {}
    }
    _errors.append(record)
    logger.error(f"[Error] {source}: {message} - {context or ''}")

def get_uptime() -> float:
    return round(time.time() - _start_time, 2)

def get_recent_errors(limit: int = 10) -> List[Dict]:
    return _errors[-limit:]

def get_recent_events(limit: int = 10) -> List[Dict]:
    return _events[-limit:]

def system_healthcheck() -> dict:
    return {
        "uptime_sec": get_uptime(),
        "error_count": len(_errors),
        "event_count": len(_events),
        "status": "healthy" if len(_errors) == 0 else "degraded"
    }
