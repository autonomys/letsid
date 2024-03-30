# tests/web/test_api.py

import unittest
from unittest.mock import patch
from src.web.api import api

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = api.test_client()

    @patch("src.core.registration.register_user_with_letsid")
    def test_register_endpoint_success(self, mock_register):
        mock_register.return_value = {"user_id": 123}

        response = self.app.post("/api/register", json={"csr": "test_csr", "digital_signature": "test_signature", "oidc_token": "test_oidc_token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "data": {"user_id": 123}})

    @patch("src.core.registration.register_user_with_letsid")
    def test_register_endpoint_failure(self, mock_register):
        mock_register.return_value = None

        response = self.app.post("/api/register", json={"csr": "test_csr", "digital_signature": "test_signature", "oidc_token": "test_oidc_token"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "error", "message": "Registration failed"})

    @patch("src.core.issuance.issue_identity")
    def test_issue_identity_endpoint_success(self, mock_issue_identity):
        mock_issue_identity.return_value = {"identity_id": 456}

        response = self.app.post("/api/issue-identity", json={"x509_certificate": "test_certificate", "user_identifier": "test_user_id"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "data": {"identity_id": 456}})

    @patch("src.core.issuance.issue_identity")
    def test_issue_identity_endpoint_failure(self, mock_issue_identity):
        mock_issue_identity.return_value = None

        response = self.app.post("/api/issue-identity", json={"x509_certificate": "test_certificate", "user_identifier": "test_user_id"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "error", "message": "Issuance failed"})

if __name__ == "__main__":
    unittest.main()
