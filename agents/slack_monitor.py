# agents/slack_monitor.py

from integrations.slack_client import SlackClient
from agents.llm_collator import LLMCollator
from agents.slack_notifier import SlackNotifier
from config.settings import load_settings
from prompts.prompts import render_prompt
from typing import Dict, Any, List


class SlackMonitor:
    """
    Monitors Slack channels for recent activity and summarizes sentiment or issues using LLMs.
    Can optionally notify channels when insights warrant attention.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = SlackClient(config.get("slack", {}))
        self.collator = LLMCollator(config.get("llms", {}))
        self.notifier = SlackNotifier(config)

    def fetch_recent_messages(self, channel: str, limit: int = 20) -> List[str]:
        return self.client.get_messages(channel, limit=limit)

    def analyze_channel(self, channel: str, context: Dict[str, Any] = {}) -> Dict:
        messages = self.fetch_recent_messages(channel)
        prompt = render_prompt("slack_sentiment_prompt.txt", {
            "channel": channel,
            "messages": messages
        })
        return self.collator.summarize_responses(prompt, context)

    def notify_if_needed(self, analysis: Dict, channel: str):
        if "alert" in analysis.get("summary", "").lower():
            message = f":rotating_light: Slack Monitor Alert:\n{analysis['summary']}"
            self.notifier.notify(message, channel)
