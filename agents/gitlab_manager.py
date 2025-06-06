# agents/gitlab_manager.py

from integrations.gitlab_client import GitLabClient
from config.settings import load_settings
from typing import Dict

class GitLabManager:
    def __init__(self, config: Dict = None):
        if config is None:
            config = load_settings()
        self.client = GitLabClient(config.get("gitlab", {}))

    def create_issue(self, project_id: str, title: str, description: str) -> Dict:
        return self.client.create_issue(project_id, title, description)

    def list_merge_requests(self, project_id: str) -> Dict:
        return self.client.get_merge_requests(project_id)
