#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime, timezone

from constantine import (
    create_session,
    to_web_url,
    require_bluesky_creds_from_env,
    fetch_all_hellthread_posts,
)


def usage(parser):
    print(parser.usage, file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--before-date",
        type=str,
        help="Only fetch posts before this date, in the local time zone (YYYY-MM-DD)",
    )
    parser.add_argument(
        "handle",
        type=str,
        help="Handle of the user whose hellthreads to fetch",
    )
    args = parser.parse_args()

    if args.before_date is not None:
        # parse YYYY-MM-DD into datetime
        try:
            args.before_date = datetime.strptime(args.before_date, "%Y-%m-%d")
            tzlocal = datetime.now(timezone.utc).astimezone().tzinfo
            args.before_date = args.before_date.replace(tzinfo=tzlocal)
        except ValueError:
            print(
                f"Invalid date `{args.before_date}`. Must be YYYY-MM-DD",
                file=sys.stderr,
            )
            usage(parser)
    return args


def main(argv):
    args = parse_args()
    handle = args.handle

    bluesky_user, bluesky_app_password = require_bluesky_creds_from_env()
    session = create_session(bluesky_user, bluesky_app_password)
    if session is None:
        print(
            "Login failed. Please check BLUESKY_USER and BLUESKY_APP_PASSWORD",
            file=sys.stderr,
        )
        sys.exit(1)

    hellthread_reply_uris = fetch_all_hellthread_posts(
        session, handle, before_date=args.before_date
    )

    print(f"{len(hellthread_reply_uris)} hellthread posts total", file=sys.stderr)
    for uri in hellthread_reply_uris:
        print(to_web_url(uri))


if __name__ == "__main__":
    main(sys.argv)
