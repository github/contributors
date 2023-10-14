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
            False,
            "url",
            100,
            "commit url",
            "sponsor_url_1",
        )
        person2 = contributor_stats.ContributorStats(
            "user2",
            False,
            "url2",
            200,
            "commit url2",
            "sponsor_url_2",
        )
        # Set person2 as a new contributor since this cannot be set on initiatization of the object
        person2.new_contributor = True
        collaborators = [
            person1,
            person2,
        ]

        write_to_markdown(
            collaborators,
            "filename",
            "2023-01-01",
            "2023-01-02",
            None,
            "org/repo",
            "false",
        )

        mock_file.assert_called_once_with("filename", "w", encoding="utf-8")
        mock_file().write.assert_any_call("# Contributors\n\n")
        mock_file().write.assert_any_call(
            "- Date range for contributor list:  2023-01-01 to 2023-01-02\n"
        )
        mock_file().write.assert_any_call(
            "| Total Contributors | Total Contributions | % New Contributors |\n| --- | --- | --- |\n| 2 | 300 | 50.0% |\n\n"
        )
        mock_file().write.assert_any_call(
            "| Username | Contribution Count | New Contributor | Commits |\n"
            "| --- | --- | --- | --- |\n"
            "| user1 | 100 | False | commit url |\n"
            "| user2 | 200 | True | commit url2 |\n"
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_markdown_with_sponsors(self, mock_file):
        """
        Test the write_to_markdown function with sponsors info turned on.
        """
        person1 = contributor_stats.ContributorStats(
            "user1",
            False,
            "url",
            100,
            "commit url",
            "sponsor_url_1",
        )
        person2 = contributor_stats.ContributorStats(
            "user2",
            False,
            "url2",
            200,
            "commit url2",
            "",
        )
        # Set person2 as a new contributor since this cannot be set on initiatization of the object
        person2.new_contributor = True
        collaborators = [
            person1,
            person2,
        ]

        write_to_markdown(
            collaborators,
            "filename",
            "2023-01-01",
            "2023-01-02",
            None,
            "org/repo",
            "true",
        )

        mock_file.assert_called_once_with("filename", "w", encoding="utf-8")
        mock_file().write.assert_any_call("# Contributors\n\n")
        mock_file().write.assert_any_call(
            "- Date range for contributor list:  2023-01-01 to 2023-01-02\n"
        )
        mock_file().write.assert_any_call(
            "| Total Contributors | Total Contributions | % New Contributors |\n| --- | --- | --- |\n| 2 | 300 | 50.0% |\n\n"
        )
        mock_file().write.assert_any_call(
            "| Username | Contribution Count | New Contributor | Sponsor URL | Commits |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| user1 | 100 | False | [Sponsor Link](sponsor_url_1) | commit url |\n"
            "| user2 | 200 | True | not sponsorable | commit url2 |\n"
        )


if __name__ == "__main__":
    unittest.main()
