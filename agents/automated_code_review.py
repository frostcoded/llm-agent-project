# agents/automated_code_review.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from prompts.prompts import render_prompt
from utils.logger import logger
from typing import Dict, Any


class AutomatedCodeReviewer:
    """
    Performs automated code reviews using LLM feedback aggregation.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def review_code(self, code_block: str, language: str = "python", context: str = "", review_style: str = "general") -> Dict[str, Any]:
        """
        Review a given code block using a configurable prompt.
        """
        prompt = render_prompt("code_review_prompt.txt", {
            "language": language,
            "code_block": code_block,
            "context": context,
            "review_style": review_style
        })

        logger.info("Performing automated code review...")
        result = self.collator.summarize_responses(prompt)

        return {
            "review_style": review_style,
            "suggestions": result.get("summary", "No suggestions returned.")
        }
