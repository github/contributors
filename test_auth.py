"""Test cases for the auth module."""

import unittest
from unittest.mock import MagicMock, patch

import auth
import github3.github


class TestAuth(unittest.TestCase):
    """
    Test case for the auth module.
    """

    @patch("github3.github.GitHub.login_as_app_installation")
    def test_auth_to_github_with_github_app(self, mock_login):
        """
        Test the auth_to_github function when GitHub app
        parameters provided.
        """
        mock_login.return_value = MagicMock()
        result = auth.auth_to_github(12345, 678910, b"hello", "", "")

        self.assertIsInstance(result, github3.github.GitHub)

    @patch("github3.login")
    def test_auth_to_github_with_token(self, mock_login):
        """
        Test the auth_to_github function when the token is provided.
        """
        mock_login.return_value = "Authenticated to GitHub.com"

        result = auth.auth_to_github("", "", b"", "token", "")

        self.assertEqual(result, "Authenticated to GitHub.com")

    def test_auth_to_github_without_token(self):
        """
        Test the auth_to_github function when the token is not provided.
        Expect a ValueError to be raised.
        """
        with self.assertRaises(ValueError):
            auth.auth_to_github("", "", b"", "", "")

    @patch("github3.github.GitHubEnterprise")
    def test_auth_to_github_with_ghe(self, mock_ghe):
        """
        Test the auth_to_github function when the GitHub Enterprise URL is provided.
        """
        mock_ghe.return_value = "Authenticated to GitHub Enterprise"
        result = auth.auth_to_github("", "", b"", "token", "https://github.example.com")

        self.assertEqual(result, "Authenticated to GitHub Enterprise")


if __name__ == "__main__":
    unittest.main()
