# tests/test_dynamics_crm.py

import pytest
from unittest.mock import patch
from agents.dynamics_crm_agent import DynamicsCRMAgent


@patch("agents.dynamics_crm.DynamicsClient")
@patch("agents.dynamics_crm.LLMCollator")
def test_analyze_leads(mock_llm, mock_client):
    mock_client.return_value.get_leads.return_value = [{"topic": "Interest in AI"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Strong tech sector leads"}

    agent = DynamicsCRM(config={"dynamics": {}, "llms": {}})
    result = agent.analyze_leads()

    assert isinstance(result, dict)
    assert "summary" in result


@patch("agents.dynamics_crm.DynamicsClient")
@patch("agents.dynamics_crm.LLMCollator")
def test_analyze_opportunities(mock_llm, mock_client):
    mock_client.return_value.get_opportunities.return_value = [{"name": "AI Deployment", "status": "Open"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Good pipeline velocity"}

    agent = DynamicsCRM(config={"dynamics": {}, "llms": {}})
    result = agent.analyze_opportunities()

    assert isinstance(result, dict)
    assert "summary" in result
