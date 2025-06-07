# agents/worflow_effiency.py

from agents.llm_collator import LLMCollator
from integrations.jira_client import JiraClient
from integrations.github_client import GitHubClient
from config.settings import load_settings
from prompts.prompts import render_prompt
from typing import Dict, Any


class WorkflowEfficiencyAgent:
    """
    Evaluates workflow timing, blockers, and inefficiencies across GitHub and Jira.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.jira = JiraClient(config.get("jira", {}))
        self.github = GitHubClient(config.get("github", {}))
        self.collator = LLMCollator(config.get("llms", {}))

    def analyze_efficiency(self, jira_board_id: int, github_repo: str) -> Dict:
        issues = self.jira.get_issues_for_board(jira_board_id)
        prs = self.github.get_pull_requests(github_repo)

        prompt = render_prompt("workflow_efficiency_prompt.txt", {
            "jira_issues": issues[:5],
            "pull_requests": prs[:5]
        })

        return self.collator.summarize_responses(prompt)
