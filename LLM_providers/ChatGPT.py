import os
from classes.LLM_provider import BaseLLMProvider
from openai import OpenAI

class ChatGPT(BaseLLMProvider):
    """
    Sample implementatioon of the "base_LLM_provider" interface for OpenAI's API.
    Stable base that can be copied and modified slightly for other providers (Claude, Gemini, etc.)
    """
    def __init__(self, API_key: str = ""):
        super().__init__(name="OpenAI", endpoint="https://api.openai.com/v1", API_key=API_key)
        resolved_API_key = self.API_key if self.API_key else os.environ.get("OPENAI_API_KEY")
        if (not resolved_API_key):
            raise ValueError("OpenAI API key must be provided either as a parameter or through the OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=resolved_API_key)
        pass # no params needed, just need the base class for polymorphism anyways

    def authenticate(self) -> bool:
        """
        This method checks if the OpenAI API key is valid by making a simple request to the OpenAI API.
        """
        try:
            # Attempt to list models as a way to check if the API key is valid
            self.client.models.list()
            return True
        except Exception as e:
            return False

    def invoke(self, model: str, in_context: str) -> str:
        """
        This is the method to invoke an OpenAI model.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.config["base_sys_prompt"]},
                    {"role": "user", "content": in_context}
                ]
            )
            msg = response.choices[0].message.content
            return msg if msg else ""
        except Exception as e:
            raise Exception(f"Error invoking OpenAI model: {e}")