# agents/doc_generator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class DocGenerator:
    """
    Generates technical or process documentation using LLMs.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_document(self, title: str, purpose: str, target_audience: str, content_outline: str) -> Dict[str, Any]:
        """
        Generate a full-length document based on input.
        """
        prompt = f"""
Generate documentation titled: "{title}".

Purpose: {purpose}
Target Audience: {target_audience}
Content Outline:
{content_outline}

Include headings, examples, and explanations where relevant.
"""
        return self.collator.summarize_responses(prompt)
