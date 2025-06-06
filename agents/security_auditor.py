# agents/security_auditor.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any


class SecurityAuditor:
    """
    Audits code or config for security risks and recommends mitigation.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def audit_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        prompt = f"""
Perform a security audit on the following {language} code:

{code}

List vulnerabilities, severity (low/medium/high), and mitigation steps.
"""
        return self.collator.summarize_responses(prompt)

    def audit_config(self, config_block: str, platform: str = "AWS") -> Dict[str, Any]:
        prompt = f"""
Perform a security audit on this {platform} config:

{config_block}

Identify misconfigurations or weak settings and suggest fixes.
"""
        return self.collator.summarize_responses(prompt)
