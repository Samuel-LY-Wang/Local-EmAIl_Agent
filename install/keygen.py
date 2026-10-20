import json
from cryptography.hazmat.primitives.asymmetric import rsa
import requests
import uuid
from config.env import env

def gen_keys() -> tuple[dict[str, str], dict[str, str]]:
    """
    Generates a new RSA key pair and returns them as a dictionary. Please note that the standard e=65537 is enforced (and is thus not returned).
    Returns:
        dict: A dictionary containing the modulus 'n' and private exponent 'd' of the RSA key pair.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    numbers = private_key.private_numbers()
    pub_nums = {
        "n": str(numbers.public_numbers.n),
        "e": str(numbers.public_numbers.e), # this should be "65537" but save anyways
    }
    priv_nums = {
        "d": str(numbers.d),
        "p": str(numbers.p),
        "q": str(numbers.q),
        "dmp1": str(numbers.dmp1),
        "dmq1": str(numbers.dmq1),
        "iqmp": str(numbers.iqmp)
    }

    return pub_nums, priv_nums # e=65537 is standard and will be enforced

def save_keys(uid: str, pub: dict[str, str], priv: dict[str, str]) -> None:
    """
    Saves the UUID to auth/uuid.txt, the RSA private numbers to auth/rsa_nums.json, and registers the public modulus with the server (required for encryption).
    """
    res = requests.post(env.server_endpoint + "/register", json={"uuid": uid, "n": pub["n"]}, timeout=10)
    if (res.status_code == 200):
        return # 200 status code is returned if this user is registered. Thus, no re-registration.
        # TODO: add separate method + endpoint for re-registration (e.g. data breach)
    res.raise_for_status()
    with open("auth/uuid.txt", "w") as f:
        f.write(f"{uid}")
    with open("auth/rsa_pub.json", "w") as f:
        json.dump(pub, f, indent=4)
    with open("auth/rsa_priv.json", "w") as f:
        json.dump(priv, f, indent=4)

if __name__ == "__main__":
    pub, priv = gen_keys()
    save_keys(str(uuid.uuid4()), pub, priv)