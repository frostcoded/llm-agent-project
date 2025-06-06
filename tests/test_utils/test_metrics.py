# tests/test_utils/test_metrics.py

from utils.metrics import track_agent, report_metrics
import time


def test_track_agent_counts_and_timing():
    @track_agent("demo_task")
    def slow_add(x, y):
        time.sleep(0.1)
        return x + y

    result = slow_add(2, 3)
    assert result == 5

    metrics = report_metrics()
    assert "demo_task" in metrics
    assert metrics["demo_task"]["calls"] == 1
    assert metrics["demo_task"]["total_time"] >= 0.1
