# agents/jira_poster.py

from integrations.jira_client import JiraClient
from config.settings import load_settings
from typing import Dict


class JiraPoster:
    """
    Posts issues, comments, and updates to Jira.
    """

    def __init__(self, config: Dict[str, str] = None):
        if config is None:
            config = load_settings()
        self.jira = JiraClient(config["jira"])

    def post_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict:
        return self.jira.create_issue(project_key, summary, description, issue_type)

    def post_comment(self, issue_key: str, comment: str) -> Dict:
        return self.jira.add_comment(issue_key, comment)
