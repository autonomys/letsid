# tests/web/test_app.py
import sys
sys.path.append('/root/letsid-draft/src')
print(sys.path)
import unittest
from flask import url_for
from src.web.app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Configure the Flask test client and propagate the exceptions to the test client
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF tokens for testing
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_index_route(self):
        # Test the index route
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to LetsID', response.data)  # Adjust based on your index page content

    def test_register_route_get(self):
        # Test the GET request for the register route
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register Form', response.data)  # Adjust based on your register form content

    def test_register_route_post(self):
        # Test the POST request for the register route
        # Adjust the data payload as per your form fields
        response = self.client.post(url_for('register'), data={
            'oidc_token': 'test_oidc_token'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful.', response.data)

    def test_issue_identity_route_get(self):
        # Test the GET request for the issue identity route
        response = self.client.get(url_for('issue_identity_route'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Issue Identity Form', response.data)  # Adjust based on your form content

    def test_issue_identity_route_post(self):
        # Test the POST request for the issue identity route
        # Adjust the data payload as per your form fields
        response = self.client.post(url_for('issue_identity_route'), data={
            'user_private_key': 'test_private_key',
            'user_identifier': 'test_identifier'
        }, follow_redirects=True)
        self.assertIn(b'Identity issued successfully.', response.data)

if __name__ == '__main__':
    unittest.main()
