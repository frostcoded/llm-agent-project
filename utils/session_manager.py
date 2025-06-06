# utils/session_manager.py

from typing import Any, Dict


class SessionManager:
    """
    Tracks memory and state per session or user.
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def set(self, session_id: str, key: str, value: Any):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id][key] = value

    def get(self, session_id: str, key: str, default: Any = None) -> Any:
        return self.sessions.get(session_id, {}).get(key, default)

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_all(self, session_id: str) -> Dict[str, Any]:
        return self.sessions.get(session_id, {})
