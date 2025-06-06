# tests/test_jira_project.py

import pytest
from unittest.mock import patch
from agents.jira_project import JiraProject


@patch("agents.jira_project.JiraClient")
@patch("agents.jira_project.LLMCollator")
def test_analyze_board(mock_llm, mock_client):
    mock_client.return_value.get_epics.return_value = [{"key": "EPIC-1"}]
    mock_client.return_value.get_sprints.return_value = [{"id": 123, "name": "Sprint 1"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Stable delivery pattern"}

    agent = JiraProject(config={"jira": {}, "llms": {}})
    result = agent.analyze_board(board_id=42)

    assert "summary" in result


@patch("agents.jira_project.JiraClient")
@patch("agents.jira_project.LLMCollator")
def test_sprint_health_check(mock_llm, mock_client):
    mock_client.return_value.get_issues_in_sprint.return_value = [{"key": "TASK-101"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "No blockers found"}

    agent = JiraProject(config={"jira": {}, "llms": {}})
    result = agent.sprint_health_check(board_id=42, sprint_id=7)

    assert isinstance(result, dict)
    assert "summary" in result
