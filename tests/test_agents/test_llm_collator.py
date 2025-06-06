# tests/test_agents/test_llm_collator.py

import pytest
from agents.llm_collator import LLMCollator

@pytest.fixture
def basic_config():
    return {
        "openai": {
            "enabled": True,
            "api_key": "test",
            "model": "gpt-4"
        }
    }

def test_collect_responses_structure(basic_config):
    collator = LLMCollator(basic_config)
    results = collator.collect_responses("What is the capital of France?")
    assert isinstance(results, list)
    for response in results:
        assert "source" in response
