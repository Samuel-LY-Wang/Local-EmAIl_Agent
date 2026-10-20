import unittest
import numpy as np
from util.rsa import rsa_encrypt, rsa_decrypt, load_rsa_nums, xor_bytes

rng = np.random.default_rng()  # Create a random number generator instance
class TestRSAFunctions(unittest.TestCase):
    def setUp(self):
        # Load RSA private numbers for testing
        self.priv_nums = load_rsa_nums()
        self.public_key = int(self.priv_nums["n"])
        self.messages = []
        for _ in range(100):
            msg_list = []
            for _ in range(1024): # test messages longer than the key (too long to directly RSA-encrypt)
                msg_list.append(rng.integers(0, 256, size=32).tobytes())
            self.messages.append(msg_list)

    def test_rsa_encrypt_decrypt(self):
        # Encrypt the message
        for msg in self.messages:
            encrypted_key, encrypted_message = rsa_encrypt(self.public_key, msg)
            
            # Decrypt the message
            decrypted_message = rsa_decrypt(self.priv_nums, encrypted_key, encrypted_message)
            
            # Assert that the decrypted message matches the original message
            self.assertEqual(decrypted_message, msg)

    def test_xor_bytes(self):
        for _ in range(1000):
            data = rng.integers(0, 1 << 32, dtype=np.int32)
            key = rng.integers(0, 1 << 8, dtype=np.int8)
            exp_result = data ^ (key + key<<8 + key<<16 + key<<24)
            
            # Test xor_bytes function
            result = xor_bytes(data.tobytes(), key.tobytes())
            
            # Assert that the result matches the expected result
            self.assertEqual(result, exp_result)