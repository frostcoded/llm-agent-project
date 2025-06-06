# agents/github_repo.py

from integrations.github_client import GitHubClient
from agents.llm_collator import LLMCollator
from config.settings import load_settings
from prompts.prompts import render_prompt
from typing import Dict, Any


class GitHubRepoAgent:
    """
    Analyzes GitHub repository activity and summarizes key insights using LLMs.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.client = GitHubClient(config.get("github", {}))
        self.collator = LLMCollator(config.get("llms", {}))

    def list_pull_requests(self, repo: str, state: str = "open") -> Any:
        return self.client.get_pull_requests(repo, state)

    def list_issues(self, repo: str, state: str = "open") -> Any:
        return self.client.get_issues(repo, state)

    def analyze_repository(self, repo: str, context: Dict[str, Any] = {}) -> Dict:
        prs = self.client.get_pull_requests(repo)
        issues = self.client.get_issues(repo)
        prompt = render_prompt("insight_prompt_base.txt", {
            "data": f"Pull Requests:\n{prs[:3]}\n\nIssues:\n{issues[:3]}\n\nEvaluate repo health, review activity, and team load."
        })
        return self.collator.summarize_responses(prompt, context)
