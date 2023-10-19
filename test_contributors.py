"""This module contains the tests for the contributors.py module"""

import unittest
from unittest.mock import patch, MagicMock
from contributor_stats import ContributorStats
from contributors import get_contributors, get_all_contributors


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
        mock_user.contributions_count = 100
        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"

        get_contributors(mock_repo, "2022-01-01", "2022-12-31")

        mock_contributor_stats.assert_called_once_with(
            "user",
            False,
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            100,
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
            "",
        )

    @patch("contributors.get_contributors")
    def test_get_all_contributors_with_organization(self, mock_get_contributors):
        """
        Test the get_all_contributors function when an organization is provided.
        """
        mock_github_connection = MagicMock()
        mock_github_connection.organization().repositories.return_value = [
            "repo1",
            "repo2",
        ]
        mock_get_contributors.return_value = [
            ContributorStats(
                "user",
                False,
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                100,
                "commit_url",
                "sponsor_url_1",
            ),
        ]

        result = get_all_contributors(
            "org", "", "2022-01-01", "2022-12-31", mock_github_connection
        )

        self.assertEqual(
            result,
            [
                ContributorStats(
                    "user",
                    False,
                    "https://avatars.githubusercontent.com/u/29484535?v=4",
                    200,
                    "commit_url, commit_url",
                    "sponsor_url_1",
                ),
            ],
        )
        mock_get_contributors.assert_any_call("repo1", "2022-01-01", "2022-12-31")
        mock_get_contributors.assert_any_call("repo2", "2022-01-01", "2022-12-31")

    @patch("contributors.get_contributors")
    def test_get_all_contributors_with_repository(self, mock_get_contributors):
        """
        Test the get_all_contributors function when a repository is provided.
        """
        mock_github_connection = MagicMock()
        mock_github_connection.repository.return_value = "repo"
        mock_get_contributors.return_value = [
            ContributorStats(
                "user",
                False,
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                100,
                "commit_url2",
                "sponsor_url_2",
            )
        ]

        result = get_all_contributors(
            "", ["owner/repo"], "2022-01-01", "2022-12-31", mock_github_connection
        )

        self.assertEqual(
            result,
            [
                ContributorStats(
                    "user",
                    False,
                    "https://avatars.githubusercontent.com/u/29484535?v=4",
                    100,
                    "commit_url2",
                    "sponsor_url_2",
                ),
            ],
        )
        mock_get_contributors.assert_called_once_with(
            "repo", "2022-01-01", "2022-12-31"
        )

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_skip_users_with_no_commits(self, mock_contributor_stats):
        """
        Test the get_contributors function skips users with no commits in the date range.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = 100
        mock_user2 = MagicMock()
        mock_user2.login = "user2"
        mock_user2.avatar_url = "https://avatars.githubusercontent.com/u/12345679?v=4"
        mock_user2.contributions_count = 102

        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"
        mock_repo.get_commits.side_effect = StopIteration

        get_contributors(mock_repo, "2022-01-01", "2022-12-31")

        # Note that only user is returned and user2 is not returned here because there were no commits in the date range
        mock_contributor_stats.assert_called_once_with(
            "user",
            False,
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            100,
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
            "",
        )


if __name__ == "__main__":
    unittest.main()
