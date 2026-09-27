from classes.email_provider import base_email_provider
from classes.email import email
from util.open_in_browser import open_in_browser
from util.rsa import rsa_encrypt, rsa_decrypt
from errors.AuthError import AuthError
from typing import List
import requests
import secrets
import hashlib
import base64
from urllib.parse import urlparse, parse_qs, urlencode
import socket
import json

def b64url_no_padding(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def make_pkce_pair():
    verifier = secrets.token_urlsafe(64)
    challenge = b64url_no_padding(
        hashlib.sha256(verifier.encode("ascii")).digest()
    )
    return verifier, challenge

def reserve_loopback_port() -> tuple[socket.socket, int]:
    # Keep this socket open; use it as / hand it to your local HTTP server.
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))  # 0 asks the OS for an ephemeral port
    listener.listen(1)
    return listener, listener.getsockname()[1]

def parse_oauth2_callback(callback_url: str, exp_state: str) -> str:
    """
    Parses the OAuth2 callback URL to extract the authorization code.
    Validates the state parameter to prevent CSRF attacks.
    """
    parsed_url = urlparse(callback_url)
    query_params = parse_qs(parsed_url.query)

    if "error" in query_params:
        error_description = query_params.get("error_description", [""])[0]
        raise RuntimeError(f"OAuth2 error: {query_params['error'][0]} - {error_description}")

    code = query_params.get("code", [None])[0]
    state = query_params.get("state", [None])[0]

    if state != exp_state:
        raise ValueError("State parameter does not match expected value.")

    if not code:
        raise RuntimeError("Authorization code not found in callback URL.")

    return code

def exchange_code(uid: str, code: str, redirect_uri: str, code_verifier: str, server_endpoint: str) -> dict:
    """
    Exchanges the authorization code for an access token.
    """
    server_n = int(requests.get(f"{server_endpoint}/get_privkey", params={"uid": uid}, timeout=10).json().get("n"))
    verifier_enc, enc_key = rsa_encrypt(server_n, code_verifier)
    response = requests.post(
        f"{server_endpoint}/google_token_exchange",
        json={"code": code, "uuid": uid, "redirect_uri": redirect_uri, "code_verifier": verifier_enc.hex(), "enc_key": enc_key.hex()},
        timeout=10
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to exchange code: {response.text}")
    return response.json()

class Gmail(base_email_provider):
    """
    This class is an implementation of the base_email_provider interface for Gmail.
    """
    def __init__(self):
        super().__init__("google")

    def authenticate(self):
        """
        Implements Gmail authentication using OAuth2.0
        Method handles OAuth2.0 flow, token storage, and refresh logic.
        """
        try:
            resp = requests.get(f"{self.handler_service_endpoint}/get_creds", params={"provider": "google", "uuid": {self.uid}}, timeout=10).json()
            CLIENT_ID = resp["client_id"]
            SCOPES = resp["scopes"]
            listener, port = reserve_loopback_port()
            redirect_uri = f"http://127.0.0.1:{port}/oauth2/callback"
            state = secrets.token_urlsafe(32)
            code_verifier, code_challenge = make_pkce_pair()
            params = {
                "client_id": CLIENT_ID,
                "response_type": "code",
                "redirect_uri": redirect_uri,
                "scope": " ".join(SCOPES),
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "access_type": "offline",
                "include_granted_scopes": "true",
            }
            auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
            open_in_browser(auth_url)
            code = parse_oauth2_callback(listener.accept()[0].recv(1024).decode("utf-8"), state)
            token = exchange_code(self.uid, code, redirect_uri, code_verifier, self.handler_service_endpoint)
            self.access_token = token["access_token"]
            self.id_token = token.get("id_token")
            with open("auth/gmail_token.json", "w") as f:
                json.dump(token, f)
        except Exception as e:
            raise AuthError("Error loading credentials: " + str(e)) from e

    def remove_acc(self):
        """
        This is meant to be a Java-style interface for removing an account from a provider. It should be overridden by subclasses.
        """
        raise NotImplementedError("This method must be overridden by subclasses.")

    def check(self) -> List[email]:
        """
        This method is a Java-style interface for reading emails from a provider. It must be overridden by subclasses.
        """
        raise NotImplementedError("This method must be overridden by subclasses.")

    def draft(self, new_email: email):
        """
        This method is a Java-style interface for adding an email to the draft folder of a provider.
        If the provider supports a draft folder, this function must be overridden by subclass.
        The parameters provided here may not be changed, as this is an interface.
        """
        raise NotImplementedError("This method must be overridden by subclasses.")

    def send(self, new_email: email):
        """
        This method is a Java-style interface for sending an email from a provider.
        The parameters provided here may not be changed, as this is an interface.
        """
        raise NotImplementedError("This method must be overridden by subclasses.")


if __name__ == "__main__":
    g = Gmail()
    g.authenticate()