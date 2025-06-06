import pytest
from agents.jira_manager import JiraManager

@pytest.fixture
def mock_config():
    return {
        "jira": {
            "url": "https://fake.atlassian.net",
            "username": "test_user",
            "api_token": "fake_token"
        }
    }

def test_jira_manager_has_methods(mock_config):
    manager = JiraManager(mock_config)
    assert hasattr(manager, "create_ticket")
    assert hasattr(manager, "update_ticket")
    assert hasattr(manager, "get_ticket")
