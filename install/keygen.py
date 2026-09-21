import json
from cryptography.hazmat.primitives.asymmetric import rsa
import requests
import uuid
from config.defaults import SERVER_ENDPOINT

def gen_keys() -> dict[str, str]:
    """
    Generates a new RSA key pair and returns them as a dictionary. Please note that the standard e=65537 is enforced (and is thus not returned).
    Returns:
        dict: A dictionary containing the modulus 'n' and private exponent 'd' of the RSA key pair.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    numbers = private_key.private_numbers()
    numbers_json = {
        "n": str(numbers.public_numbers.n),
        "d": str(numbers.d),
        "e": str(numbers.public_numbers.e), # this should be "65537" but save anyways
        "p": str(numbers.p),
        "q": str(numbers.q),
        "dmp1": str(numbers.dmp1),
        "dmq1": str(numbers.dmq1),
        "iqmp": str(numbers.iqmp)
    }

    return numbers_json # e=65537 is standard and will be enforced

def save_keys(uid: str, n: int, priv_nums: dict[str, str]):
    """
    Saves the UUID to auth/uuid.txt, the RSA private numbers to auth/rsa_nums.json, and registers the public modulus with the server (required for encryption).
    """
    with open("auth/uuid.txt", "w") as f:
        f.write(f"{uid}")
    with open("auth/rsa_nums.json", "w") as f:
        json.dump(priv_nums, f)
    requests.post(SERVER_ENDPOINT + "/register", params={"uid": uid, "n": n}, timeout=10)

if __name__ == "__main__":
    keys = gen_keys()
    save_keys(str(uuid.uuid4()), int(keys["n"]), keys)