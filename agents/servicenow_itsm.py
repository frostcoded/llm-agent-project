# agents/servicenow_itsm.py

from integrations.servicenow_client import ServiceNowClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class ServiceNowITSM:
    """
    Summarizes ITSM incident and change records for insights and alerts.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = ServiceNowClient(config.get("servicenow", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def summarize_incidents(self, state: str = "all") -> Dict:
        data = self.client.get_incidents(state)
        prompt = f"""
Review the following ITSM incident tickets from ServiceNow:

{data[:5]}

Summarize root causes, affected systems, and possible remediations.
Highlight recurring issues if any.
"""
        return self.llm.summarize_responses(prompt)

    def summarize_changes(self) -> Dict:
        data = self.client.get_changes()
        prompt = f"""
Analyze the following recent change records from ServiceNow:

{data[:5]}

Assess impact risk, approval patterns, and any implementation delays.
"""
        return self.llm.summarize_responses(prompt)
