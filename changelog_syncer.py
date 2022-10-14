import datetime
import typing
import os

import httpx


def main() -> None:
    notion_api_timeout = httpx.Timeout(
        float(os.environ.get("NOTION_API_TIMEOUT", 10.0))
    )
    notion_api_key = os.environ.get("NOTION_API_KEY", "")
    notion_database_id = os.environ.get("NOTION_DATABASE_ID", "")
    notion_api_version = os.environ.get("NOTION_API_VERSION", "")

    client = httpx.Client(
        base_url="https://api.notion.com",
        timeout=notion_api_timeout,
        headers={
            "Accept": "application/json",
            "Notion-Version": notion_api_version,
            "Authorization": f"Bearer {notion_api_key}",
        },
    )
    add_changelog_entry(
        client,
        notion_database_id=notion_database_id,
        title="General Kenobi",
        merged_at=datetime.date.today(),
        description="Hello there!",
    )


def add_changelog_entry(
    client: httpx.Client,
    notion_database_id: str | None,
    title: str,
    merged_at: datetime.date,
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
            "icon": {"emoji": "🤖"},
            "properties": properties,
            "children": children,
        },
    )

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(e.response.json()["message"])


def text_block(content: str) -> dict[str, typing.Any]:
    return {"text": {"content": content}}


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    main()
