# agents/cycle_time_analyzer.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class CycleTimeAnalyzer:
    """
    Analyzes item completion times and recommends improvements to reduce cycle time.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def analyze_cycle_time(
        self,
        items: List[Dict[str, Any]],
        process_doc: str = ""
    ) -> Dict[str, Any]:
        """
        Accepts a list of items with timestamps and optionally a process description.
        Returns suggestions to streamline the cycle time.
        """
        prompt = f"""
Analyze the following completed items for cycle time efficiency:

Items:
{items}

Process Description:
{process_doc}

Identify delays, unnecessary steps, or inconsistencies. Suggest how to reduce average cycle time.
"""
        return self.collator.summarize_responses(prompt)
