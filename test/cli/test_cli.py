# tests/cli/test_cli.py
import unittest
from unittest.mock import patch
from src.cli.main import main

class TestCLI(unittest.TestCase):

    @patch('sys.argv', ['letsid', 'register'])
    @patch('builtins.print')
    def test_register_command(self, mock_print):
        """
        Test the register command of the CLI.
        """
        try:
            main()
        except SystemExit:
            pass  # main() may call sys.exit(), so catch SystemExit to prevent test from exiting
        mock_print.assert_called_with('Registration result: success')  # Adjust expected output

    @patch('sys.argv', ['letsid', 'issue'])
    @patch('builtins.print')
    def test_issue_command(self, mock_print):
        """
        Test the issue command of the CLI.
        """
        try:
            main()
        except SystemExit:
            pass  # Handle potential sys.exit() from the CLI
        mock_print.assert_called_with('Issuance result: success')  # Adjust expected output

if __name__ == '__main__':
    unittest.main()
