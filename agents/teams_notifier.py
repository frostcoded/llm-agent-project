# agents/teams_notifier.py

from integrations.teams_client import TeamsClient
from config.settings import load_settings
from typing import Dict, Any, List


class TeamsNotifier:
    """
    Sends updates to Microsoft Teams for various workflow stages.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.teams = TeamsClient(config["teams"])

    def notify(self, recipients: List[str], message: str, subject: str = "Update") -> Dict[str, Any]:
        """
        Sends a formatted Teams message.
        """
        return self.teams.send_message(recipients, message, subject)
