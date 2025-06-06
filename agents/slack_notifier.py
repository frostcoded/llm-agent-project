# agents/slack_notifier.py

from integrations.slack_client import SlackClient
from config.settings import load_settings
from typing import List, Dict

class SlackNotifier:
    def __init__(self, config: Dict = None):
        if config is None:
            config = load_settings()
        self.slack = SlackClient(config.get("slack", {}))

    def notify(self, message: str, channel: str = "#general") -> Dict:
        return self.slack.send_message(channel, message)
