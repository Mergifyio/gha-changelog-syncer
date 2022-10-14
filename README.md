# changelog-syncer

GitHub Action to synchronize the description of a pull request to a Notion Database.

## Installation

First, create a `.env` file by copying `.env.example` file and completing empty variables.
Then install Python dependencies.

```
poetry install
```

## Run

```
poetry run python changelog_syncer.py
```

## Delivery

If there are new Python dependencies, export and commit `requirement.txt` file with Poetry.

```
poetry export -f requirements.txt --output requirements.txt
git add requirements.txt
git commit -m "New Python dependencies"
```

Push to the GitHub repository to deliver.
