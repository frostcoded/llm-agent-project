# agents/prd_generator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, List, Any


class PRDGenerator:
    """
    Generates Product Requirements Documents from Jira stories, sprints, or user input.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def generate_prd(self, sprint_name: str, stories: List[Dict[str, Any]], goals: str) -> Dict[str, Any]:
        """
        Builds a structured PRD from provided user stories and sprint goals.
        """
        prompt = f"""
Generate a Product Requirements Document (PRD) for sprint: {sprint_name}

Sprint Goals:
{goals}

User Stories:
{stories}

Include a summary, acceptance criteria, dependencies, and potential risks.
"""
        return self.collator.summarize_responses(prompt)
