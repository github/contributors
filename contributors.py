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

    # Check for new contributor if user provided start_date and end_date
    if start_date and end_date:
        # get the list of contributors from before start_date
        # so we can see if contributors after start_date are new or returning
        returning_contributors = get_all_contributors(
            organization,
            repository,
            start_date="2008-02-29",  # GitHub was founded on 2008-02-29
            end_date=start_date,
            github_connection=github_connection,
        )
        for contributor in contributors:
            contributor.new_contributor = contributor_stats.is_new_contributor(
                contributor.username, returning_contributors
            )

    # Output the contributors information
    # print(contributors)
    markdown.write_to_markdown(
        contributors, "contributors.md", start_date, end_date, organization, repository
    )
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

    # Check for duplicates and merge when usernames are equal
    all_contributors = contributor_stats.merge_contributors(all_contributors)

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
        if start_date and end_date:
            commit_url = f"https://github.com/{repo.full_name}/commits?author={user.login}&since={start_date}&until={end_date}"
        else:
            commit_url = (
                f"https://github.com/{repo.full_name}/commits?author={user.login}"
            )
        contributor = contributor_stats.ContributorStats(
            user.login,
            False,
            user.avatar_url,
            user.contributions_count,
            commit_url,
        )
        contributors.append(contributor)

    return contributors


if __name__ == "__main__":
    main()
