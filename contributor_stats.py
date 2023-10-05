"""This module builds out the default data structure for the contributors stats object."""

# [
#   {
#     "username" : "zkoppert",
#     "avatar_url" : "https://avatars.githubusercontent.com/u/29484535?v=4",
#     "contribution_count" : "1261",
#     "commits" : {
#        "744d20e": "2023-06-29 09:43:24 -0700",
#        "5c622f9" : "2023-06-29 15:55:38 -0700"
#     },
#   }
# ]


class ContributorStats:
    """A class to represent a contributor_stats object"""

    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """Create a new contributor_stats object"""
        return super().__new__(cls)

    def __init__(self, username, avatar_url, contribution_count, commits):
        """Initialize the contributor_stats object"""
        self.username = username
        self.avatar_url = avatar_url
        self.contribution_count = contribution_count
        self.commits = commits

    def __repr__(self) -> str:
        """Return the representation of the contributor_stats object"""
        return (
            f"contributor_stats(username={self.username}, "
            f"avatar_url={self.avatar_url}, "
            f"contribution_count={self.contribution_count}, commits={self.commits})"
        )
