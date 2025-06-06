# agents/competitor_analysis.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, List, Any


class CompetitorAnalysisAgent:
    """
    Analyzes internal and external data to compare competitive position.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def analyze(self, company_name: str, competitors: List[str], internal_data: str = "", external_data: str = "", period: str = "last 6 months") -> Dict[str, Any]:
        """
        Generates a comparative analysis.

        Args:
            company_name: Name of the user's company.
            competitors: List of competitors.
            internal_data: Internal, scrubbed documents or insights.
            external_data: Public content (scraped or uploaded).
            period: Time window to reference for analysis.
        """
        prompt = f"""
Compare {company_name} against the following competitors: {', '.join(competitors)}.
Use this internal information (scrubbed): {internal_data}
And this public data: {external_data}
Timeframe: {period}

Identify key trends, market advantages or weaknesses, and assign confidence scores. List external references if available.
"""
        return self.collator.summarize_responses(prompt)
