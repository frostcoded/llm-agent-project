# agents/automated_code_review.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class AutomatedCodeReviewer:
    """
    Performs automated code reviews using multiple LLMs.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def review_code(self, code_block: str, language: str = "python", context: str = "") -> Dict[str, Any]:
        """
        Review a given code block and return LLM-based suggestions.
        """
        prompt = f"""
Perform a detailed code review on the following {language} code:

{code_block}

Additional context: {context}

Point out bugs, code smells, improvements, and formatting issues. Provide suggestions.
"""
        return self.collator.summarize_responses(prompt)
