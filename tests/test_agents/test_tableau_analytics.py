# tests/test_agents/test_tableau_analytics.py

import pytest
from unittest.mock import patch, MagicMock
from agents.tableau_analytics import TableauAnalytics


@patch("agents.tableau_analytics.TableauClient")
@patch("agents.tableau_analytics.LLMCollator")
def test_analyze_dashboards(mock_llm, mock_client):
    mock_client.return_value.list_dashboards.return_value = ["Sales Dashboard"]
    mock_client.return_value.get_dashboard_views.return_value = ["Revenue View", "Pipeline View"]

    agent = TableauAnalytics(config={"tableau": {}, "llms": {}})
    result = agent.analyze_dashboards()

    assert "Sales Dashboard" in result
    assert isinstance(result["Sales Dashboard"], list)
    assert "Revenue View" in result["Sales Dashboard"]


@patch("agents.tableau_analytics.TableauClient")
@patch("agents.tableau_analytics.LLMCollator")
def test_summarize_insights(mock_llm, mock_client):
    mock_client.return_value.get_dashboard_views.return_value = ["Overview", "KPIs"]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Looks healthy"}

    agent = TableauAnalytics(config={"tableau": {}, "llms": {}})
    result = agent.summarize_insights("My Dashboard")

    assert "summary" in result
