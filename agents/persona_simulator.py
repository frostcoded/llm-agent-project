# agents/persona_simulator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class PersonaSimulator:
    """
    Simulates different communication styles or voices based on persona profiles.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def simulate_persona_output(self, persona: str, content_goal: str, topic: str) -> Dict[str, Any]:
        """
        Generates an output styled in the manner of a given persona.
        """
        prompt = f"""
Write the following content as if authored by the persona: {persona}
Topic: {topic}
Goal: {content_goal}

Match tone, word choice, and structure accordingly.
"""
        return self.collator.summarize_responses(prompt)
