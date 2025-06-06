# tests/test_agents/test_incident_responder.py

import pytest
from agents.incident_responder import IncidentResponder

@pytest.fixture
def mock_config():
    return {
        "llms": {"openai": {"api_key": "fake"}},
        "slack": {"enabled": True, "token": "fake-token"}
    }

def test_respond_to_alert(monkeypatch, mock_config):
    agent = IncidentResponder(mock_config)

    # Mock LLM summarization and Slack notification
    monkeypatch.setattr(agent.llm, "summarize_responses", lambda prompt: {"summary": "System outage detected."})
    monkeypatch.setattr(agent.slack, "notify", lambda msg, channel='#general': {"ok": True})

    response = agent.respond_to_alert("CRITICAL: System down", system_context="Production", notify=True)

    assert "summary" in response
    assert response["summary"] == "System outage detected."

def test_no_slack_notify(monkeypatch):
    # Slack is disabled in this config
    agent = IncidentResponder({"llms": {"openai": {"api_key": "fake"}}, "slack": {"enabled": False}})

    monkeypatch.setattr(agent.llm, "summarize_responses", lambda prompt: {"summary": "No Slack needed"})
    response = agent.respond_to_alert("Low disk space", notify=True)

    assert "summary" in response
    assert response["summary"] == "No Slack needed"
