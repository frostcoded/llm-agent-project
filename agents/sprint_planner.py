# agents/sprint_planner.py

from agents.llm_collator import LLMCollator
from config.settings import load_settings
from typing import Dict, Any, List


class SprintPlanner:
    """
    Creates sprint plans by analyzing team inputs, past sprints, and constraints.
    """

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_settings().get("llms", {})
        self.collator = LLMCollator(config)

    def plan_sprint(
        self,
        sprint_length: int,
        team_availability: Dict[str, str],
        recent_velocity: str,
        sprint_goals: str,
    ) -> Dict[str, Any]:
        """
        Generates a sprint plan based on constraints and context.
        """
        prompt = f"""
Plan a {sprint_length}-week sprint.

Team Availability:
{team_availability}

Recent Velocity:
{recent_velocity}

Sprint Goals:
{sprint_goals}

Recommend team assignments, story allocations, and key milestones.
"""
        return self.collator.summarize_responses(prompt)
