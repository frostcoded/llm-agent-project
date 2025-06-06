# test/tests/test_agents/test_workflow_effiency.py

import pytest
from agents.workflow_efficiency import WorkflowEfficiencyAgent

@pytest.fixture
def mock_config():
    return {
        "jira": {"api_key": "fake", "base_url": "https://jira.test"},
        "github": {"token": "gh_fake", "base_url": "https://api.github.com"},
        "llms": {"openai": {"api_key": "fake"}}
    }

def test_analyze_efficiency(monkeypatch, mock_config):
    agent = WorkflowEfficiencyAgent(mock_config)

    monkeypatch.setattr(agent.jira, "get_issues_for_board", lambda board_id: ["Jira1", "Jira2", "Jira3"])
    monkeypatch.setattr(agent.github, "get_pull_requests", lambda repo: ["PR1", "PR2"])
    monkeypatch.setattr(agent.collator, "summarize_responses", lambda prompt: {"efficiency": "Optimal"})

    result = agent.analyze_efficiency(1, "example/repo")
    assert "efficiency" in result
    assert result["efficiency"] == "Optimal"
