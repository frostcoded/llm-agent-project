# integrations/splunk_client.py

import requests
from typing import Dict, List


class SplunkClient:
    """
    Queries log and event data from Splunk using its REST API.
    """

    def __init__(self, config: Dict[str, str]):
        self.base_url = config.get("base_url")
        self.token = config.get("token")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def search(self, query: str, earliest: str = "-1h", latest: str = "now") -> List[Dict]:
        """
        Executes a Splunk search query.
        """
        url = f"{self.base_url}/services/search/jobs"
        payload = {
            "search": f"search {query}",
            "earliest_time": earliest,
            "latest_time": latest",
            "output_mode": "json"
        }
        response = requests.post(url, headers=self.headers, data=payload)
        sid = response.json().get("sid")

        # Poll results
        results_url = f"{self.base_url}/services/search/jobs/{sid}/results?output_mode=json"
        results = requests.get(results_url, headers=self.headers)
        return results.json().get("results", [])
