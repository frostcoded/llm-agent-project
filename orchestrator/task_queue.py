# orchestrator/task_queue.py

import threading
import time
from typing import Callable, List, Tuple, Any

class TaskQueue:
    """
    Simple in-memory queue to store and run agent tasks.
    """

    def __init__(self):
        self.queue: List[Tuple[Callable, Tuple[Any], dict]] = []
        self.lock = threading.Lock()
        self.running = False

    def add_task(self, func: Callable, *args, **kwargs):
        """
        Add a callable task to the queue.
        """
        with self.lock:
            self.queue.append((func, args, kwargs))

    def run_once(self):
        """
        Run a single task from the queue.
        """
        if self.queue:
            with self.lock:
                task, args, kwargs = self.queue.pop(0)
            task(*args, **kwargs)

    def run_all(self, delay: float = 0):
        """
        Run all tasks in the queue with optional delay between each.
        """
        while self.queue:
            self.run_once()
            if delay:
                time.sleep(delay)

    def run_background(self, interval: float = 1.0):
        """
        Continuously process tasks in a background thread.
        """
        def loop():
            self.running = True
            while self.running:
                self.run_once()
                time.sleep(interval)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
