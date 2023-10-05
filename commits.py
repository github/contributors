"""This module contains functions that retrieve commit information on a repository"""
import github3


def get_commits(
    author: str, repo: object, github_connection: object, start_date: str, end_date: str
) -> github3.search.commit.CommitSearchResult:
    """Get commit information for a single author from the repository"""
    search_dates = ""
    if start_date and end_date:
        search_dates = f" committer-date:{start_date}..{end_date}"

    commits = github_connection.search_commits(
        f"repo:{repo.full_name} author:{author} merge:false {search_dates}"
    )
    return commits
