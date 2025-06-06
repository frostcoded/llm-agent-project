# agents/meeting_summarizer.py

from config.settings import load_settings
from agents.llm_collator import LLMCollator
from integrations.teams_client import TeamsClient
from prompts.prompts import render_prompt
from typing import Dict, Any


class MeetingSummarizer:
    """
    Summarizes meeting transcripts and chat logs. Optionally uses reactions and action-item formatting.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.teams_client = TeamsClient(config.get("teams", {}))
        self.collator = LLMCollator(config.get("llms", {}))

    def summarize_meeting(
        self,
        meeting_id: str,
        reactions: Dict[str, int] = {},
        include_action_items: bool = True,
        context: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Generate a meeting summary using transcript + optional metadata like reactions.
        """
        transcript = self.teams_client.get_meeting_transcript(meeting_id)
        prompt = render_prompt("meeting_summary_prompt.txt", {
            "transcript": transcript,
            "reactions": reactions,
            "action_items": "Highlight them separately." if include_action_items else ""
        })
        return self.collator.summarize_responses(prompt=prompt, context=context)

    def summarize_highlighted_segments(self, meeting_id: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        highlights = self.teams_client.get_highlighted_segments(meeting_id)
        prompt = render_prompt("meeting_summary_prompt.txt", {
            "transcript": highlights,
            "reactions": {},
            "action_items": ""
        })
        return self.collator.summarize_responses(prompt=prompt, context=context)
