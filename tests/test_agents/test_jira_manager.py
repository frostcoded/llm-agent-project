import pytest
from agents.jira_manager import JiraAgent

@pytest.fixture
def mock_config():
    return {
        "jira": {"api_key": "test", "base_url": "https://fake.jira.com"},
        "llms": {"openai": {"api_key": "test"}}
    }

def test_create_ticket(monkeypatch, mock_config):
    agent = JiraAgent(mock_config)

    def mock_create_issue(project_key, summary, description, issue_type):
        return {"key": "PROJ-123", "summary": summary}

    monkeypatch.setattr(agent.client, "create_issue", mock_create_issue)
    result = agent.create_ticket("PROJ", "Test Summary", "Test Description")

    assert result["key"] == "PROJ-123"
    assert result["summary"] == "Test Summary"

def test_analyze_board(monkeypatch, mock_config):
    agent = JiraAgent(mock_config)

    monkeypatch.setattr(agent.client, "get_epics", lambda board_id: ["Epic1", "Epic2", "Epic3"])
    monkeypatch.setattr(agent.client, "get_sprints", lambda board_id: ["Sprint1", "Sprint2", "Sprint3"])
    monkeypatch.setattr(agent.collator, "summarize_responses", lambda prompt: {"summary": "OK"})

    result = agent.analyze_board(1)
    assert "summary" in result

def test_sprint_health_check(monkeypatch, mock_config):
    agent = JiraAgent(mock_config)

    monkeypatch.setattr(agent.client, "get_issues_in_sprint", lambda sprint_id: ["Issue1", "Issue2", "Issue3"])
    monkeypatch.setattr(agent.collator, "summarize_responses", lambda prompt: {"health": "Good"})

    result = agent.sprint_health_check(1, 2)
    assert result["health"] == "Good"
