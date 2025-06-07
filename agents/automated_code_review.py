# agents/automated_code_review.py

from agents.llm_factory import get_collator
from config.settings import load_settings
from utils.logger import logger
from typing import Dict, Any
from prompts.prompts import render_prompt


class AutomatedCodeReviewer:
    """
    Performs automated code reviews using a collator (LLM or mock).
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = get_collator(config)
        self.config = config

    def review_code(
        self,
        code_block: str,
        language: str = "python",
        context: str = "",
        review_style: str = "general"
    ) -> Dict[str, Any]:
        """
        Review a given code block using a contextual LLM prompt.
        Returns summarized suggestions.
        """
        logger.info(f"[CodeReview] Reviewing code in language: {language} | Style: {review_style}")

        prompt = render_prompt("code_review_prompt.txt", {
            "language": language,
            "code_block": code_block,
            "context": context,
            "review_style": review_style
        })

        result = self.collator.summarize_responses(prompt)

        return {
            "review_style": review_style,
            "language": language,
            "suggestions": result.get("summary", "No suggestions returned.")
        }
