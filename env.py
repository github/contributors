"""A GitHub Action that given an organization or repository, produces information about the contributors over the specified time period."""

import os
from os.path import dirname, join
from dotenv import load_dotenv


def get_env_vars() -> tuple[str, str, str, str, str, str, str]:
    """
    Get the environment variables for use in the action.

    Args:
        None

    Returns:
        str: the organization to get contributor information for
        str: the repository to get contributor information for
        str: the GitHub token to use for authentication
        str: the GitHub Enterprise URL to use for authentication
        str: the start date to get contributor information from
        str: the end date to get contributor information to.
        str: whether to get sponsor information on the contributor

    """
    # Load from .env file if it exists
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

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

    ghe = os.getenv("GH_ENTERPRISE_URL", default="").strip()

    start_date = os.getenv("START_DATE")
    # make sure that start date is in the format YYYY-MM-DD
    if start_date and len(start_date) != 10:
        raise ValueError("START_DATE environment variable not in the format YYYY-MM-DD")

    end_date = os.getenv("END_DATE")
    # make sure that end date is in the format YYYY-MM-DD
    if end_date and len(end_date) != 10:
        raise ValueError("END_DATE environment variable not in the format YYYY-MM-DD")

    sponsor_info = os.getenv("SPONSOR_INFO")
    # make sure that sponsor_string is a boolean
    sponsor_info = sponsor_info.lower().strip()
    if sponsor_info not in ["true", "false", ""]:
        raise ValueError(
            "SPONSOR_INFO environment variable not a boolean. ie. True or False or blank"
        )

    return organization, repository, token, ghe, start_date, end_date, sponsor_info
