# tests/test_agents/test_code_generator.py

import pytest
from agents.code_generator import CodeGenerator

@pytest.fixture
def mock_code_generator():
    return CodeGenerator(config={"openai": {"enabled": False}})

def test_generate_code_basic(mock_code_generator):
    result = mock_code_generator.generate_code("Write a Python function to add two numbers.")
    assert isinstance(result, list)
    assert all("source" in r for r in result)
