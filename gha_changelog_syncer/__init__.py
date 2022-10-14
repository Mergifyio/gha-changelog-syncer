import argparse
import datetime
import os
import typing

import dateutil.parser
import httpx


def main(title: str, description: str, merged_at: datetime.datetime) -> None:
    notion_api_timeout = httpx.Timeout(
        float(os.environ.get("NOTION_API_TIMEOUT", 10.0))
    )
    notion_api_key = os.environ.get("NOTION_API_KEY", "")
    notion_database_id = os.environ.get("NOTION_DATABASE_ID", "")
    notion_api_version = os.environ.get("NOTION_API_VERSION", "2022-06-28")

    client = httpx.Client(
        base_url="https://api.notion.com",
        timeout=notion_api_timeout,
        headers={
            "Accept": "application/json",
            "Notion-Version": notion_api_version,
            "Authorization": f"Bearer {notion_api_key}",
        },
    )
    add_database_entry(
        client,
        notion_database_id=notion_database_id,
        title=title,
        merged_at=merged_at,
        description=description,
    )


def add_database_entry(
    client: httpx.Client,
    notion_database_id: str | None,
    title: str,
    merged_at: datetime.datetime,
    description: str,
) -> None:
    properties = {
        "Date": {
            "date": {"start": merged_at.isoformat()},
        },
        # "Categories": {
        #     "multi_select": [{"name": "Actions"}, {"name": "Merge Queue"}],
        # },
        "Name": {
            "title": [text_block(title)],
        },
    }
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [text_block(description)]},
        }
    ]
    response = client.post(
        "/v1/pages",
        json={
            "parent": {
                "type": "database_id",
                "database_id": notion_database_id,
            },
            "icon": {"emoji": "🟠"},
            "properties": properties,
            "children": children,
        },
    )

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(e.response.json()["message"])
        raise


def text_block(content: str) -> dict[str, typing.Any]:
    return {"text": {"content": content}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send a pull request description to a Notion Database."
    )
    parser.add_argument(
        "--title",
        help="Pull request title",
        default=os.getenv("PR_TITLE"),
    )
    parser.add_argument(
        "--description",
        help="Pull request description",
        default=os.environ.get("PR_DESCRIPTION", ""),
    )
    parser.add_argument(
        "--merged_at",
        help="Pull request merge date (e.g. 2011-01-26T19:01:12Z)",
        default=os.environ.get("PR_MERGED_AT", datetime.datetime.utcnow().isoformat()),
    )

    args = parser.parse_args()
    merged_at = dateutil.parser.isoparse(args.merged_at)

    main(args.title, args.description, merged_at)
