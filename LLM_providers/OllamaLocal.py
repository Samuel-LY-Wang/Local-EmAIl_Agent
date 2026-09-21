from classes.LLM_provider import BaseLLMProvider
import ollama as llama

class OllamaLocal(BaseLLMProvider):
    """
    Sample implementation of the "BaseLLMProvider" interface for Ollama's API.
    """
    def __init__(self):
        super().__init__(name="Ollama", endpoint="http://localhost:11434", API_key="")

    def authenticate(self) -> bool:
        """
        Ollama does not require authentication, so this method always returns True.
        """
        return True

    def invoke(self, model: str, in_context: str) -> str:
        """
        This is the method to invoke an Ollama model.
        """
        try:
            resp = llama.chat(model=model, messages=[{"role": "system", "content": self.config["base_sys_prompt"]}, {"role": "user", "content": in_context}])
            return resp['content']
        except llama.ResponseError as e:
            raise Exception(f"Error invoking Ollama model: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while invoking Ollama model: {e}")