# agents/release_note_builder.py

from agents.llm_collator import LLMCollator
from agents.slack_notifier import SlackNotifier
from agents.gitlab_manager import GitLabManager
from config.settings import load_settings
from typing import List, Dict, Any


class ReleaseNoteBuilder:
    """
    Builds release notes. Can notify Slack and log issues in GitLab.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings()
        self.llm = LLMCollator(config.get("llms", {}))
        self.slack = SlackNotifier(config) if config.get("slack", {}).get("enabled", False) else None
        self.gitlab = GitLabManager(config) if config.get("gitlab", {}).get("api_token") else None

    def build_release_notes(
        self,
        version: str,
        issues: List[Dict[str, str]],
        commits: List[str] = None,
        project_id: str = None,
        notify: bool = True
    ) -> Dict[str, Any]:
        issue_list = "\n".join([f"- {item['key']}: {item['summary']}" for item in issues])
        commit_list = "\n".join(commits) if commits else "N/A"

        prompt = f"""
Create professional release notes for version {version}.

Resolved Issues:
{issue_list}

Associated Commits:
{commit_list}

Structure it with clear headers, bullet points, and a summary section.
"""
        result = self.llm.summarize_responses(prompt)
        content = result.get("summary", "Release notes not generated.")

        if notify and self.slack:
            self.slack.notify(f"📦 *Release {version} published!*\n{content[:500]}...")

        if self.gitlab and project_id:
            self.gitlab.create_issue(project_id, f"Release {version} Notes", content)

        return result
