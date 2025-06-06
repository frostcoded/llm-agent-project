# utils/workflow_runner.py

from typing import List, Callable, Dict, Any


class WorkflowRunner:
    """
    Executes a defined chain of agent functions with optional input/output handoff.
    """

    def __init__(self, name: str):
        self.name = name
        self.steps: List[Callable[[Any], Any]] = []

    def add_step(self, step: Callable[[Any], Any]) -> None:
        """
        Add an agent function to the workflow chain.
        """
        self.steps.append(step)

    def run(self, initial_input: Any = None) -> Any:
        """
        Run the full agent chain, passing output of each step to the next.
        """
        output = initial_input
        for i, step in enumerate(self.steps):
            output = step(output)
        return output
