# Contributors action

This is a GitHub Action that given an organization or repository, produces information about the contributors over the specified time period.

Similar actions to help you recognize contributors include:
- [contributor-list](https://github.com/marketplace/actions/contribute-list)

This action was developed by the GitHub OSPO for our own use and developed in a way that we could open source it that it might be useful to you as well! If you want to know more about how we use it, reach out in an issue in this repository.

## Example use cases

- As a maintainer, you may want to ackowledge recent contributors in a discussion post
- As an OSPO or maintainer, you may want to know who candidates are for new maintainers

## Support

If you need support using this project or have questions about it, please [open up an issue in this repository](https://github.com/github/contributors/issues). Requests made directly to GitHub staff or support team will be redirected here to open an issue. GitHub SLA's and support/services contracts do not apply to this repository.

## Use as a GitHub Action

1. Create a repository to host this GitHub Action or select an existing repository.
1. Select a best fit workflow file from the [examples below](#example-workflows).
1. Copy that example into your repository (from step 1) and into the proper directory for GitHub Actions: `.github/workflows/` directory with the file extension `.yml` (ie. `.github/workflows/contributors.yml`)
1. Edit the values (`ORGANIZATION`, `REPOSITORY`, `START_DATE`, `END_DATE`) from the sample workflow with your information.
1. If you are running this action on an organization or repository other than the one where the workflow file is going to be, then update the value of `GH_TOKEN`. Do this by creating a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) with permissions to read the repository/organization and write issues. Then take the value of the API token you just created, and [create a repository secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets) where the name of the secret is `GH_TOKEN` and the value of the secret the API token. Then finally update the workflow file to use that repository secret by changing `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to `GH_TOKEN: ${{ secrets.GH_TOKEN }}`. The name of the secret can really be anything. It just needs to match between when you create the secret name and when you refer to it in the workflow file.
1. If you want the resulting issue with the output to appear in a different repository other than the one the workflow file runs in, update the line `token: ${{ secrets.GITHUB_TOKEN }}` with your own GitHub API token stored as a repository secret. This process is the same as described in the step above. More info on creating secrets can be found [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets).
1. Commit the workflow file to the default branch (often `master` or `main`)
1. Wait for the action to trigger based on the `schedule` entry or manually trigger the workflow as shown in the [documentation](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow).

### Configuration

Below are the allowed configuration options:

| field                 | required | default | description |
|-----------------------|----------|---------|-------------|
| `GH_TOKEN`            | True     |         | The GitHub Token used to scan the repository or organization. Must have read access to all repository you are interested in scanning. |
| `ORGANIZATION`        | Required to have `ORGANIZATION` or `REPOSITORY` |         | The name of the GitHub organization which you want the contributor information of all repos from. ie. github.com/github would be `github` |
| `REPOSITORY`          | Required to have `ORGANIZATION` or `REPOSITORY` |         | The name of the repository and organization which you want the contributor information from. ie. `github/contributors` |
| `START_DATE`                | False |   All time      | The date from which you want to start gathering contributor information. ie. Aug 1st, 2023 would be `2023-08-01` |
| `END_DATE`                | False |   All time      | The date at which you want to stop gathering contributor information. Must be later than the `START_DATE`. ie. Aug 2nd, 2023 would be `2023-08-02` |


### Example workflows

TO BE WRITTEN

## Local usage without Docker

1. Make sure you have at least Python3.11 installed
1. Copy `.env-example` to `.env`
1. Fill out the `.env` file with a _token_ from a user that has access to the organization to scan (listed below). Tokens should have admin:org or read:org access.
1. Fill out the `.env` file with the configuration parameters you want to use
1. `pip3 install -r requirements.txt`
1. Run `python3 ./contributors.py`, which will output everything in the terminal

## License

[MIT](LICENSE)
