# integrations/slack_client.py

import requests
from typing import List, Dict


class SlackClient:
    """
    Simple Slack client to send messages via webhook or Bot Token.
    """

    def __init__(self, config: Dict[str, str]):
        self.webhook_url = config.get("webhook_url")
        self.token = config.get("bot_token")

    def send_message(self, channel: str, message: str) -> Dict:
        if self.token:
            return self._send_via_bot(channel, message)
        return self._send_via_webhook(message)

    def _send_via_webhook(self, message: str) -> Dict:
        response = requests.post(self.webhook_url, json={"text": message})
        return {"status": response.status_code, "response": response.text}

    def _send_via_bot(self, channel: str, message: str) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "channel": channel,
            "text": message
        }
        response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=data)
        return response.json()
