# config/settings.py
import yaml
import os
from pathlib import Path


def _load_yaml(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Missing config: {file_path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_settings() -> dict:
    config = _load_yaml("config/settings.yaml")
    _inject_env_variables(config)
    return config


def load_agent_profiles() -> dict:
    return _load_yaml("config/agent_profiles.yaml")


def _inject_env_variables(config: dict):
    def replace_env(val):
        if isinstance(val, str) and val.startswith("ENV_"):
            return os.environ.get(val.replace("ENV_", ""), "MISSING_ENV_VAR")
        return val

    def recursive_replace(obj):
        if isinstance(obj, dict):
            return {k: recursive_replace(replace_env(v)) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [recursive_replace(v) for v in obj]
        return replace_env(obj)

    for key in config:
        config[key] = recursive_replace(config[key])
import yaml
from pathlib import Path

def load_settings(path: str = "config/settings.yaml") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
