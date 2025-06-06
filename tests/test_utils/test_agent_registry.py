# tests/test_utils/test_agent_registry.py

import pytest
from utils.agent_registry import register_agent, get_agent, list_agents


def test_register_and_retrieve_agent():
    class DummyAgent:
        def run(self): return "ok"

    register_agent("dummy", lambda: DummyAgent())
    agent = get_agent("dummy")

    assert isinstance(agent, DummyAgent)
    assert agent.run() == "ok"


def test_list_agents_contains_registered():
    agents = list_agents()
    assert "dummy" in agents


def test_get_agent_not_found():
    with pytest.raises(ValueError):
        get_agent("nonexistent_agent")
