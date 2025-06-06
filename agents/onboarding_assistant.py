# agents/onboarding_assistant.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any, List


class OnboardingAssistant:
    """
    Creates onboarding documentation and personalized introductions for new team members.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def create_onboarding_package(
        self,
        role: str,
        jira_boards: List[str],
        team_summary: str,
        docs: str,
        meeting_notes: str
    ) -> Dict[str, Any]:
        """
        Produces a role-specific onboarding document from key sources.
        """
        prompt = f"""
Create an onboarding package for a new {role}.
Include:
- Key Jira boards: {jira_boards}
- Team summary/personality profile: {team_summary}
- Core documentation: {docs}
- Summarized recent meetings: {meeting_notes}

Make it concise, informative, and welcoming.
"""
        return self.collator.summarize_responses(prompt)
