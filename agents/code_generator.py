# agents/code_generator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class CodeGenerator:
    """
    Generates code snippets using one or more LLM backends via the LLMCollator.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_code(self, task_description: str, context: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Generates code based on the provided description or prompt.
        Returns all LLM responses for review.
        """
        return self.collator.collect_responses(prompt=task_description, context=context)

    def generate_and_summarize(self, task_description: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Generates code and provides a summary of all responses.
        """
        return self.collator.summarize_responses(prompt=task_description, context=context)
