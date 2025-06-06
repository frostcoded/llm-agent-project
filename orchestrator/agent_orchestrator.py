# orchestrator/agent_orchestrator.py

from utils.workflow_runner import WorkflowRunner
from utils.agent_registry import get_agent
from utils.metrics import track_agent
from orchestrator.task_queue import TaskQueue
from config.settings import load_settings

class AgentOrchestrator:
    """
    Central controller to route tasks, workflows, or agent execution.
    """

    def __init__(self):
        self.config = load_settings()
        self.queue = TaskQueue()

    @track_agent("orchestrator_dispatch")
    def dispatch(self, command: str, payload: dict):
        """
        Route a task to the correct agent based on command.
        """
        if command == "analyze_sap_sales":
            agent = get_agent("sap_erp")
            return agent.analyze_sales()

        elif command == "summarize_tableau":
            agent = get_agent("tableau_analytics")
            return agent.analyze_dashboards()

        elif command == "jira_project_check":
            agent = get_agent("jira_project")
            return agent.analyze_board(payload.get("board_id"))

        else:
            raise ValueError(f"Unknown command: {command}")

    def run_workflow(self, workflow_name: str, input_data=None):
        """
        Run a multi-step agent workflow.
        """
        wf = WorkflowRunner(workflow_name)

        if workflow_name == "release_summary":
            wf.add_step(lambda _: get_agent("jira_project").analyze_board(42))
            wf.add_step(lambda result: get_agent("servicenow_itsm").summarize_changes())
            wf.add_step(lambda result: get_agent("slack_notifier").notify(str(result)))

        return wf.run(input_data)

    def enqueue_task(self, func, *args, **kwargs):
        self.queue.add_task(func, *args, **kwargs)
