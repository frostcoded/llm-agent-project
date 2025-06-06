# agents/jira_manager.py

from integrations.jira_client import JiraClient
from config.settings import load_settings
from typing import Dict, Any, List


class JiraManager:
    """
    High-level interface to manage Jira projects, sprints, stories, epics, and more.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.jira = JiraClient(config["jira"])

    def create_ticket(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        return self.jira.create_issue(project_key, summary, description, issue_type)

    def update_ticket(self, issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        return self.jira.update_issue(issue_key, fields)

    def get_ticket(self, issue_key: str) -> Dict[str, Any]:
        return self.jira.get_issue(issue_key)

    def list_sprint_issues(self, board_id: str, sprint_id: str) -> List[Dict[str, Any]]:
        return self.jira.get_issues_for_sprint(board_id, sprint_id)
