from config.load_config import load_config
from abc import ABC, abstractmethod

class base_LLM_provider(ABC):
    """
    This is a Java-style interface storing information about an LLM provider and some functions for authenticating and invoking a model from that provider.
    It will not work unless overridden by subclasses.
    """
    def __init__(self, name: str, endpoint: str, API_key: str):
        self.name = name
        self.endpoint = endpoint
        self.API_key = API_key
        self.config = load_config("LLM")
    @abstractmethod
    def authenticate(self) -> bool:
        """
        This is meant to be a Java-style interface for authenticating with a provider. It should be overridden by subclasses.
        """
        pass
    @abstractmethod
    def invoke(self, model: str, in_context: str) -> str:
        """
        This method is a Java-style interface for invoking a model with a provider. It must be overridden by subclasses.
        """
        pass
    def change_key(self, new_key: str):
        self.API_key = new_key