# tests/web/test_forms.py
import unittest
from flask import Flask
from src.web.app import app
from src.web.forms import RegistrationForm, IssueIdentityForm  # Assuming these are your form classes

class TestRegistrationForm(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_valid_registration_form(self):
        # Simulate a valid form submission
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword',
            'confirm': 'securepassword'
        })
        self.assertTrue(form.validate())

    def test_invalid_registration_form(self):
        # Simulate an invalid form submission
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'invalidemail',  # Invalid email
            'password': 'securepassword',
            'confirm': 'mismatchpassword'  # Passwords do not match
        })
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)
        self.assertIn('confirm', form.errors)

class TestIssueIdentityForm(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_valid_issue_identity_form(self):
        # Simulate a valid form submission
        form = IssueIdentityForm(data={
            'user_identifier': '123456',
            'private_key': 'test_private_key'
        })
        self.assertTrue(form.validate())

    def test_invalid_issue_identity_form(self):
        # Simulate an invalid form submission
        form = IssueIdentityForm(data={
            'user_identifier': '',  # Missing user identifier
            'private_key': ''  # Missing private key
        })
        self.assertFalse(form.validate())
        self.assertIn('user_identifier', form.errors)
        self.assertIn('private_key', form.errors)

if __name__ == '__main__':
    unittest.main()
