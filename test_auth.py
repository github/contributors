"""Test cases for the auth module."""
import unittest
from unittest.mock import patch
import auth


class TestAuth(unittest.TestCase):
    """
    Test case for the auth module.
    """

    @patch("os.getenv")
    @patch("github3.github.GitHubEnterprise")
    def test_auth_to_github_enterprise(self, mock_github_enterprise, mock_getenv):
        """
        Test the auth_to_github function when the GH_ENTERPRISE_URL and GH_TOKEN environment variables are set.
        """
        mock_getenv.side_effect = ["https://github.enterprise.com", "token"]
        mock_github_enterprise.return_value = "Authenticated to GitHub Enterprise"

        result = auth.auth_to_github()

        self.assertEqual(result, "Authenticated to GitHub Enterprise")

    @patch("github3.login")
    @patch("os.getenv")
    def test_auth_to_github_com(self, mock_login, mock_getenv):
        """
        Test the auth_to_github function when only the GH_TOKEN environment variable is set.
        """
        mock_getenv.side_effect = ["", "token"]
        mock_login.return_value = "Authenticated to GitHub.com"

        result = auth.auth_to_github()

        self.assertEqual(result.url, "Authenticated to GitHub.com")

    @patch("os.getenv")
    def test_auth_to_github_no_token(self, mock_getenv):
        """
        Test the auth_to_github function when the GH_TOKEN environment variable is not set.
        Expect a ValueError to be raised.
        """
        mock_getenv.side_effect = ["", ""]

        with self.assertRaises(ValueError):
            auth.auth_to_github()


if __name__ == "__main__":
    unittest.main()
