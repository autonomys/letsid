# tests/core/test_issuance.py
import unittest
from unittest.mock import patch
from letsid.issuance import issue_identity

class TestIssuance(unittest.TestCase):
    @patch("letsid.issuance.create_x509_certificate", return_value="test_certificate")
    @patch("letsid.client.LetsIDClient.send_data_to_letsid", return_value={"result": "success"})
    @patch("letsid.client.LetsIDClient.generate_key_pair_and_csr", return_value=("test_public_key", "test_private_key", "test_seed", "test_csr"))
    def test_issue_identity(self, mock_generate_key_pair_and_csr, mock_send_data_to_letsid, mock_create_x509_certificate):
        issue_identity()
        mock_generate_key_pair_and_csr.assert_called_once()
        mock_create_x509_certificate.assert_called_once_with("test_csr", "user_private_key_hex_placeholder")
        mock_send_data_to_letsid.assert_called_once_with("issue_identity", {
            "x509_certificate": "test_certificate",
            "user_identifier": "user_identifier_placeholder"
        })

if __name__ == "__main__":
    unittest.main()
