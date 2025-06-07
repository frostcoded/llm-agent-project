# tests/test_agents/test_competitor_analysis.py

import pytest
from unittest.mock import patch, MagicMock
from agents.competitor_analysis import CompetitorAnalysisAgent


@pytest.fixture
def agent():
    return CompetitorAnalysisAgent(config={"openai": {"enabled": False}})


@patch("agents.competitor_analysis.render_prompt")
@patch("agents.competitor_analysis.LLMCollator")
def test_competitor_analysis_valid_input(mock_collator_cls, mock_render, agent):
    mock_collator = MagicMock()
    mock_collator.summarize_responses.return_value = {
        "summary": "Company is strong in AI",
        "confidence": "high"
    }
    mock_collator_cls.return_value = mock_collator
    mock_render.return_value = "Rendered prompt content"

    result = agent.analyze(
        company_name="Acme Corp",
        competitors=["Beta Inc", "Gamma LLC"],
        internal_data="Acme has 90% feature adoption",
        external_data="Beta announced layoffs",
        period="Q1 2024"
    )

    mock_render.assert_called_once()
    mock_collator.summarize_responses.assert_called_once_with("Rendered prompt content")
    assert "summary" in result
    assert result["confidence"] == "high"


@patch("agents.competitor_analysis.render_prompt")
@patch("agents.competitor_analysis.LLMCollator")
def test_competitor_analysis_handles_empty_input(mock_collator_cls, mock_render, agent):
    result = agent.analyze(company_name="", competitors=[])

    assert result["summary"] == "Missing input data"
    assert result["confidence"] == "low"
    mock_render.assert_not_called()
    mock_collator_cls.assert_not_called()


@patch("agents.competitor_analysis.render_prompt")
@patch("agents.competitor_analysis.LLMCollator")
def test_competitor_analysis_handles_partial_data(mock_collator_cls, mock_render, agent):
    mock_collator = MagicMock()
    mock_collator.summarize_responses.return_value = {"summary": "Needs more data", "confidence": "medium"}
    mock_collator_cls.return_value = mock_collator
    mock_render.return_value = "Partial prompt"

    result = agent.analyze(
        company_name="Acme Corp",
        competitors=["Beta Inc"],
        external_data="",
        internal_data=""
    )

    assert isinstance(result, dict)
    assert "summary" in result
