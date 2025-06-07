# agents/llm_factory.py

from config.settings import load_settings
from agents.llm_collator import LLMCollator
from agents.fake_llm_collator import FakeLLMCollator
from typing import Dict, Any


def get_collator(config: Dict[str, Any] = None):
    """
    Returns the appropriate collator (real or fake) based on config.
    """
    if config is None:
        config = load_settings().get("llms", {})

    if config.get("use_fake", False):
        return FakeLLMCollator(config)
    return LLMCollator(config)
