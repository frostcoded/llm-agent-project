# utils/auth.py

import os

def get_env_credential(key: str, fallback: str = None) -> str:
    value = os.environ.get(key)
    if not value and fallback:
        return fallback
    elif not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value
