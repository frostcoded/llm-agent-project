# agents/compliance_checker.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class ComplianceChecker:
    """
    Checks for regulatory compliance against standards like GDPR, HIPAA, SOC 2.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def check_document(self, text: str, framework: str = "GDPR") -> Dict[str, Any]:
        prompt = f"""
Check the following document for compliance with {framework}:

{text}

List areas that are compliant, potentially non-compliant, and suggest remediation where needed.
"""
        return self.collator.summarize_responses(prompt)

    def check_workflow(self, description: str, framework: str = "HIPAA") -> Dict[str, Any]:
        prompt = f"""
Review the following operational workflow for compliance with {framework}:

{description}

Identify violations or concerns and suggest mitigations.
"""
        return self.collator.summarize_responses(prompt)
