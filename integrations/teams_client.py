# integrations/teams_client.py

import requests
from typing import Dict, List, Optional
from config.settings import load_settings


class TeamsClient:
    """
    Microsoft Teams client that uses the Microsoft Graph API.
    Supports sending messages to channels or chats and fetching basic channel metadata.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        if config is None:
            config = load_settings().get("teams", {})
        self.token = config.get("access_token")
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_message_to_channel(self, team_id: str, channel_id: str, message: str) -> Dict:
        """
        Posts a message to a specific channel in a team.
        """
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages"
        payload = {"body": {"content": message}}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def list_teams(self) -> List[Dict]:
        """
        Returns a list of Microsoft Teams the user is a member of.
        """
        url = f"{self.base_url}/me/joinedTeams"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def list_channels(self, team_id: str) -> List[Dict]:
        """
        Returns the list of channels within a team.
        """
        url = f"{self.base_url}/teams/{team_id}/channels"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def send_chat_message(self, recipient_id: str, message: str) -> Dict:
        """
        Sends a 1:1 chat message to a user by their ID.
        """
        # First create the chat (or assume chatId exists)
        chat_payload = {
            "chatType": "oneOnOne",
            "members": [
                {
                    "@odata.type": "#microsoft.graph.aadUserConversationMember",
                    "roles": ["owner"],
                    "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{recipient_id}')"
                }
            ]
        }
        chat_response = requests.post(f"{self.base_url}/chats", headers=self.headers, json=chat_payload)
        chat_response.raise_for_status()
        chat_id = chat_response.json().get("id")

        # Send message to chat
        message_url = f"{self.base_url}/chats/{chat_id}/messages"
        message_payload = {"body": {"content": message}}
        message_response = requests.post(message_url, headers=self.headers, json=message_payload)
        message_response.raise_for_status()
        return message_response.json()
