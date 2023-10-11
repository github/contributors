"""This module contains the tests for the ContributorStats class."""

import unittest
from contributor_stats import ContributorStats, merge_contributors


class TestContributorStats(unittest.TestCase):
    """
    Test case for the ContributorStats class.
    """

    def setUp(self):
        """
        Set up a ContributorStats instance for use in tests.
        """
        self.contributor = ContributorStats(
            "zkoppert",
            False,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            1261,
            "commit_url5",
        )

    def test_init(self):
        """
        Test the __init__ method of the ContributorStats class.
        """
        self.assertEqual(self.contributor.username, "zkoppert")
        self.assertEqual(self.contributor.new_contributor, False)
        self.assertEqual(
            self.contributor.avatar_url,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
        )
        self.assertEqual(self.contributor.contribution_count, 1261)
        self.assertEqual(
            self.contributor.commit_url,
            "commit_url5",
        )

    def test_merge_contributors(self):
        """
        Test the merge_contributors function.
        """
        contributor1 = ContributorStats(
            "user1",
            False,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            100,
            "commit_url1",
        )
        contributor2 = ContributorStats(
            "user2",
            False,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            200,
            "commit_url2",
        )
        contributor3 = ContributorStats(
            "user1",
            False,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            150,
            "commit_url1",
        )
        all_contributors = [
            [
                contributor1,
                contributor2,
                contributor3,
            ]
        ]
        expected_result = [
            ContributorStats(
                "user1",
                False,
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                250,
                "commit_url1",
            ),
            ContributorStats(
                "user2",
                False,
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                200,
                "commit_url2",
            ),
        ]

        result = merge_contributors(all_contributors)

        self.assertTrue(expected_result == result)


if __name__ == "__main__":
    unittest.main()
