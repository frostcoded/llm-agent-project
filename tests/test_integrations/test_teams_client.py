import pytest
from integrations.teams_client import TeamsClient

def test_teams_client_stub():
    client = TeamsClient(config={"webhook_url": "https://example.com"})
    assert hasattr(client, "send_message")
