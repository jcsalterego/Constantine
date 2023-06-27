#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timezone

from constantine import (
    create_session,
    to_web_url,
    require_bluesky_creds_from_env,
    fetch_all_hellthread_posts,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--before-date",
        type=str,
        help="Only fetch posts before this date (exclusive),"
        " in the local time zone (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--after-date",
        type=str,
        help="Only fetch posts on or after this date (inclusive),"
        " in the local time zone (YYYY-MM-DD)",
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
            args.before_date = parse_local_date(args.before_date)
        except ValueError:
            print(
                f"Invalid date `{args.before_date}`. Must be YYYY-MM-DD",
                file=sys.stderr,
            )
            sys.exit(1)

    if args.after_date is not None:
        # parse YYYY-MM-DD into datetime
        try:
            args.after_date = parse_local_date(args.after_date)
        except ValueError:
            print(
                f"Invalid date `{args.after_date}`. Must be YYYY-MM-DD",
                file=sys.stderr,
            )
            sys.exit(1)

    if (
        args.before_date is not None
        and args.after_date is not None
        and args.before_date <= args.after_date
    ):
        print(
            f"Invalid date range:\n"
            f"  --after-date:  {args.after_date}\n"
            f"  --before-date: {args.before_date}",
            file=sys.stderr,
        )
        sys.exit(1)

    return args


def parse_local_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    tzlocal = datetime.now(timezone.utc).astimezone().tzinfo
    date = date.replace(tzinfo=tzlocal)
    return date


def main():
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
        session, handle, before_date=args.before_date, after_date=args.after_date
    )

    print(f"{len(hellthread_reply_uris)} hellthread posts total", file=sys.stderr)
    for uri in hellthread_reply_uris:
        print(to_web_url(uri))


if __name__ == "__main__":
    main()
