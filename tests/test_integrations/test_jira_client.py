import pytest
from integrations.jira_client import JiraClient

def test_jira_client_stub():
    client = JiraClient(config={"url": "https://fake.atlassian.net"})
    assert hasattr(client, "create_issue")
