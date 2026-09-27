from typing import List
from classes.email import email
from abc import ABC, abstractmethod
from config.load_config import load_env

class base_email_provider(ABC):
    """
    This is a Java-style interface storing information about an email provider and some functions for authenticating, reading emails, anddrafting/sending a new email.
    It will not work unless overridden by subclasses.
    """
    def __init__(self, name: str):
        self.name = name
        self.handler_service_endpoint: str = load_env().get("SERVER_ENDPOINT", "")
        assert self.handler_service_endpoint, "SERVER_ENDPOINT environment variable is not set."
        with open("config/uuid.txt", "r") as f:
            self.uid = f.read().strip()
    @abstractmethod
    def authenticate(self):
        """
        This is meant to be a Java-style interface for authenticating with a provider. It should be overridden by subclasses.
        Intended use: Authenticates a user to the given email provider.
        This method should handle authentication flow, token storage, and (if supported) refresh logic.
        It should return nothing if authentication is successful and throw an Exception if it fails.
        """
        pass
    @abstractmethod
    def remove_acc(self):
        """
        This is meant to be a Java-style interface for removing an account from a provider. It should be overridden by subclasses.
        Intended use: Removes a user's account from this instance of the app.
        This method should handle all necessary cleanup, such as deleting stored tokens, and (if supported) revoking access from the provider.
        It should return nothing if removal is successful and throw an Exception if it fails.
        """
        pass
    @abstractmethod
    def check(self) -> List[email]:
        """
        This method is a Java-style interface for reading emails from a provider. It must be overridden by subclasses.
        Intended use: Reads emails from the user's inbox on the given email provider.
        This method should return a list of email objects representing the emails in the user's inbox.
        It should throw an Exception if reading emails fails.
        """
        pass
    @abstractmethod
    def draft(self, new_email: email):
        """
        This method is a Java-style interface for adding an email to the draft folder of a provider.
        If the provider supports a draft folder, this function must be overridden by subclass. If not, it may remain.
        The parameters provided here may not be changed, as this is an interface.
        """
        pass
    @abstractmethod
    def send(self, new_email: email):
        """
        This method is a Java-style interface for sending an email from a provider.
        The parameters provided here may not be changed, as this is an interface.
        """
        pass