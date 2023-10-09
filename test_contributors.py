"""This module contains the tests for the contributors.py module"""

import unittest
from unittest.mock import patch, MagicMock
from contributors import get_contributors


class TestContributors(unittest.TestCase):
    """
    Test case for the contributors module.
    """

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors(self, mock_contributor_stats):
        """
        Test the get_contributors function.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = "100"
        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"

        get_contributors(mock_repo, "2022-01-01", "2022-12-31")

        mock_contributor_stats.assert_called_once_with(
            "user",
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            "100",
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
        )


if __name__ == "__main__":
    unittest.main()
