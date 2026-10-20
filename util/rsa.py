from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import secrets
import json

def load_rsa_nums() -> dict[str, str]:
    """
    Loads the RSA private numbers from auth/rsa_nums.json.
    Returns:
        dict: A dictionary containing the RSA private numbers.
    """
    with open("auth/rsa_nums.json", "r") as f:
        priv_nums = json.load(f)
    return priv_nums

"""
Yes I know repeating-key XOR is not that secure
However, it doesn't matter in this case. The key is the same length as the message.
"""
def xor_bytes(data: bytes, key: bytes) -> bytes:
    """Performs bitwise XOR on raw bytes payload."""
    key_len = len(key)
    # Fast iteration using zip and a generator expression
    return bytes(b ^ key[i % key_len] for i, b in enumerate(data))

def rsa_encrypt(public_key: int, message: str) -> tuple[bytes, bytes]:
    xor_key = secrets.token_bytes(128)  # Generate a random 128-byte (1024-bit) key
    rsa_key = rsa.RSAPublicNumbers(public_key, 65537).public_key()
    encrypted_key = rsa_key.encrypt(
        xor_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_message = xor_bytes(message.encode(), xor_key)
    return (encrypted_key, encrypted_message)

def rsa_decrypt(priv_nums: dict[str, str], encrypted_key: bytes, encrypted_message: bytes) -> str:
    rsa_key = rsa.RSAPrivateNumbers(
        d=int(priv_nums["d"]),
        p=int(priv_nums["p"]),
        q=int(priv_nums["q"]),
        dmp1=int(priv_nums["dmp1"]),
        dmq1=int(priv_nums["dmq1"]),
        iqmp=int(priv_nums["iqmp"]),
        public_numbers=rsa.RSAPublicNumbers(
            n=int(priv_nums["n"]),
            e=int(priv_nums["e"])
        )
    ).private_key()
    xor_key = rsa_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_message = xor_bytes(encrypted_message, xor_key)
    return decrypted_message.decode()