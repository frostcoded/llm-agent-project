# tests/test_agents/test_splunk_monitoring.py

import pytest
from unittest.mock import patch
from agents.splunk_monitoring import SplunkMonitoring


@patch("agents.splunk_monitoring.SplunkClient")
@patch("agents.splunk_monitoring.LLMCollator")
def test_summarize_logs(mock_llm, mock_client):
    mock_client.return_value.search.return_value = [{"event": "error: disk full"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Disk space issues detected"}

    agent = SplunkMonitoring(config={"splunk": {}, "llms": {}})
    result = agent.summarize_logs("error")

    assert isinstance(result, dict)
    assert "summary" in result
