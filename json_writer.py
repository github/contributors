"""This module contains a function that writes data to a JSON file."""

import json


def write_to_json(
    contributors,
    filename,
    start_date,
    end_date,
    organization,
    repository_list,
    sponsor_info,
    link_to_profile,
):
    """Write data to a JSON file.

    Args:
        contributors (list): A list of Contributor objects.
        filename (str): The name of the JSON file.
        start_date (str): The start date of the date range for the contributor list.
        end_date (str): The end date of the date range for the contributor list.
        organization (str): The organization for which the contributors are being listed.
        repository_list (list): A list of repositories for which the contributors are being listed.
        sponsor_info (str): A string indicating whether sponsor information should be included.
        link_to_profile (str): A string indicating whether a link to the contributor's profile should be included.

    Returns:
        None
    """

    # Prepare data for JSON such that it looks like the markdown data. ie.
    # {
    #     "start_date": "2024-03-08",
    #     "end_date": "2024-03-15",
    #     "organization": null,
    #     "repository_list": [
    #         "github/stale-repos",
    #         "github/issue-metrics",
    #         "github/contributors",
    #         "github/automatic-contrib-prs",
    #         "github/evergreen",
    #         "github/cleanowners"
    #     ],
    #     "sponsor_info": false,
    #     "link_to_profile": false,
    #     "contributors": [
    #         {
    #             "username": "zkoppert",
    #             "new_contributor": false,
    #             "avatar_url": "https://avatars.githubusercontent.com/u/6935431?v=4",
    #             "contribution_count": 785,
    #             "commit_url": "https://github.com/github/stale-repos/commits?author=zkoppert&since=2024-03-08&until=2024-03-15,
    #             "sponsor_info": ""
    #         },
    #         {
    #             "username": "jmeridth",
    #             "new_contributor": false,
    #             "avatar_url": "https://avatars.githubusercontent.com/u/35014?v=4",
    #             "contribution_count": 94,
    #             "commit_url": "https://github.com/github/stale-repos/commits?author=jmeridth&since=2024-03-08&until=2024-03-15,
    #             "sponsor_info": ""
    #         }
    #     ]
    # }
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "organization": organization,
        "repository_list": repository_list,
        "sponsor_info": sponsor_info,
        "link_to_profile": link_to_profile,
        "contributors": [contributor.__dict__ for contributor in contributors],
    }

    # Write data to a JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
