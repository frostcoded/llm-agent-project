# tests/test_utils/test_session_manager.py

from utils.session_manager import SessionManager


def test_session_set_and_get():
    sm = SessionManager()
    sm.set("user1", "last_query", "show me sales")
    assert sm.get("user1", "last_query") == "show me sales"


def test_session_isolation():
    sm = SessionManager()
    sm.set("user1", "key", "value1")
    sm.set("user2", "key", "value2")
    assert sm.get("user1", "key") == "value1"
    assert sm.get("user2", "key") == "value2"


def test_session_clear():
    sm = SessionManager()
    sm.set("user1", "key", "value")
    sm.clear("user1")
    assert sm.get("user1", "key") is None


def test_session_get_all():
    sm = SessionManager()
    sm.set("user1", "a", 1)
    sm.set("user1", "b", 2)
    data = sm.get_all("user1")
    assert data == {"a": 1, "b": 2}
