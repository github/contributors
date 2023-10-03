"""This is the module that contains functions related to authenticating to GitHub with a personal access token."""

import os
import github3


def auth_to_github():
    """Connect to GitHub.com or GitHub Enterprise, depending on env variables."""
    ghe = os.getenv("GH_ENTERPRISE_URL", default="").strip()
    token = os.getenv("GH_TOKEN")
    if ghe and token:
        github_connection = github3.github.GitHubEnterprise(ghe, token=token)
    elif token:
        github_connection = github3.login(token=os.getenv("GH_TOKEN"))
    else:
        raise ValueError("GH_TOKEN environment variable not set")

    if not github_connection:
        raise ValueError("Unable to authenticate to GitHub")
    return github_connection  # type: ignore
