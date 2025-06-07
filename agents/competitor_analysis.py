# agents/competitor_analysis.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from prompts.prompts import render_prompt
from utils.logger import logger
from typing import Dict, List, Any


class CompetitorAnalysisAgent:
    """
    Analyzes internal and external data to compare competitive position.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def analyze(
        self,
        company_name: str,
        competitors: List[str],
        internal_data: str = "",
        external_data: str = "",
        period: str = "last 6 months"
    ) -> Dict[str, Any]:

        if not company_name or not competitors:
            logger.warning("[CompetitorAnalysisAgent] Missing company name or competitors.")
            return {"summary": "Missing input data", "confidence": "low"}

        prompt = render_prompt("competitor_analysis_prompt.txt", {
            "company": company_name,
            "competitors": ", ".join(competitors),
            "internal_data": internal_data,
            "external_data": external_data,
            "period": period
        })

        logger.debug(f"[CompetitorAnalysisAgent] Prompt generated for {company_name} vs {competitors}")
        return self.collator.summarize_responses(prompt)
