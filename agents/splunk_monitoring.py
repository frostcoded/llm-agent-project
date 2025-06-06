# agents/splunk_monitoring.py

from integrations.splunk_client import SplunkClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class SplunkMonitoring:
    """
    Monitors Splunk logs and summarizes incidents, alerts, and error patterns.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = SplunkClient(config.get("splunk", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def summarize_logs(self, query: str, earliest: str = "-1h", latest: str = "now") -> Dict:
        logs = self.client.search(query, earliest, latest)
        prompt = f"""
You are a security and reliability analyst. Summarize the following Splunk logs:

{logs[:5]}

Highlight notable anomalies, frequent error codes, or spike patterns.
Recommend any action items based on the content.
"""
        return self.llm.summarize_responses(prompt)
