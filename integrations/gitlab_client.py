# integrations/gitlab_client.py

import requests
from typing import Dict


class GitLabClient:
    """
    GitLab API client to interact with projects, issues, and pipelines.
    """

    def __init__(self, config: Dict[str, str]):
        self.token = config.get("api_token")
        self.base_url = config.get("base_url", "https://gitlab.com/api/v4")
        self.headers = {
            "PRIVATE-TOKEN": self.token
        }

    def create_issue(self, project_id: str, title: str, description: str) -> Dict:
        url = f"{self.base_url}/projects/{project_id}/issues"
        data = {"title": title, "description": description}
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_merge_requests(self, project_id: str, state: str = "opened") -> Dict:
        url = f"{self.base_url}/projects/{project_id}/merge_requests"
        response = requests.get(url, headers=self.headers, params={"state": state})
        return response.json()
