# agents/code_generator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from prompts.prompts import render_prompt
from utils.logger import logger
from typing import List, Dict, Any


class CodeGenerator:
    """
    Generates code using LLMs via LLMCollator and prompt templates.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_code(self, task_description: str, context: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Generates code using rendered prompt and returns all LLM responses.
        """
        if not task_description:
            logger.warning("No task description provided.")
            return []

        prompt = render_prompt("code_generation_prompt.txt", {"task": task_description})
        logger.debug(f"[CodeGenerator] Generated prompt: {prompt[:200]}...")
        return self.collator.collect_responses(prompt=prompt, context=context)

    def generate_and_summarize(self, task_description: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Generates code and returns a summarized LLM response.
        """
        if not task_description:
            logger.warning("No task description provided.")
            return {"summary": "No task provided", "response": None}

        prompt = render_prompt("code_generation_prompt.txt", {"task": task_description})
        logger.debug(f"[CodeGenerator] Summarizing for task: {task_description}")
        return self.collator.summarize_responses(prompt=prompt, context=context)
