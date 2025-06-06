# agents/test_case_generator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class TestCaseGenerator:
    """
    Generates test cases based on PRD, user stories, or goals.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_test_cases(self, requirements_doc: str) -> Dict[str, Any]:
        """
        Converts a requirements document into test cases.
        """
        prompt = f"""
Based on the following product requirements, generate test cases:

{requirements_doc}

Format using Given/When/Then or another clear testing structure.
"""
        return self.collator.summarize_responses(prompt)
