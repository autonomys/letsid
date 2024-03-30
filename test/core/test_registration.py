# tests/cli/test_cli.py
import unittest
from unittest.mock import patch
from letsid.registration import register_user_with_letsid

class TestRegistration(unittest.TestCase):
    @patch("letsid.client.LetsIDClient.send_data_to_letsid", return_value={"result": "success"})
    @patch("letsid.client.LetsIDClient.generate_key_pair_and_csr", return_value=("test_public_key", "test_private_key", "test_seed", "test_csr"))
    @patch("letsid.registration.sign_csr_with_private_key", return_value="test_signature")
    @patch("letsid.registration.perform_oidc_signup", return_value="test_oidc_token")
    def test_register_user_with_letsid(self, mock_perform_oidc_signup, mock_sign_csr_with_private_key, mock_generate_key_pair_and_csr, mock_send_data_to_letsid):
        result = register_user_with_letsid("test_csr", "test_signature", "test_oidc_token")
        mock_generate_key_pair_and_csr.assert_called_once()
        mock_sign_csr_with_private_key.assert_called_once_with("test_csr", "test_private_key")
        mock_perform_oidc_signup.assert_called_once()
        mock_send_data_to_letsid.assert_called_once_with("register", {
            "csr": "test_csr",
            "digital_signature": "test_signature",
            "oidc_token": "test_oidc_token"
        })

if __name__ == "__main__":
    unittest.main()
