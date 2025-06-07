# agents/backlog_refiner.py

from agents.llm_collator import LLMCollator
from integrations.jira_client import JiraClient
from config.settings import load_settings
from typing import List, Dict, Any


class BacklogRefiner:
    """
    Assists in refining the Jira backlog by labeling, prioritizing, and merging.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.llm = LLMCollator(config.get("llms", {}))
        self.jira = JiraClient(config["jira"])

    def refine_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest priority, labels, merges, and clarification needs.
        """
        prompt = f"""
Review the following Jira issues and make suggestions to improve backlog health.

Issues:
{issues}

Suggest: Priority changes, label/tag adjustments, duplicates, or unclear tickets.
"""
        return self.llm.summarize_responses(prompt)
