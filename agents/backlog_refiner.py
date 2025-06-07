# agents/backlog_refiner.py

from agents.llm_factory import get_collator
from integrations.jira_client import JiraClient
from config.settings import load_settings
from utils.logger import logger
from prompts.prompts import render_prompt
from typing import List, Dict, Any


class BacklogRefiner:
    """
    Assists in refining the Jira backlog by labeling, prioritizing, and merging.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.llm = get_collator(config.get("llms", {}))
        self.jira = JiraClient(config["jira"])

    def refine_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest priority, labels, merges, and clarification needs.
        """
        if not issues:
            return {"summary": "No issues provided.", "suggestions": []}

        logger.info(f"[BacklogRefiner] Refining {len(issues)} issues...")

        prompt = render_prompt("backlog_refinement_prompt.txt", {"issues": issues})

        result = self.llm.summarize_responses(prompt)

        return {
            "summary": result.get("summary", ""),
            "suggestions": result.get("suggestions", []),
            "confidence": result.get("confidence", 0.0)
        }
