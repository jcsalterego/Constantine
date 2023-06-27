#!/usr/bin/env python3

import sys
import argparse

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
        "handle",
        type=str,
        help="Handle of the user whose hellthreads to fetch",
    )
    args = parser.parse_args()
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
        session, handle
    )

    print(f"{len(hellthread_reply_uris)} hellthread posts total", file=sys.stderr)
    for uri in hellthread_reply_uris:
        print(to_web_url(uri))


if __name__ == "__main__":
    main(sys.argv)
