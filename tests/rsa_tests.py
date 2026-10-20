import unittest
from util.rsa import rsa_encrypt, rsa_decrypt, load_rsa_nums, xor_bytes

class TestRSAFunctions(unittest.TestCase):
    def setUp(self):
        # Load RSA private numbers for testing
        self.priv_nums = load_rsa_nums()
        self.public_key = int(self.priv_nums["n"])
        self.message = "Test message for RSA encryption"

    def test_rsa_encrypt_decrypt(self):
        # Encrypt the message
        encrypted_key, encrypted_message = rsa_encrypt(self.public_key, self.message)
        
        # Decrypt the message
        decrypted_message = rsa_decrypt(self.priv_nums, encrypted_key, encrypted_message)
        
        # Assert that the decrypted message matches the original message
        self.assertEqual(decrypted_message, self.message)

    def test_xor_bytes(self):
        data = b"Hello, World!"
        key = b"key"
        expected_result = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
        
        # Test xor_bytes function
        result = xor_bytes(data, key)
        
        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)