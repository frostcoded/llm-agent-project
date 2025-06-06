# agents/knowledge_base_updater.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class KnowledgeBaseUpdater:
    """
    Summarizes new data or tickets into structured documentation updates.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_kb_update(self, title: str, updates: str, target_audience: str = "engineering") -> Dict[str, Any]:
        prompt = f"""
Generate a knowledge base update titled '{title}' for the {target_audience} audience.

Content to summarize:
{updates}

Format it for clarity and reuse (bullet points, headings, links).
"""
        return self.collator.summarize_responses(prompt)
