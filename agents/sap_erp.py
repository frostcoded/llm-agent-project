# agents/sap_erp.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from integrations.sap_client import SAPClient
from prompts.prompts import render_prompt
from typing import Dict, Any, List


class SAPERP:
    """
    Analyzes SAP data (sales + procurement) using modular LLM prompts and summarization.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = SAPClient(config.get("sap", {}))
        self.collator = LLMCollator(config.get("llms", {}))

    def analyze_purchases(self, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        po_data = self.client.get_purchase_orders()
        sample = po_data[:5]
        prompt = render_prompt("insight_prompt_base.txt", {
            "data": f"{sample}\n\nFocus on: recent purchasing trends, cost outliers, vendor changes."
        })
        return self.collator.summarize_responses(prompt=prompt, context=context)

    def analyze_sales(self, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        sales_data = self.client.get_sales_orders()
        sample = sales_data[:5]
        prompt = render_prompt("insight_prompt_base.txt", {
            "data": f"{sample}\n\nHighlight: revenue trends, customer segmentation, order flow risks."
        })
        return self.collator.summarize_responses(prompt=prompt, context=context)
