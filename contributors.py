"""This file contains the main() and other functions needed to get contributor information from the organization or repository"""

import env
import auth
import contributor_stats
import markdown


def main():
    """Run the main program"""

    # Get environment variables
    organization, repository, token, start_date, end_date = env.get_env_vars()

    # Auth to GitHub.com
    github_connection = auth.auth_to_github(token)

    # Get the contributors
    contributors = get_all_contributors(
        organization,
        repository,
        start_date,
        end_date,
        github_connection,
    )

    # Output the contributors information
    print(contributors)
    markdown.write_to_markdown(contributors, "contributors.md")
    # write_to_json(contributors)


def get_all_contributors(
    organization: str,
    repository: str,
    start_date: str,
    end_date: str,
    github_connection: object,
):
    """Get all contributors from the organization or repository"""
    repos = []
    if organization:
        repos = github_connection.organization(organization).repositories()
    else:
        owner, repo = repository.split("/")
        repository_obj = github_connection.repository(owner, repo)

    all_contributors = []
    if repos:
        for repo in repos:
            all_contributors.append(get_contributors(repo, start_date, end_date))
    else:
        all_contributors.append(get_contributors(repository_obj, start_date, end_date))

    return all_contributors


def get_contributors(
    repo: object,
    start_date: str,
    end_date: str,
):
    """Get contributors from a single repository and filter by start end dates"""
    all_repo_contributors = repo.contributors()
    contributors = []
    for user in all_repo_contributors:
        # Ignore contributors with [bot] in their name
        if "[bot]" in user.login:
            continue

        # Store the contributor information in a ContributorStats object
        if start_date and end_date:
            commit_url = f"https://github.com/{repo.full_name}/commits?author={user.login}&since={start_date}&until={end_date}"
        else:
            commit_url = (
                f"https://github.com/{repo.full_name}/commits?author={user.login}"
            )
        contributor = contributor_stats.ContributorStats(
            user.login,
            user.avatar_url,
            user.contributions_count,
            commit_url,
        )
        contributors.append(contributor)

    return contributors


if __name__ == "__main__":
    main()
