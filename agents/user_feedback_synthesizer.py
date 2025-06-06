# agents/user_feedback_synthesizer.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class UserFeedbackSynthesizer:
    """
    Combines user feedback across sources into thematic summaries.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def synthesize_feedback(self, feedback_items: List[str], platform_tags: List[str]) -> Dict[str, Any]:
        """
        Generate a synthesized view of user feedback.
        """
        prompt = f"""
Synthesize the following user feedback collected across platforms: {platform_tags}

Feedback:
{feedback_items}

Identify common themes, pain points, and actionable recommendations.
"""
        return self.collator.summarize_responses(prompt)
