# agents/dynamics_crm.py

from integrations.dynamics_client import DynamicsClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class DynamicsCRM:
    """
    Analyzes CRM activity from Microsoft Dynamics 365 for sales and customer insights.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = DynamicsClient(config.get("dynamics", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def analyze_leads(self) -> Dict:
        leads = self.client.get_leads()
        prompt = f"""
Here is a summary of recent leads from Dynamics CRM:

{leads[:5]}

Please identify trends in lead sources, common industries, and readiness to convert.
Suggest optimizations to improve lead quality or nurturing.
"""
        return self.llm.summarize_responses(prompt)

    def analyze_opportunities(self) -> Dict:
        opps = self.client.get_opportunities()
        prompt = f"""
Review the following opportunities from Dynamics 365:

{opps[:5]}

Analyze win/loss likelihood, potential bottlenecks in pipeline, and projected value.
Provide suggestions for accelerating deal closure.
"""
        return self.llm.summarize_responses(prompt)
