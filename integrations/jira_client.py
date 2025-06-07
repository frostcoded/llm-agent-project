# integrations/jira_client.py

import requests
from typing import Dict, Any, List, Optional
from config.settings import load_settings


class JiraClient:
    """
    Handles integration with the Jira REST API.
    Supports operations such as creating issues, retrieving boards/sprints, and posting comments.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        if config is None:
            config = load_settings().get("jira", {})
        self.base_url = config.get("url", "").rstrip("/")
        self.email = config.get("email")
        self.api_token = config.get("api_token")
        self.headers = {
            "Content-Type": "application/json"
        }

    def _auth(self):
        return (self.email, self.api_token)

    def _url(self, path: str) -> str:
        return f"{self.base_url}/rest/api/3/{path.lstrip('/')}"

    def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        }
        response = requests.post(self._url("issue"), json=payload, auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"fields": fields}
        response = requests.put(self._url(f"issue/{issue_key}"), json=payload, auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        response = requests.get(self._url(f"issue/{issue_key}"), auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        payload = {"body": comment}
        response = requests.post(self._url(f"issue/{issue_key}/comment"), json=payload, auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_boards(self) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/rest/agile/1.0/board", auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json().get("values", [])

    def get_sprints(self, board_id: int) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint", auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json().get("values", [])

    def get_epics(self, board_id: int) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/rest/agile/1.0/board/{board_id}/epic", auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json().get("values", [])

    def get_issues_for_sprint(self, board_id: str, sprint_id: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/rest/agile/1.0/board/{board_id}/sprint/{sprint_id}/issue"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json().get("issues", [])

    def get_issues_in_sprint(self, sprint_id: int) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        response.raise_for_status()
        return response.json().get("issues", [])
