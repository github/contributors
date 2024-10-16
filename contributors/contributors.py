# pylint: disable=broad-exception-caught
"""This file contains the main() and other functions needed to get contributor information from the organization or repository"""

from typing import List

import github3.repos
import github3.users
import github3

from . import auth, contributor_stats, env, json_writer, markdown


def main():
    """Run the main program"""

    # Get environment variables
    environment = env.get_env_vars()

    # Auth to GitHub.com
    github_connection: github3.GitHub = auth.auth_to_github(
        environment.gh_app_id,
        environment.gh_app_installation_id,
        environment.gh_app_private_key_bytes,
        environment.token,
        environment.ghe,
    )

    # Get the contributors
    contributors = get_all_contributors(
        environment.organization,
        environment.repositories_list,
        environment.start_date,
        environment.end_date,
        github_connection,
    )

    # Check for new contributor if user provided start_date and end_date
    if environment.start_date and environment.end_date:
        # get the list of contributors from before start_date
        # so we can see if contributors after start_date are new or returning
        returning_contributors = get_all_contributors(
            environment.organization,
            environment.repositories_list,
            start_date="2008-02-29",  # GitHub was founded on 2008-02-29
            end_date=environment.start_date,
            github_connection=github_connection,
        )
        for contributor in contributors:
            contributor.new_contributor = contributor_stats.is_new_contributor(
                contributor.username, returning_contributors
            )

    # Get sponsor information on the contributor
    if environment.sponsor_info == "true":
        contributors = contributor_stats.get_sponsor_information(contributors, environment.token)
    # Output the contributors information
    markdown.write_to_markdown(
        contributors,
        f"{environment.filename}.md",
        environment.start_date,
        environment.end_date,
        environment.organization,
        environment.repositories_list,
        environment.sponsor_info,
        environment.link_to_profile,
        environment.show_organisations_list,
    )
    #TODO HCookie Fix to json
    json_writer.write_to_json(
        filename="{environment.filename}.json",
        start_date=environment.start_date,
        end_date=environment.end_date,
        organization=environment.organization,
        repository_list=environment.repositories_list,
        sponsor_info=environment.sponsor_info,
        link_to_profile=environment.link_to_profile,
        contributors=contributors,
    )


def get_all_contributors(
    organization: str,
    repository_list: List[str],
    start_date: str,
    end_date: str,
    github_connection: github3.GitHub,
):
    """
    Get all contributors from the organization or repository

    Args:
        organization (str): The organization for which the contributors are being listed.
        repository_list (List[str]): The repository list for which the contributors are being listed.
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.
        github_connection (object): The authenticated GitHub connection object from PyGithub

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
            repo_contributors = get_contributors(repo, start_date, end_date)
            if repo_contributors:
                all_contributors.append(repo_contributors)

    # Check for duplicates and merge when usernames are equal
    all_contributors = contributor_stats.merge_contributors(all_contributors)

    return all_contributors


def get_contributors(
    repo: github3.repos.Repository,
    start_date: str,
    end_date: str,
) -> list[contributor_stats.ContributorStats]:
    """
    Get contributors from a single repository and filter by start end dates if present.

    Args:
        repo (object): The repository object from PyGithub
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.

    Returns:
        contributors (list): A list of ContributorStats objects
    """
    all_repo_contributors = repo.contributors()
    contributors = []
    try:
        for user in all_repo_contributors:
            # Ignore contributors with [bot] in their name
            if "[bot]" in user.login:
                continue

            # Check if user has commits in the date range
            if start_date and end_date:
                user_commits = repo.commits(author=user.login, since=start_date, until=end_date)

                # If the user has no commits in the date range, skip them
                try:
                    next(user_commits)
                except StopIteration:
                    continue

            # Store the contributor information in a ContributorStats object
            if start_date and end_date:
                commit_url = f"https://github.com/{repo.full_name}/commits?author={user.login}&since={start_date}&until={end_date}"
            else:
                commit_url = f"https://github.com/{repo.full_name}/commits?author={user.login}"
            contributor = contributor_stats.ContributorStats(
                username=user.login,
                new_contributor=False,
                avatar_url=user.avatar_url,
                contribution_count=user.contributions_count,
                commit_url=commit_url,
                sponsor_info="",
                organisations=list(map(lambda x: x.url.split("/")[-1], user.organizations())),
            )
            contributors.append(contributor)
    except Exception as e:
        print("Error getting contributors for repository: " + repo.full_name)
        print(e)
        return None

    return contributors
