"""
A GitHub Action that given an organization or repository,
produces information about the contributors over the specified time period.
"""

import datetime
import os
from os.path import dirname, join

from dotenv import load_dotenv
from dataclasses import dataclass


def get_bool_env_var(env_var_name: str, default: bool = False) -> bool:
    """Get a boolean environment variable.

    Args:
        env_var_name: The name of the environment variable to retrieve.
        default: The default value to return if the environment variable is not set.

    Returns:
        The value of the environment variable as a boolean.
    """
    ev = os.environ.get(env_var_name, "")
    if ev == "" and default:
        return default
    return ev.strip().lower() == "true"


def get_int_env_var(env_var_name: str) -> int | None:
    """Get an integer environment variable.

    Args:
        env_var_name: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable as an integer or None.
    """
    env_var = os.environ.get(env_var_name)
    if env_var is None or not env_var.strip():
        return None
    try:
        return int(env_var)
    except ValueError:
        return None


def validate_date_format(env_var_name: str) -> str:
    """Validate the date format of the environment variable.

    Does nothing if the environment variable is not set.

    Args:
        env_var_name: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable as a string.
    """
    date_to_validate = os.getenv(env_var_name, "")

    if not date_to_validate:
        return date_to_validate

    pattern = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date_to_validate, pattern)
    except ValueError as exc:
        raise ValueError(f"{env_var_name} environment variable not in the format YYYY-MM-DD") from exc
    return date_to_validate


@dataclass
class EnvironmentConfig:
    """
    Environment Configuration
    """

    organization: str
    repositories_list: list[str]
    gh_app_id: int | None
    gh_app_installation_id: int | None
    gh_app_private_key_bytes: bytes
    token: str
    ghe: str
    start_date: str
    end_date: str
    sponsor_info: str
    link_to_profile: str
    show_organisations_list: list[str]
    filename: str = 'contributors'


def get_env_vars(
    test: bool = False,
) -> EnvironmentConfig:
    """
    Get the environment variables for use in the action.

    Args:
        None

    Returns:
        EnvironmentConfig:
            organization, str:
                the organization to get contributor information for
            repositories_list, List[str]:
                A list of the repositories to get contributor information for
            gh_app_id, int|None:
                the GitHub App ID to use for authentication
            gh_app_installation_id, int|None:
                the GitHub App Installation ID to use for authentication
            gh_app_private_key_bytes, bytes:
                the GitHub App Private Key as bytes to use for authentication
            token, str:
                the GitHub token to use for authentication
            ghe, str:
                the GitHub Enterprise URL to use for authentication
            start_date, str,
                the start date to get contributor information from
            end_date, str:
                the end date to get contributor information to.
            sponsor_info, str:
                whether to get sponsor information on the contributor
            link_to_profile, str:
                whether to link username to Github profile in markdown output
            show_organisations_list, list:
                Organisations to show in order of preference

    """

    if not test:
        dotenv_path = join(dirname(__file__), ".env")
        load_dotenv(dotenv_path)

    organization = os.getenv("ORGANIZATION")
    repositories_str = os.getenv("REPOSITORY")
    # Either organization or repository must be set
    if not organization and not repositories_str:
        raise ValueError("ORGANIZATION and REPOSITORY environment variables were not set. Please set one")

    gh_app_id = get_int_env_var("GH_APP_ID")
    gh_app_private_key_bytes = os.environ.get("GH_APP_PRIVATE_KEY", "").encode("utf8")
    gh_app_installation_id = get_int_env_var("GH_APP_INSTALLATION_ID")

    if gh_app_id and (not gh_app_private_key_bytes or not gh_app_installation_id):
        raise ValueError("GH_APP_ID set and GH_APP_INSTALLATION_ID or GH_APP_PRIVATE_KEY variable not set")

    token = os.getenv("GH_TOKEN", "")
    if not gh_app_id and not gh_app_private_key_bytes and not gh_app_installation_id and not token:
        raise ValueError("GH_TOKEN environment variable not set")

    ghe = os.getenv("GH_ENTERPRISE_URL", default="").strip()
    filename = os.getenv("CONTRIB_FILENAME", default="contributors").strip()

    show_organisations = os.getenv("SHOW_ORGANISATIONS", default="").strip()

    start_date = validate_date_format("START_DATE")
    end_date = validate_date_format("END_DATE")

    sponsor_info = get_bool_env_var("SPONSOR_INFO", False)
    link_to_profile = get_bool_env_var("LINK_TO_PROFILE", False)

    # Separate repositories_str into a list based on the comma separator
    repositories_list = []
    if repositories_str:
        repositories_list = [repository.strip() for repository in repositories_str.split(",")]

    show_organisations_list = []
    if show_organisations:
        show_organisations_list = [org.strip() for org in show_organisations.split(",")]

    return EnvironmentConfig(
        organization,
        repositories_list,
        gh_app_id,
        gh_app_installation_id,
        gh_app_private_key_bytes,
        token,
        ghe,
        start_date,
        end_date,
        sponsor_info,
        link_to_profile,
        show_organisations_list,
        filename = filename,
    )
