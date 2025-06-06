# agents/meeting_summarizer.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class MeetingSummarizer:
    """
    Summarizes meeting discussions based on audio transcripts and/or Teams chat logs.
    Reactions are used to prioritize important points.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def summarize_meeting(self, transcript: str, reactions: Dict[str, int] = {}, include_action_items: bool = True) -> Dict[str, Any]:
        """
        Generate a summary from transcript and optional reactions metadata.
        """
        prompt = f"""
Summarize the following meeting transcript:
{transcript}

Reactions (importance signals): {reactions}

Include clear action items if any were discussed.
{"Highlight them separately." if include_action_items else ""}
"""
        return self.collator.summarize_responses(prompt)
