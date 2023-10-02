"""A GitHub Action that given an organization or repository, produces information about the contributors over the specified time period."""

import os
from typing import List


def get_env_vars() -> tuple[str, str, List[str]]:
    """
    Get the environment variables for use in the action.

    Returns:
        str: the organization to get contributor information for
        str: the repository to get contributor information for
        str: the GitHub token to use for authentication
        str: the start date to get contributor information from
        str: the end date to get contributor information to.
    """
    organization = os.getenv("ORGANIZATION")
    repository = os.getenv("REPOSITORY")
    # Either organization or repository must be set
    if not organization and not repository:
        raise ValueError(
            "ORGANIZATION and repository environment variables were both not set. Please enter a valid value for one of them."
        )

    token = os.getenv("GH_TOKEN")
    # required env variable
    if not token:
        raise ValueError("GH_TOKEN environment variable not set")

    start_date = os.getenv("START_DATE")
    # make sure that start date is in the format YYYY-MM-DD
    if start_date and len(start_date) != 10:
        raise ValueError("START_DATE environment variable not in the format YYYY-MM-DD")

    end_date = os.getenv("END_DATE")
    # make sure that end date is in the format YYYY-MM-DD
    if end_date and len(end_date) != 10:
        raise ValueError("END_DATE environment variable not in the format YYYY-MM-DD")

    return organization, repository, token, start_date, end_date
