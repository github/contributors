"""This module contains the tests for the contributors.py module"""

import unittest
from unittest.mock import MagicMock, patch

from contributor_stats import ContributorStats
from contributors import (
    get_all_contributors,
    get_coauthor_contributors,
    get_coauthors_from_message,
    get_contributors,
)


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

        get_contributors(mock_repo, "2022-01-01", "2022-12-31", "", False, None)

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
        ghe = ""

        result = get_all_contributors(
            "org", "", "2022-01-01", "2022-12-31", mock_github_connection, ghe, False
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
        mock_get_contributors.assert_any_call(
            "repo1", "2022-01-01", "2022-12-31", ghe, False, mock_github_connection
        )
        mock_get_contributors.assert_any_call(
            "repo2", "2022-01-01", "2022-12-31", ghe, False, mock_github_connection
        )

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
        ghe = ""

        result = get_all_contributors(
            "",
            ["owner/repo"],
            "2022-01-01",
            "2022-12-31",
            mock_github_connection,
            ghe,
            False,
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
            "repo", "2022-01-01", "2022-12-31", ghe, False, mock_github_connection
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
        ghe = ""

        get_contributors(mock_repo, "2022-01-01", "2022-12-31", ghe, False, None)

        # Note that only user is returned and user2 is not returned here because there were no commits in the date range
        mock_contributor_stats.assert_called_once_with(
            "user",
            False,
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            100,
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
            "",
        )

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_skip_bot(self, mock_contributor_stats):
        """
        Test if the get_contributors function skips the bot user.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "[bot]"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = 100

        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"
        mock_repo.get_commits.side_effect = StopIteration
        ghe = ""

        get_contributors(mock_repo, "2022-01-01", "2022-12-31", ghe, False, None)

        # Note that only user is returned and user2 is not returned here because there were no commits in the date range
        mock_contributor_stats.isEmpty()

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_no_commit_end_date(self, mock_contributor_stats):
        """
        Test the get_contributors does the search of commits only with start date
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = 100

        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"
        mock_repo.get_commits.side_effect = StopIteration
        ghe = ""

        get_contributors(mock_repo, "2022-01-01", "", ghe, False, None)

        # Note that only user is returned and user2 is not returned here because there were no commits in the date range
        mock_contributor_stats.assert_called_once_with(
            "user",
            False,
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            100,
            "https://github.com/owner/repo/commits?author=user",
            "",
        )


class TestCoauthorFunctions(unittest.TestCase):
    """
    Test case for the co-author related functions in the contributors module.
    """

    def test_get_coauthors_from_message_with_noreply_email(self):
        """
        Test extracting co-authors from a commit message with noreply email.
        """
        message = """Fix bug in login

Co-authored-by: John Doe <johndoe@users.noreply.github.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["johndoe"])

    def test_get_coauthors_from_message_with_noreply_email_with_id(self):
        """
        Test extracting co-authors from a commit message with noreply email containing ID prefix.
        """
        message = """Fix bug in login

Co-authored-by: John Doe <12345678+johndoe@users.noreply.github.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["johndoe"])

    def test_get_coauthors_from_message_multiple_coauthors(self):
        """
        Test extracting multiple co-authors from a commit message.
        """
        message = """Feature implementation

Co-authored-by: Alice <alice@users.noreply.github.com>
Co-authored-by: Bob <bob@users.noreply.github.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["alice", "bob"])

    def test_get_coauthors_from_message_with_regular_email(self):
        """
        Test that regular emails are extracted as co-authors.
        """
        message = """Fix bug

Co-authored-by: John Doe <john@example.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["john@example.com"])

    def test_get_coauthors_from_message_case_insensitive(self):
        """
        Test that co-authored-by is case insensitive.
        """
        message = """Fix bug

co-authored-by: John Doe <johndoe@users.noreply.github.com>
CO-AUTHORED-BY: Jane Doe <janedoe@users.noreply.github.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["johndoe", "janedoe"])

    def test_get_coauthors_from_message_empty_message(self):
        """
        Test extracting co-authors from an empty commit message.
        """
        result = get_coauthors_from_message("", None)
        self.assertEqual(result, [])

    def test_get_coauthors_from_message_no_coauthors(self):
        """
        Test extracting co-authors from a commit message without co-authors.
        """
        message = "Fix bug in login system"
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, [])

    def test_get_coauthors_from_message_mixed_email_types(self):
        """
        Test extracting co-authors with both GitHub noreply and regular emails.
        """
        message = """Feature implementation

Co-authored-by: Alice <alice@users.noreply.github.com>
Co-authored-by: Bob <bob@example.com>
Co-authored-by: Charlie <12345+charlie@users.noreply.github.com>
"""
        result = get_coauthors_from_message(message, None)
        self.assertEqual(result, ["alice", "bob@example.com", "charlie"])

    def test_get_coauthor_contributors(self):
        """
        Test the get_coauthor_contributors function.
        """
        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"

        mock_commit1 = MagicMock()
        mock_commit1.commit.message = """Feature implementation

Co-authored-by: Alice <alice@users.noreply.github.com>
"""

        mock_commit2 = MagicMock()
        mock_commit2.commit.message = """Bug fix

Co-authored-by: Alice <alice@users.noreply.github.com>
Co-authored-by: Bob <bob@users.noreply.github.com>
"""

        mock_repo.commits.return_value = [mock_commit1, mock_commit2]

        result = get_coauthor_contributors(
            mock_repo, "2022-01-01", "2022-12-31", "", None
        )

        # Alice should have count 2, Bob should have count 1
        self.assertEqual(len(result), 2)
        usernames = {c.username for c in result}
        self.assertIn("alice", usernames)
        self.assertIn("bob", usernames)

        # Check counts
        for contributor in result:
            if contributor.username == "alice":
                self.assertEqual(contributor.contribution_count, 2)
            elif contributor.username == "bob":
                self.assertEqual(contributor.contribution_count, 1)

    def test_get_coauthor_contributors_includes_all(self):
        """
        Test that get_coauthor_contributors includes all co-authors, even if they are already main contributors.
        """
        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"

        mock_commit = MagicMock()
        mock_commit.commit.message = """Feature

Co-authored-by: Alice <alice@users.noreply.github.com>
Co-authored-by: Bob <bob@users.noreply.github.com>
"""

        mock_repo.commits.return_value = [mock_commit]

        # Alice is already a main contributor, but should still be included in co-author results
        result = get_coauthor_contributors(
            mock_repo, "2022-01-01", "2022-12-31", "", None
        )

        # Both Alice and Bob should be in the result
        self.assertEqual(len(result), 2)
        usernames = {c.username for c in result}
        self.assertIn("alice", usernames)
        self.assertIn("bob", usernames)

    @patch("contributors.get_coauthor_contributors")
    def test_get_contributors_with_acknowledge_coauthors(
        self, mock_get_coauthor_contributors
    ):
        """
        Test that get_contributors calls get_coauthor_contributors when acknowledge_coauthors is True.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = 100
        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"

        mock_coauthor = ContributorStats(
            "coauthor",
            False,
            "",
            1,
            "https://github.com/owner/repo/commits?author=coauthor&since=2022-01-01&until=2022-12-31",
            "",
        )
        mock_get_coauthor_contributors.return_value = [mock_coauthor]

        result = get_contributors(
            mock_repo,
            "2022-01-01",
            "2022-12-31",
            "",
            acknowledge_coauthors=True,
            github_connection=None,
        )

        # Verify that get_coauthor_contributors was called
        mock_get_coauthor_contributors.assert_called_once()

        # Verify that the result includes both the regular contributor and the co-author
        self.assertEqual(len(result), 2)
        usernames = [c.username for c in result]
        self.assertIn("user", usernames)
        self.assertIn("coauthor", usernames)


if __name__ == "__main__":
    unittest.main()
