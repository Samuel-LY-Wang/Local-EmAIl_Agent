import json
import dotenv

def load_config(setting: str) -> dict:
    """
    Loads the config file from config/config.json, as well as the base system prompt from config/base_sys_prompt.txt
    Returns a JSON object containing both the config data and the system prompt (as a key in the JSON object).
    """
    with open("config/config.json", "r") as f:
        config_data = json.load(f)[setting]
    if setting == "LLM":
        with open("config/base_sys_prompt.txt", "r") as f:
            base_sys_prompt = f.read()
        config_data["base_sys_prompt"] = base_sys_prompt
    return config_data

def load_env() -> dict:
    """
    Loads environment variables from the .env file.
    Returns a dictionary containing the environment variables.
    """
    return dotenv.dotenv_values(dotenv.find_dotenv())