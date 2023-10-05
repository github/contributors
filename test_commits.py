"""This module contains the tests for the commits module."""
import unittest
from unittest.mock import patch, MagicMock
from commits import get_commits


class TestCommits(unittest.TestCase):
    """
    Test case for the commits module.
    """

    @patch("github3.search.commit.CommitSearchResult")
    @patch("github3.github.GitHubEnterprise.search_commits")
    def test_get_commits(self, mock_search_commits, mock_commit_search_result):
        """
        Test the get_commits function.
        """
        mock_repo = MagicMock()
        mock_repo.full_name = "org/repo"
        mock_github_connection = MagicMock()
        mock_github_connection.search_commits = mock_search_commits
        mock_search_commits.return_value = mock_commit_search_result

        result = get_commits(
            "author", mock_repo, mock_github_connection, "2022-01-01", "2022-12-31"
        )

        self.assertEqual(result, mock_commit_search_result)
        mock_search_commits.assert_called_once_with(
            "repo:org/repo author:author merge:false committer-date:2022-01-01..2022-12-31"
        )


if __name__ == "__main__":
    unittest.main()
