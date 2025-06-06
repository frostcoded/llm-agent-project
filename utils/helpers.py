# utils/helpers.py

from datetime import datetime

def format_datetime(dt: datetime, tz: str = "UTC") -> str:
    return dt.astimezone().isoformat()

def safe_get(d: dict, keys: list, default=None):
    for key in keys:
        d = d.get(key, {})
    return d if d else default
