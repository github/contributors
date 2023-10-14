"""This is the test module for the env module."""

import unittest
from unittest.mock import patch
import env


class TestEnv(unittest.TestCase):
    """
    Test case for the env module.
    """

    @patch("os.getenv")
    def test_get_env_vars(self, mock_getenv):
        """
        Test the get_env_vars function when all environment variables are set correctly.
        """
        mock_getenv.side_effect = [
            "org",
            "repo",
            "token",
            "",
            "2022-01-01",
            "2022-12-31",
            "False",
        ]

        (
            organization,
            repository,
            token,
            ghe,
            start_date,
            end_date,
            sponsor_info,
        ) = env.get_env_vars()

        self.assertEqual(organization, "org")
        self.assertEqual(repository, "repo")
        self.assertEqual(token, "token")
        self.assertEqual(ghe, "")
        self.assertEqual(start_date, "2022-01-01")
        self.assertEqual(end_date, "2022-12-31")
        self.assertEqual(sponsor_info, "false")

    @patch("os.getenv")
    def test_get_env_vars_missing_values(self, mock_getenv):
        """
        Test the get_env_vars function when none of the environment variables are set.
        Expect a ValueError to be raised.
        """
        mock_getenv.side_effect = [None, None, None, None, None, None, None]

        with self.assertRaises(ValueError):
            env.get_env_vars()


if __name__ == "__main__":
    unittest.main()
