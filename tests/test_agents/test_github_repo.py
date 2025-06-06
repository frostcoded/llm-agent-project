# tests/test_agents/test_github_repo.py

import pytest
from agents.github_repo import GitHubRepoAgent

@pytest.fixture
def mock_config():
    return {
        "github": {"token": "fake-token", "base_url": "https://api.github.com"},
        "llms": {"openai": {"api_key": "test"}}
    }

def test_list_pull_requests(monkeypatch, mock_config):
    agent = GitHubRepoAgent(mock_config)

    def mock_get_prs(repo, state="open"):
        return [{"title": "Fix bug"}, {"title": "Add feature"}]

    monkeypatch.setattr(agent.client, "get_pull_requests", mock_get_prs)
    result = agent.list_pull_requests("test/repo")
    assert len(result) == 2
    assert result[0]["title"] == "Fix bug"

def test_analyze_repository(monkeypatch, mock_config):
    agent = GitHubRepoAgent(mock_config)

    monkeypatch.setattr(agent.client, "get_pull_requests", lambda repo: ["PR1", "PR2", "PR3"])
    monkeypatch.setattr(agent.client, "get_issues", lambda repo: ["Issue1", "Issue2"])
    monkeypatch.setattr(agent.collator, "summarize_responses", lambda prompt, context={}: {"summary": "Repo is active"})

    result = agent.analyze_repository("test/repo")
    assert result["summary"] == "Repo is active"
