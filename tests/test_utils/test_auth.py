import os
import pytest
from utils.auth import get_env_credential

def test_get_env_credential(monkeypatch):
    monkeypatch.setenv("TEST_KEY", "secure123")
    assert get_env_credential("TEST_KEY") == "secure123"

def test_missing_credential_raises(monkeypatch):
    with pytest.raises(EnvironmentError):
        get_env_credential("NON_EXISTENT")
