# agents/release_coordinator.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class ReleaseCoordinator:
    """
    Plans and coordinates software releases based on availability and team roles.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def plan_release(self, release_name: str, team_availability: Dict[str, str], roles: Dict[str, str], historical_notes: str = "") -> Dict[str, Any]:
        """
        Assigns and schedules a release based on team availability and role fit.
        """
        prompt = f"""
Plan a software release titled '{release_name}'.

Team Availability:
{team_availability}

Roles:
{roles}

Historical release data (if any):
{historical_notes}

Assign responsibilities and recommend a release window.
"""
        return self.collator.summarize_responses(prompt)
