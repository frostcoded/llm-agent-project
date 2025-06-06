# agents/release_note_builder.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import List, Dict, Any


class ReleaseNoteBuilder:
    """
    Converts deployment changes into human-readable release notes.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def build_release_notes(self, version: str, issues: List[Dict[str, str]], commits: List[str] = None) -> Dict[str, Any]:
        """
        Build release notes from Jira issues or commit messages.
        """
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
        return self.collator.summarize_responses(prompt)
