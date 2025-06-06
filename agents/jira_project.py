# agents/jira_project.py

from integrations.jira_client import JiraClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class JiraProject:
    """
    Provides insights into Jira project health, sprint trends, and epic progress.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = JiraClient(config.get("jira", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def analyze_board(self, board_id: int) -> Dict:
        epics = self.client.get_epics(board_id)
        sprints = self.client.get_sprints(board_id)
        prompt = f"""
Project Analysis Report for Jira Board {board_id}

Epics:
{epics[:3]}

Sprints:
{sprints[:3]}

Please evaluate delivery velocity, epic completion rate, and project risk.
Highlight delays, blockers, or scope creep if found.
"""
        return self.llm.summarize_responses(prompt)

    def sprint_health_check(self, board_id: int, sprint_id: int) -> Dict:
        issues = self.client.get_issues_in_sprint(sprint_id)
        prompt = f"""
Sprint Health Report

Board ID: {board_id}
Sprint ID: {sprint_id}

Sprint Issues:
{issues[:5]}

Summarize team performance, risk of spillover, and story quality.
"""
        return self.llm.summarize_responses(prompt)
