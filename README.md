# changelog-syncer

GitHub Action to synchronize the description of a pull request to a Notion Database.

## Usage

Example of a workflow sending details of [merged pull requests](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#running-your-workflow-when-a-pull-request-merges-1) to a Notion Database.

```yaml
name: Changelog sync

on:
  pull_request_target:
    branches: ["main"]
    types:
      - closed

permissions: read-all

jobs:
  if_merged:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Synchronize changelog
        uses: DouglasBlackwood/gha-changelog-syncer@main
        with:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
```

## Run locally

Clone the repository and install Python dependecies.

```
poetry install
```

Create a `.env` file by copying `.env.example` file and completing empty variables. Then run the program.

```
poetry run dotenv run -- python gha_changelog_syncer/__init__.py
```
