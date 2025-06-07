# agents/jira_manager.py

from integrations.jira_client import JiraClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any, List


class JiraAgent:
    """
    Unified Jira agent for CRUD operations, sprint/epic data, and LLM-powered analysis.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = JiraClient(config.get("jira", {}))
        self.collator = LLMCollator(config.get("llms", {}))

    # ───────────────────────────────────────────────
    # CRUD and Posting
    # ───────────────────────────────────────────────

    def create_ticket(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task"
    ) -> Dict[str, Any]:
        return self.client.create_issue(project_key, summary, description, issue_type)

    def update_ticket(
        self,
        issue_key: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.client.update_issue(issue_key, fields)

    def get_ticket(self, issue_key: str) -> Dict[str, Any]:
        return self.client.get_issue(issue_key)

    def list_sprint_issues(
        self,
        board_id: str,
        sprint_id: str
    ) -> List[Dict[str, Any]]:
        return self.client.get_issues_for_sprint(board_id, sprint_id)

    def post_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        return self.client.add_comment(issue_key, comment)

    # ───────────────────────────────────────────────
    # LLM-Driven Insights
    # ───────────────────────────────────────────────

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
        return self.collator.summarize_responses(prompt)

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
        return self.collator.summarize_responses(prompt)
