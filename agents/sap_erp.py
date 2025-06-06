# agents/sap_erp.py

from integrations.sap_client import SAPClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class SAPERP:
    """
    Uses SAP ERP data to generate procurement/sales summaries and financial insights.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = SAPClient(config.get("sap", {}))
        self.llm = LLMCollator(config.get("llms", {}))

    def analyze_purchases(self) -> Dict:
        po_data = self.client.get_purchase_orders()
        prompt = f"""
Analyze the following SAP purchase order data:

{po_data[:5]}  # sample only

What are the recent purchasing trends, cost outliers, or vendor shifts?
"""
        return self.llm.summarize_responses(prompt)

    def analyze_sales(self) -> Dict:
        sales_data = self.client.get_sales_orders()
        prompt = f"""
Analyze this SAP sales order data:

{sales_data[:5]}

Identify revenue trends, customer groupings, or potential risks in order flow.
"""
        return self.llm.summarize_responses(prompt)
