"""This module contains the tests for the ContributorStats class."""

import unittest
from contributor_stats import ContributorStats


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
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            "1261",
            {
                "744d20e": "2023-06-29 09:43:24 -0700",
                "5c622f9": "2023-06-29 15:55:38 -0700",
            },
        )

    def test_init(self):
        """
        Test the __init__ method of the ContributorStats class.
        """
        self.assertEqual(self.contributor.username, "zkoppert")
        self.assertEqual(
            self.contributor.avatar_url,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
        )
        self.assertEqual(self.contributor.contribution_count, "1261")
        self.assertEqual(
            self.contributor.commits,
            {
                "744d20e": "2023-06-29 09:43:24 -0700",
                "5c622f9": "2023-06-29 15:55:38 -0700",
            },
        )


if __name__ == "__main__":
    unittest.main()
