"""This is the test module for the markdown module"""
import unittest
from unittest.mock import patch, mock_open
from markdown import write_to_markdown
import contributor_stats


class TestMarkdown(unittest.TestCase):
    """
    Test case for the markdown module.
    """

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_markdown(self, mock_file):
        """
        Test the write_to_markdown function.
        """
        person1 = contributor_stats.ContributorStats(
            "user1",
            "url",
            100,
            "commit url",
        )
        person2 = contributor_stats.ContributorStats(
            "user2",
            "url2",
            200,
            "commit url2",
        )
        collaborators = [
            [
                person1,
                person2,
            ]
        ]

        write_to_markdown(collaborators, "filename")

        mock_file.assert_called_once_with("filename", "w", encoding="utf-8")
        mock_file().write.assert_any_call("# Contributors\n\n")
        mock_file().write.assert_any_call(
            "| Username | Contribution Count | Commits |\n| --- | --- | --- |\n| user1 | 100 | commit url |\n| user2 | 200 | commit url2 |\n"
        )


if __name__ == "__main__":
    unittest.main()
