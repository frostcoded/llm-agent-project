# agents/incident_responder.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class IncidentResponder:
    """
    Detects and proposes remediation for operational or security incidents.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def respond_to_alert(self, alert_log: str, system_context: str = "") -> Dict[str, Any]:
        prompt = f"""
Analyze the following incident log:

{alert_log}

System Context:
{system_context}

Diagnose the issue, assess its impact, and recommend specific remediation steps.
"""
        return self.collator.summarize_responses(prompt)
