# agents/compliance_checker.py

from agents.llm_collator import LLMCollator
from agents.gitlab_manager import GitLabManager
from config.settings import load_settings
from typing import Dict, Any


class ComplianceChecker:
    """
    Checks documents and workflows for regulatory compliance.
    Can log violations to GitLab.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.llm = LLMCollator(config.get("llms", {}))
        self.gitlab = GitLabManager(config) if config.get("gitlab", {}).get("api_token") else None

    def check_document(self, text: str, framework: str = "GDPR", project_id: str = None) -> Dict[str, Any]:
        prompt = f"""
Check the following document for compliance with {framework}:

{text}

List compliant areas, non-compliance risks, and remediation steps.
"""
        result = self.llm.summarize_responses(prompt)

        if self.gitlab and project_id:
            self.gitlab.create_issue(
                project_id,
                f"Compliance Review - {framework}",
                result.get("summary", "Compliance review generated.")
            )

        return result
