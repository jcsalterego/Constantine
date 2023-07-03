#!/usr/bin/env python3

import argparse
import os
import sys
from datetime import datetime, timezone

from constantine import (
    create_session,
    fetch_all_hellthread_posts,
    post_xrpc,
    require_bluesky_creds_from_env,
    to_web_url,
)

APP_BSKY_FEED_POST_COLLECTION = "app.bsky.feed.post"


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
    parser.add_argument(
        "--max-posts",
        action="store",
        dest="max_delete_posts",
        type=int,
        help="Maximum number of posts to delete",
        default=os.getenv("MAX_DELETE_POSTS", 100),
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


def delete_post(session, uri):
    words = uri.replace("at://", "").split("/")
    if len(words) == 3 and words[1] == APP_BSKY_FEED_POST_COLLECTION:
        did = words[0]
        rkey = words[2]
        json_payload = {
            "collection": APP_BSKY_FEED_POST_COLLECTION,
            "repo": did,
            "rkey": rkey,
        }
        return post_xrpc(
            session, "com.atproto.repo.deleteRecord", json_payload=json_payload
        )
    return None


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
    total_deleted = 0
    failure = False
    for uri in hellthread_reply_uris:
        if total_deleted >= args.max_delete_posts:
            print(
                f"Reached max-posts={args.max_delete_posts} posts",
                file=sys.stderr,
            )
            break

        print(f"Deleting {to_web_url(uri)}", file=sys.stderr)
        delete_post(session, uri)
        total_deleted += 1

    print(f"Deleted {total_deleted} posts", file=sys.stderr)
    if failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
