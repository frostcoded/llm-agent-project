# agents/personality_profiler.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class PersonalityProfiler:
    """
    Builds and maintains personality profiles for individuals and teams.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_profile(self, messages: List[str], sender: str) -> Dict[str, Any]:
        """
        Creates a personality profile from user messages.
        """
        prompt = f"""
Analyze the following communications from {sender}.

Messages:
{messages}

Identify communication style, tone, strengths, and potential biases.
Output a structured personality profile.
"""
        return self.collator.summarize_responses(prompt)
