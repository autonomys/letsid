# tests/core/test_client.py
import os
import unittest
from unittest.mock import patch
from src.letsid.client import LetsIDClient

class TestLetsIDClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the LetsIDClient instance
        cls.client = LetsIDClient()

    @patch.dict(os.environ, {"LETSID_SERVER_URL": "https://test-server.com"})
    def test_server_url_from_env(self):
        self.assertEqual(self.client.server_url, "https://test-server.com")

    def test_generate_key_pair_and_csr(self):
        public_key_hex, private_key_hex, seed_hex, csr = self.client.generate_key_pair_and_csr()
        self.assertEqual(public_key_hex, os.getenv("PUBLIC_KEY_HEX", "public_key_hex_placeholder"))
        self.assertEqual(private_key_hex, os.getenv("PRIVATE_KEY_HEX", "private_key_hex_placeholder"))
        self.assertEqual(seed_hex, os.getenv("SEED_HEX", "seed_hex_placeholder"))
        self.assertEqual(csr, os.getenv("CSR", "csr_placeholder"))

    def test_sign_csr_with_private_key(self):
        csr = os.getenv("CSR", "csr_placeholder")
        private_key_hex = os.getenv("PRIVATE_KEY_HEX", "private_key_hex_placeholder")
        signature = self.client.sign_csr_with_private_key(csr, private_key_hex)
        self.assertEqual(signature, os.getenv("DIGITAL_SIGNATURE", "digital_signature_placeholder"))

    def test_send_data_to_letsid(self):
        data = {"csr": "test_csr", "digital_signature": "test_signature", "oidc_token": "test_oidc_token"}
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"result": "success"}
            result = self.client.send_data_to_letsid("register", data)
            self.assertEqual(result, {"result": "success"})

if __name__ == "__main__":
    unittest.main()
