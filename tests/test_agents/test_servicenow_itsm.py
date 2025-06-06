# tests/test_agents/test_servicenow_itsm.py

import pytest
from unittest.mock import patch
from agents.servicenow_itsm import ServiceNowITSM


@patch("agents.servicenow_itsm.ServiceNowClient")
@patch("agents.servicenow_itsm.LLMCollator")
def test_summarize_incidents(mock_llm, mock_client):
    mock_client.return_value.get_incidents.return_value = [{"number": "INC001", "short_description": "Login error"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Recurring auth issue"}

    agent = ServiceNowITSM(config={"servicenow": {}, "llms": {}})
    result = agent.summarize_incidents()

    assert isinstance(result, dict)
    assert "summary" in result


@patch("agents.servicenow_itsm.ServiceNowClient")
@patch("agents.servicenow_itsm.LLMCollator")
def test_summarize_changes(mock_llm, mock_client):
    mock_client.return_value.get_changes.return_value = [{"number": "CHG001", "risk": "Medium"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Stable change flow"}

    agent = ServiceNowITSM(config={"servicenow": {}, "llms": {}})
    result = agent.summarize_changes()

    assert "summary" in result
