"""This module contains the tests for the contributors.py module"""

import unittest
from unittest.mock import patch, MagicMock
from contributors import get_contributors


class TestContributors(unittest.TestCase):
    """
    Test case for the contributors module.
    """

    @patch("contributors.contributor_stats.ContributorStats")
    @patch("contributors.commits.get_commits")
    def test_get_contributors(self, mock_get_commits, mock_contributor_stats):
        """
        Test the get_contributors function.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = "100"
        mock_repo.contributors.return_value = [mock_user]
        mock_github_connection = MagicMock()

        get_contributors(mock_repo, mock_github_connection, "2022-01-01", "2022-12-31")

        mock_contributor_stats.assert_called_once_with(
            "user",
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            "100",
            mock_get_commits.return_value,
        )


if __name__ == "__main__":
    unittest.main()
