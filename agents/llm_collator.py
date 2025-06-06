# agents/llm_collator.py

from typing import Dict, List, Any
from integrations.openai_client import OpenAIClient
from integrations.claude_client import ClaudeClient
from integrations.google_llm_client import GoogleLLMClient
from integrations.grok_client import GrokClient


class LLMCollator:
    """
    Aggregates responses from multiple LLMs and returns unified output.
    """

    def __init__(self, config: Dict[str, Any]):
        self.clients = []

        if config.get("openai", {}).get("enabled", False):
            self.clients.append(
                OpenAIClient(
                    api_key=config["openai"]["api_key"],
                    model=config["openai"].get("model", "gpt-4")
                )
            )

        if config.get("claude", {}).get("enabled", False):
            self.clients.append(
                ClaudeClient(
                    api_key=config["claude"]["api_key"],
                    model=config["claude"].get("model", "claude-3-opus")
                )
            )

        if config.get("google", {}).get("enabled", False):
            self.clients.append(
                GoogleLLMClient(
                    api_key=config["google"]["api_key"],
                    model=config["google"].get("model", "gemini-pro")
                )
            )

        if config.get("grok", {}).get("enabled", False):
            self.clients.append(
                GrokClient(
                    api_key=config["grok"]["api_key"],
                    model=config["grok"].get("model", "grok-1")
                )
            )

    def collect_responses(self, prompt: str, context: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Get and collate responses from all available LLMs.
        """
        results = []

        for client in self.clients:
            result = client.generate_response(prompt, context)
            results.append(result)

        return results

    def summarize_responses(self, prompt: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Optional: Perform meta-analysis or ranking on results.
        """
        responses = self.collect_responses(prompt, context)
        valid_responses = [r for r in responses if "response" in r]

        return {
            "summary": f"{len(valid_responses)} responses collected.",
            "results": responses
        }
