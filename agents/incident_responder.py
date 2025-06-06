# agents/incident_responder.py

from agents.llm_collator import LLMCollator
from agents.slack_notifier import SlackNotifier
from config.settings import load_settings
from typing import Dict, Any


class IncidentResponder:
    """
    Detects and proposes remediation for operational or security incidents using LLM.
    Can optionally send a Slack alert when configured.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.llm = LLMCollator(config.get("llms", {}))
        self.slack = SlackNotifier(config) if config.get("slack", {}).get("enabled", False) else None

    def respond_to_alert(self, alert_log: str, system_context: str = "", notify: bool = True) -> Dict[str, Any]:
        prompt = f"""\
Analyze the following incident log:

{alert_log}

System Context:
{system_context}

Diagnose the issue, assess its impact, and recommend specific remediation steps.
"""
        result = self.llm.summarize_responses(prompt)

        if notify and self.slack:
            summary = result.get("summary", "No summary provided.")
            alert_message = f"🚨 Incident detected:\n{alert_log[:100]}...\n\nSummary: {summary}"
            self.slack.notify(alert_message)

        return result
