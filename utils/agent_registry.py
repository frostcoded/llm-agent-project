# utils/agent_registry.py

from typing import Dict, Callable, Any

_agent_registry: Dict[str, Callable[[], Any]] = {}


def register_agent(name: str, constructor: Callable[[], Any]):
    """
    Register an agent by name with its constructor (no args).
    """
    _agent_registry[name] = constructor


def get_agent(name: str) -> Any:
    """
    Retrieve an agent by name, raising if not found.
    """
    if name not in _agent_registry:
        raise ValueError(f"Agent '{name}' is not registered.")
    return _agent_registry[name]()


def list_agents() -> Dict[str, Callable[[], Any]]:
    return _agent_registry.copy()
