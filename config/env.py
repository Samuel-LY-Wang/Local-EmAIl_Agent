import dotenv

class ENV():
    """
    Loads environment variables from the .env file.
    """
    def __init__(self):
        try:
            env_vars = dotenv.dotenv_values()
        except FileNotFoundError:
            raise RuntimeError("Failed to load .env file. Please ensure that the .env file exists in the project root directory.")
        self.env = {key: value for key, value in env_vars.items() if isinstance(value, str)}
        self.server_endpoint = self.env["SERVER_ENDPOINT"]

env = ENV()