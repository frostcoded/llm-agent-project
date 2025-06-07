# tests/test_agents/test_code_generator.py

import pytest
from unittest.mock import patch, MagicMock
from agents.code_generator import CodeGenerator

@pytest.fixture
def code_generator():
    return CodeGenerator(config={"openai": {"enabled": False}})

@patch("agents.code_generator.render_prompt")
@patch("agents.code_generator.LLMCollator")
def test_generate_code_basic(mock_collator_cls, mock_render, code_generator):
    mock_collator = MagicMock()
    mock_collator.collect_responses.return_value = [{"source": "mock", "code": "def add(a, b): return a + b"}]
    mock_collator_cls.return_value = mock_collator
    mock_render.return_value = "Mock rendered prompt"

    result = code_generator.generate_code("Write a function to add numbers.")
    
    mock_render.assert_called_once_with("code_generation_prompt.txt", {"task": "Write a function to add numbers."})
    mock_collator.collect_responses.assert_called_once()
    
    assert isinstance(result, list)
    assert "source" in result[0]

@patch("agents.code_generator.render_prompt")
@patch("agents.code_generator.LLMCollator")
def test_generate_and_summarize_basic(mock_collator_cls, mock_render, code_generator):
    mock_collator = MagicMock()
    mock_collator.summarize_responses.return_value = {"summary": "It adds numbers", "response": "def add..."}
    mock_collator_cls.return_value = mock_collator
    mock_render.return_value = "Mock prompt"

    result = code_generator.generate_and_summarize("Create a Python script that sums a list.")

    mock_render.assert_called_once_with("code_generation_prompt.txt", {"task": "Create a Python script that sums a list."})
    mock_collator.summarize_responses.assert_called_once()

    assert isinstance(result, dict)
    assert "summary" in result

def test_generate_code_empty_input(code_generator):
    result = code_generator.generate_code("")
    assert result == []

def test_generate_and_summarize_empty_input(code_generator):
    result = code_generator.generate_and_summarize("")
    assert isinstance(result, dict)
    assert result["summary"] == "No task provided"
