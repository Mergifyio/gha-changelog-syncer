import datetime
import os

import dateutil.parser

import gha_changelog_syncer


def handle():
    title = os.getenv("PR_TITLE")
    description = os.environ.get("PR_DESCRIPTION", "")
    merged_at_str = os.environ.get(
        "PR_MERGED_AT", datetime.datetime.utcnow().isoformat()
    )
    merged_at = dateutil.parser.isoparse(merged_at_str)

    gha_changelog_syncer.run(title, description, merged_at)
