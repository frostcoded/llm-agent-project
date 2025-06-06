---

## 📄 `main.py`

```python
# main.py

import argparse
from config.settings import load_settings
from core.orchestrator import Orchestrator
from utils.logger import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="LLM Agent Framework CLI")
    parser.add_argument("--workflow", type=str, required=True, help="Workflow to run (e.g. onboarding, release, sprint)")
    parser.add_argument("--params", type=str, help="Optional JSON string of parameters")
    args = parser.parse_args()

    config = load_settings()
    orchestrator = Orchestrator(config)

    logger.info(f"Running workflow: {args.workflow}")
    result = orchestrator.execute_workflow(args.workflow)
    print(result)


if __name__ == "__main__":
    main()
