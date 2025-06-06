# tests/test_utils/test_workflow_runner.py

from utils.workflow_runner import WorkflowRunner


def test_workflow_chaining():
    wf = WorkflowRunner("test_chain")

    # Define mock steps
    wf.add_step(lambda x: x + 1)
    wf.add_step(lambda x: x * 2)
    wf.add_step(lambda x: f"Result: {x}")

    result = wf.run(initial_input=3)

    assert result == "Result: 8"
