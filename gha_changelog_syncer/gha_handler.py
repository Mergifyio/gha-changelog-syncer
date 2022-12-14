import datetime
import os

import daiquiri
import dateutil.parser

import gha_changelog_syncer


def handle():
    title = os.getenv("PR_TITLE")
    description = os.environ.get("PR_DESCRIPTION", "")
    merged_at_str = os.environ.get(
        "PR_MERGED_AT", datetime.datetime.utcnow().isoformat()
    )
    merged_at = dateutil.parser.isoparse(merged_at_str)

    logger = daiquiri.getLogger(__name__)
    logger.info(
        "Arguments parsed", title=title, description=description, merged_at=merged_at
    )

    gha_changelog_syncer.run(title, description, merged_at)
