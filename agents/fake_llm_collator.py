# agents/fake_llm_collator.py

from typing import Dict, Any


class FakeLLMCollator:
    """
    Simulates LLMCollator behavior for offline testing and CI environments.
    Returns predictable mock responses.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {"provider": "mock"}

    def summarize_responses(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "summary": f"[Mock Summary] Based on prompt: {prompt[:50]}...",
            "confidence": 0.99,
            "provider": self.config.get("provider", "mock")
        }

    def collect_responses(self, prompt: str, context: Dict[str, Any] = None) -> list:
        return [
            {
                "provider": "mock-llm-1",
                "response": f"[Mock Response] A - for prompt: {prompt[:30]}...",
                "score": 0.98
            },
            {
                "provider": "mock-llm-2",
                "response": f"[Mock Response] B - for prompt: {prompt[:30]}...",
                "score": 0.96
            }
        ]
