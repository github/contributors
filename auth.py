"""This is the module that contains functions related to authenticating to GitHub with a personal access token."""

import github3


def auth_to_github(token: str) -> github3.GitHub:
    """Connect to GitHub.com or GitHub Enterprise, depending on env variables."""
    if token:
        github_connection = github3.login(token=token)
    else:
        raise ValueError("GH_TOKEN environment variable not set")

    if not github_connection:
        raise ValueError("Unable to authenticate to GitHub")
    return github_connection  # type: ignore
