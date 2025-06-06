# integrations/openai_client.py

import openai
from typing import Any, Dict
from integrations.base_llm_client import BaseLLMClient

class OpenAIClient(BaseLLMClient):
    """
    OpenAI implementation of BaseLLMClient.
    """

    def __init__(self, api_key: str, model: str = "gpt-4"):
        openai.api_key = api_key
        self.model = model

    def generate_response(self, prompt: str, context: Dict[str, Any] = {}) -> Dict[str, Any]:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **context
            )
            return {
                "source": "openai",
                "response": response.choices[0].message["content"],
                "usage": response.usage
            }
        except Exception as e:
            return {
                "source": "openai",
                "error": str(e)
            }
