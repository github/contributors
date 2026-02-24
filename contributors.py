# pylint: disable=broad-exception-caught
"""This file contains the main() and other functions needed to get contributor information from the organization or repository"""

import re
from typing import Dict, List, Optional

import auth
import contributor_stats
import env
import json_writer
import markdown


def main():
    """Run the main program"""

    # Get environment variables
    (
        organization,
        repository_list,
        gh_app_id,
        gh_app_installation_id,
        gh_app_private_key,
        gh_app_enterprise_only,
        token,
        ghe,
        start_date,
        end_date,
        sponsor_info,
        link_to_profile,
        acknowledge_coauthors,
    ) = env.get_env_vars()

    # Auth to GitHub.com
    github_connection = auth.auth_to_github(
        token,
        gh_app_id,
        gh_app_installation_id,
        gh_app_private_key,
        ghe,
        gh_app_enterprise_only,
    )

    if not token and gh_app_id and gh_app_installation_id and gh_app_private_key:
        token = auth.get_github_app_installation_token(
            ghe, gh_app_id, gh_app_private_key, gh_app_installation_id
        )

    # Get the contributors
    contributors = get_all_contributors(
        organization,
        repository_list,
        start_date,
        end_date,
        github_connection,
        ghe,
        acknowledge_coauthors,
    )

    # Check for new contributor if user provided start_date and end_date
    if start_date and end_date:
        # get the list of contributors from before start_date
        # so we can see if contributors after start_date are new or returning
        returning_contributors = get_all_contributors(
            organization,
            repository_list,
            start_date="2008-02-29",  # GitHub was founded on 2008-02-29
            end_date=start_date,
            github_connection=github_connection,
            ghe=ghe,
            acknowledge_coauthors=acknowledge_coauthors,
        )
        for contributor in contributors:
            contributor.new_contributor = contributor_stats.is_new_contributor(
                contributor.username, returning_contributors
            )

    # Get sponsor information on the contributor
    if sponsor_info == "true":
        contributors = contributor_stats.get_sponsor_information(
            contributors, token, ghe
        )
    # Output the contributors information
    # print(contributors)
    markdown.write_to_markdown(
        contributors,
        "contributors.md",
        start_date,
        end_date,
        organization,
        repository_list,
        sponsor_info,
        link_to_profile,
        ghe,
    )
    json_writer.write_to_json(
        filename="contributors.json",
        start_date=start_date,
        end_date=end_date,
        organization=organization,
        repository_list=repository_list,
        sponsor_info=sponsor_info,
        link_to_profile=link_to_profile,
        contributors=contributors,
    )


def get_all_contributors(
    organization: str,
    repository_list: List[str],
    start_date: str,
    end_date: str,
    github_connection: object,
    ghe: str,
    acknowledge_coauthors: bool,
):
    """
    Get all contributors from the organization or repository

    Args:
        organization (str): The organization for which the contributors are being listed.
        repository_list (List[str]): The repository list for which the contributors are being listed.
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.
        github_connection (object): The authenticated GitHub connection object from PyGithub
        ghe (str): The GitHub Enterprise URL to use for authentication
        acknowledge_coauthors (bool): Whether to acknowledge co-authors from commit messages

    Returns:
        all_contributors (list): A list of ContributorStats objects
    """
    repos = []
    if organization:
        repos = github_connection.organization(organization).repositories()
    else:
        repos = []
        for repo in repository_list:
            owner, repo_name = repo.split("/")
            repository_obj = github_connection.repository(owner, repo_name)
            repos.append(repository_obj)

    all_contributors = []
    if repos:
        for repo in repos:
            repo_contributors = get_contributors(
                repo,
                start_date,
                end_date,
                ghe,
                acknowledge_coauthors,
                github_connection,
            )
            if repo_contributors:
                all_contributors.append(repo_contributors)

    # Check for duplicates and merge when usernames are equal
    all_contributors = contributor_stats.merge_contributors(all_contributors)

    return all_contributors


def get_coauthors_from_message(
    commit_message: str,
    github_connection: object = None,
    email_cache: Optional[Dict[str, str]] = None,
) -> List[str]:
    """
    Extract co-author identifiers from a commit message.

    Co-authored-by trailers follow the format:
    Co-authored-by: Name <email>

    For GitHub noreply emails (username@users.noreply.github.com), extracts the username.
    For @github.com emails, extracts the username (part before @).
    For other emails, uses GitHub Search Users API to find the username, or falls back to email.

    Args:
        commit_message (str): The commit message to parse
        github_connection (object): The authenticated GitHub connection object from PyGithub
        email_cache (dict): Optional cache mapping emails to resolved usernames to avoid
            redundant API calls

    Returns:
        List[str]: List of co-author identifiers (GitHub usernames or email addresses)
    """
    # Match Co-authored-by trailers - case insensitive
    # Format: Co-authored-by: Name <email>
    pattern = r"Co-authored-by:\s*[^<]*<([^>]+)>"
    matches = re.findall(pattern, commit_message, re.IGNORECASE)

    identifiers = []
    for email in matches:
        # Check if it's a GitHub noreply email format: username@users.noreply.github.com
        noreply_pattern = r"^(\d+\+)?([^@]+)@users\.noreply\.github\.com$"
        noreply_match = re.match(noreply_pattern, email)
        if noreply_match:
            # For GitHub noreply emails, extract just the username
            identifiers.append(noreply_match.group(2))
        elif email.endswith("@github.com"):
            # For @github.com emails, extract the username (part before @)
            username = email.split("@")[0]
            identifiers.append(username)
        else:
            # For other emails, check cache first, then try Search Users API
            if email_cache is not None and email in email_cache:
                identifiers.append(email_cache[email])
            elif github_connection:
                try:
                    # Search for users by email
                    search_result = github_connection.search_users(f"email:{email}")
                    if search_result.totalCount > 0:
                        # Use the first matching user's login
                        resolved = search_result[0].login
                    else:
                        # If no user found, fall back to email address
                        resolved = email
                    if email_cache is not None:
                        email_cache[email] = resolved
                    identifiers.append(resolved)
                except Exception:
                    # If API call fails, fall back to email address
                    if email_cache is not None:
                        email_cache[email] = email
                    identifiers.append(email)
            else:
                # If no GitHub connection available, use the full email address
                identifiers.append(email)
    return identifiers


def get_contributors(
    repo: object,
    start_date: str,
    end_date: str,
    ghe: str,
    acknowledge_coauthors: bool,
    github_connection: object,
):
    """
    Get contributors from a single repository and filter by start end dates if present.

    Args:
        repo (object): The repository object from PyGithub
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.
        ghe (str): The GitHub Enterprise URL to use for authentication
        acknowledge_coauthors (bool): Whether to acknowledge co-authors from commit messages
        github_connection (object): The authenticated GitHub connection object from PyGithub

    Returns:
        contributors (list): A list of ContributorStats objects
    """
    all_repo_contributors = repo.contributors()
    contributors = []
    # Track usernames already added as contributors
    contributor_usernames = set()

    try:
        for user in all_repo_contributors:
            # Ignore contributors with [bot] in their name
            if "[bot]" in user.login:
                continue

            # Check if user has commits in the date range
            if start_date and end_date:
                user_commits = repo.commits(
                    author=user.login, since=start_date, until=end_date
                )

                # If the user has no commits in the date range, skip them
                try:
                    next(user_commits)
                except StopIteration:
                    continue

            # Store the contributor information in a ContributorStats object
            endpoint = ghe if ghe else "https://github.com"
            if start_date and end_date:
                commit_url = f"{endpoint}/{repo.full_name}/commits?author={user.login}&since={start_date}&until={end_date}"
            else:
                commit_url = f"{endpoint}/{repo.full_name}/commits?author={user.login}"
            contributor = contributor_stats.ContributorStats(
                user.login,
                False,
                user.avatar_url,
                user.contributions_count,
                commit_url,
                "",
            )
            contributors.append(contributor)
            contributor_usernames.add(user.login)

        # Get co-authors from commit messages if enabled
        if acknowledge_coauthors:
            coauthor_contributors = get_coauthor_contributors(
                repo,
                start_date,
                end_date,
                ghe,
                github_connection,
            )
            # Only add co-authors not already in the contributor list for this repo
            for coauthor in coauthor_contributors:
                if coauthor.username not in contributor_usernames:
                    contributors.append(coauthor)
                    contributor_usernames.add(coauthor.username)

    except Exception as e:
        print(f"Error getting contributors for repository: {repo.full_name}")
        print(e)
        return None

    return contributors


def get_coauthor_contributors(
    repo: object,
    start_date: str,
    end_date: str,
    ghe: str,
    github_connection: object,
) -> List[contributor_stats.ContributorStats]:
    """
    Get contributors who were co-authors on commits in the repository.

    Args:
        repo (object): The repository object
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.
        ghe (str): The GitHub Enterprise URL
        github_connection (object): The authenticated GitHub connection object from PyGithub

    Returns:
        List[ContributorStats]: A list of ContributorStats objects for co-authors
    """
    coauthor_counts: dict = {}  # username -> count
    endpoint = ghe if ghe else "https://github.com"
    # cache email -> username lookups to avoid redundant API calls
    email_cache: Dict[str, str] = {}

    try:
        # Get all commits in the date range
        if start_date and end_date:
            commits = repo.commits(since=start_date, until=end_date)
        else:
            commits = repo.commits()

        for commit in commits:
            # Get commit message from the commit object
            commit_message = commit.commit.message if commit.commit else ""
            if not commit_message:
                continue

            # Extract co-authors from commit message
            coauthors = get_coauthors_from_message(
                commit_message, github_connection, email_cache
            )
            for username in coauthors:
                # Skip bot accounts for consistency with regular contributor filtering
                if "[bot]" in username.lower():
                    continue
                coauthor_counts[username] = coauthor_counts.get(username, 0) + 1

    except Exception as e:
        print(f"Error getting co-authors for repository: {repo.full_name}")
        print(e)
        return []

    # Create ContributorStats objects for co-authors
    coauthor_contributors = []
    for username, count in coauthor_counts.items():
        if start_date and end_date:
            commit_url = f"{endpoint}/{repo.full_name}/commits?author={username}&since={start_date}&until={end_date}"
        else:
            commit_url = f"{endpoint}/{repo.full_name}/commits?author={username}"

        contributor = contributor_stats.ContributorStats(
            username,
            False,
            "",  # No avatar URL available for co-authors
            count,
            commit_url,
            "",
        )
        coauthor_contributors.append(contributor)

    return coauthor_contributors


if __name__ == "__main__":
    main()
