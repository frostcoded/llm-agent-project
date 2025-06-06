# config/settings.py

import yaml
from pathlib import Path

def load_settings(path: str = "config/settings.yaml") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
