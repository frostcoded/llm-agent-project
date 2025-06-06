# agents/tableau_analytics.py

from integrations.tableau_client import TableauClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict


class TableauAnalytics:
    """
    Analyzes Tableau dashboards, views, and embedded metrics using LLM interpretation.
    """

    def __init__(self, config: Dict = None):
        if config is None:
            config = load_settings()
        self.client = TableauClient(config.get("tableau", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def analyze_dashboards(self) -> Dict[str, List[str]]:
        dashboards = self.client.list_dashboards()
        result = {}
        for dash in dashboards:
            views = self.client.get_dashboard_views(dash)
            result[dash] = views
        return result

    def summarize_insights(self, dashboard_name: str) -> Dict:
        views = self.client.get_dashboard_views(dashboard_name)
        prompt = f"""
Analyze the following Tableau dashboard: {dashboard_name}

Views included:
{', '.join(views)}

Summarize key insights and any anomalies that may need review.
"""
        return self.llm.summarize_responses(prompt)
