# integrations/outlook_client.py

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config.settings import load_settings


class OutlookClient:
    """
    Integrates with Microsoft Outlook Calendar via Microsoft Graph API.
    Supports reading and creating calendar events.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        if config is None:
            config = load_settings().get("outlook", {})
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.token = config.get("access_token")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def list_events(self, start_time: datetime, end_time: datetime, user_id: str = "me") -> List[Dict]:
        """
        Lists calendar events for the given time range.
        """
        url = f"{self.base_url}/users/{user_id}/calendarView"
        params = {
            "startDateTime": start_time.isoformat(),
            "endDateTime": end_time.isoformat()
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("value", [])

    def create_event(
        self,
        subject: str,
        start_time: datetime,
        end_time: datetime,
        body: str = "",
        location: str = "",
        attendees: Optional[List[str]] = None,
        user_id: str = "me"
    ) -> Dict:
        """
        Creates a calendar event.
        """
        attendees_list = []
        if attendees:
            attendees_list = [{"emailAddress": {"address": email}, "type": "required"} for email in attendees]

        payload = {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
            "location": {"displayName": location},
            "attendees": attendees_list
        }

        url = f"{self.base_url}/users/{user_id}/events"
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_event(self, event_id: str, user_id: str = "me") -> bool:
        """
        Deletes a calendar event by ID.
        """
        url = f"{self.base_url}/users/{user_id}/events/{event_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return True
        response.raise_for_status()
        return False
