# integrations/dynamics_client.py

import requests
from typing import Dict, List


class DynamicsClient:
    """
    Connects to Microsoft Dynamics 365 to fetch CRM records like leads and opportunities.
    """

    def __init__(self, config: Dict[str, str]):
        self.base_url = config.get("base_url")
        self.access_token = config.get("access_token")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_leads(self, top: int = 5) -> List[Dict]:
        url = f"{self.base_url}/api/data/v9.2/leads?$top={top}"
        response = requests.get(url, headers=self.headers)
        return response.json().get("value", [])

    def get_opportunities(self, top: int = 5) -> List[Dict]:
        url = f"{self.base_url}/api/data/v9.2/opportunities?$top={top}"
        response = requests.get(url, headers=self.headers)
        return response.json().get("value", [])
