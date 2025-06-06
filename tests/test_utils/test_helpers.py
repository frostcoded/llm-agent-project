from datetime import datetime
from utils.helpers import format_datetime, safe_get

def test_format_datetime():
    now = datetime.utcnow()
    assert "T" in format_datetime(now)

def test_safe_get():
    data = {"a": {"b": {"c": "value"}}}
    assert safe_get(data, ["a", "b", "c"]) == "value"
