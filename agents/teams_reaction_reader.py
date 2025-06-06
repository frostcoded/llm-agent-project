# agents/teams_reaction_reader.py

from integrations.teams_client import TeamsClient
from config.settings import load_settings
from typing import Dict, Any


class TeamsReactionReader:
    """
    Reads message reactions in Microsoft Teams to assess relevance or sensitivity.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.teams = TeamsClient(config["teams"])

    def get_reactions(self, message_id: str) -> Dict[str, Any]:
        """
        Fetch reactions to a message.
        """
        return self.teams.fetch_reactions(message_id)

    def interpret_reactions(self, reactions: Dict[str, int]) -> Dict[str, Any]:
        """
        Score reactions to guide importance or confidentiality.
        """
        score = sum(reactions.values())
        confidential = reactions.get("👀", 0) > 0 or reactions.get("🔒", 0) > 0
        return {
            "priority_score": score,
            "sensitive_content": confidential,
            "raw": reactions
        }
