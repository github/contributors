"""This module builds out the default data structure for the contributors stats object."""

# [
#   {
#     "username" : "zkoppert",
#     "new_contributor" : "False",
#     "avatar_url" : "https://avatars.githubusercontent.com/u/29484535?v=4",
#     "contribution_count" : "1261",
#     "commit_url" : "https://github.com/github/contributors/commits?author=zkoppert&since=2023-10-01&until=2023-10-05"
#   }
# ]


class ContributorStats:
    """A class to represent a contributor_stats object"""

    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """Create a new contributor_stats object"""
        return super().__new__(cls)

    def __init__(
        self, username, new_contributor, avatar_url, contribution_count, commit_url
    ):
        """Initialize the contributor_stats object"""
        new_contributor = False
        self.username = username
        self.new_contributor = new_contributor
        self.avatar_url = avatar_url
        self.contribution_count = contribution_count
        self.commit_url = commit_url

    def __repr__(self) -> str:
        """Return the representation of the contributor_stats object"""
        return (
            f"contributor_stats(username={self.username}, "
            f"new_contributor={self.new_contributor}, "
            f"avatar_url={self.avatar_url}, "
            f"contribution_count={self.contribution_count}, commit_url={self.commit_url})"
        )


def is_new_contributor(username: str, returning_contributors: list) -> bool:
    """Check if the contributor is new or returning"""
    if username in returning_contributors:
        return True
    return False
