import argparse
import datetime

import daiquiri
import dateutil.parser
import dotenv

import gha_changelog_syncer


def handle():
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(
        description="Send a pull request description to a Notion Database."
    )
    parser.add_argument("--title", help="Pull request title")
    parser.add_argument("--description", help="Pull request description", default="")
    parser.add_argument(
        "--merged_at",
        help="Pull request merge date (e.g. 2011-01-26)",
        type=dateutil.parser.isoparse,
        default=datetime.datetime.utcnow(),
    )

    args = parser.parse_args()

    logger = daiquiri.getLogger(__name__)
    logger.info("Arguments parsed", arguments=args)

    gha_changelog_syncer.run(args.title, args.description, args.merged_at)
