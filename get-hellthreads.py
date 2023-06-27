#!/usr/bin/env python3

import sys

from constantine import (
    create_session,
    to_web_url,
    require_bluesky_creds_from_env,
    fetch_all_hellthread_posts,
)


def usage():
    print("Usage: get-hellthreads.py <handle>", file=sys.stderr)
    sys.exit(1)


def main(argv):
    if len(argv) < 2:
        usage()
    actor = argv[1]

    bluesky_user, bluesky_app_password = require_bluesky_creds_from_env()
    session = create_session(bluesky_user, bluesky_app_password)
    if session is None:
        print(
            "Login failed. Please check BLUESKY_USER and BLUESKY_APP_PASSWORD",
            file=sys.stderr,
        )
        sys.exit(1)

    hellthread_reply_uris = fetch_all_hellthread_posts(session, actor)

    print(f"{len(hellthread_reply_uris)} hellthread posts total", file=sys.stderr)
    for uri in hellthread_reply_uris:
        print(to_web_url(uri))


if __name__ == "__main__":
    main(sys.argv)
