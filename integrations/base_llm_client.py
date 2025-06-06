# integrations/base_llm_client.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    All LLM implementations should inherit from this class and implement the `generate_response` method.
    """

    @abstractmethod
    def generate_response(self, prompt: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        Generate a response from the LLM.

        Args:
            prompt (str): The prompt or input text.
            context (dict): Optional additional context or parameters.

        Returns:
            dict: A structured response including generated text and optional metadata.
        """
        pass
