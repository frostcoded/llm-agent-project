# integrations/servicenow_client.py

import requests
from typing import Dict, List


class ServiceNowClient:
    """
    Connects to ServiceNow to query incidents, changes, or CMDB entries.
    """

    def __init__(self, config: Dict[str, str]):
        self.base_url = config.get("base_url")
        self.username = config.get("username")
        self.password = config.get("password")
        self.headers = {"Content-Type": "application/json"}

    def _auth(self):
        return (self.username, self.password)

    def get_incidents(self, state: str = "all", limit: int = 5) -> List[Dict]:
        query = f"state={state}" if state != "all" else ""
        url = f"{self.base_url}/api/now/table/incident?{query}&sysparm_limit={limit}"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        return response.json().get("result", [])

    def get_changes(self, limit: int = 5) -> List[Dict]:
        url = f"{self.base_url}/api/now/table/change_request?sysparm_limit={limit}"
        response = requests.get(url, auth=self._auth(), headers=self.headers)
        return response.json().get("result", [])
