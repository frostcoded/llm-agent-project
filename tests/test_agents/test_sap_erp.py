# tests/test_sap_erp.py

import pytest
from unittest.mock import patch
from agents.sap_erp_agent import SAPERPAgent


@patch("agents.sap_erp.SAPClient")
@patch("agents.sap_erp.LLMCollator")
def test_analyze_purchases(mock_llm, mock_client):
    mock_client.return_value.get_purchase_orders.return_value = [{"id": "P1001", "vendor": "Acme"}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "High spend detected"}

    agent = SAPERP(config={"sap": {}, "llms": {}})
    result = agent.analyze_purchases()

    assert "summary" in result


@patch("agents.sap_erp.SAPClient")
@patch("agents.sap_erp.LLMCollator")
def test_analyze_sales(mock_llm, mock_client):
    mock_client.return_value.get_sales_orders.return_value = [{"id": "S2002", "customer": "Widget Inc."}]
    mock_llm.return_value.summarize_responses.return_value = {"summary": "Consistent sales growth"}

    agent = SAPERP(config={"sap": {}, "llms": {}})
    result = agent.analyze_sales()

    assert isinstance(result, dict)
    assert "summary" in result
