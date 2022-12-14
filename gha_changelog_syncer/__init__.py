import datetime
import logging
import os
import sys
import typing

import daiquiri
import httpx

daiquiri.setup(level=logging.INFO, outputs=[daiquiri.output.Stream(sys.stdout)])
LOGGER = daiquiri.getLogger(__name__)


def run(title: str, description: str, merged_at: datetime.datetime) -> None:
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
        merged_at=merged_at.date(),
        description=description,
    )


def add_database_entry(
    client: httpx.Client,
    notion_database_id: str | None,
    title: str,
    merged_at: datetime.date,
    description: str,
) -> None:
    LOGGER.info(
        "Add changelog entry",
        title=title,
        merged_at=merged_at.isoformat(),
        description=description,
    )

    properties = {
        "Date": {
            "date": {"start": merged_at.isoformat()},
        },
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
        LOGGER.error(e.response.json()["message"])
        raise
    else:
        LOGGER.info("Changelog entry added")


def text_block(content: str) -> dict[str, typing.Any]:
    return {"text": {"content": content}}
