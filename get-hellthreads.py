#!/usr/bin/env python3

import json
import os
import sys

from constantine import (
    create_session,
    fetch_all_posts,
    to_web_url,
    get_node,
    BLESSED_HELLTHREAD,
)


def usage():
    print("Usage: get-hellthreads.py <handle>", file=sys.stderr)
    sys.exit(1)


def main(argv):
    if len(argv) < 2:
        usage()
    actor = argv[1]

    bluesky_user = os.getenv("BLUESKY_USER")
    bluesky_app_password = os.getenv("BLUESKY_APP_PASSWORD")
    if not bluesky_user or not bluesky_app_password:
        print("BLUESKY_USER and BLUESKY_APP_PASSWORD have to be set", file=sys.stderr)
        sys.exit(1)

    # login
    session = create_session(bluesky_user, bluesky_app_password)
    if session is None:
        print(
            "Login failed. Please check BLUE_SKY_USER and BLUE_SKY_APP_PASSWORD",
            file=sys.stderr,
        )
        sys.exit(1)

    all_posts = fetch_all_posts(session, actor)
    print(f"{len(all_posts)} posts total", file=sys.stderr)

    hellthread_reply_uris = []
    for feed_item in all_posts:
        if BLESSED_HELLTHREAD in json.dumps(feed_item):
            if "reason" in feed_item:
                # skip reposts
                continue

            post_record_reply_root_uri = get_node(
                feed_item, "post.record.reply.root.uri"
            )
            if (
                post_record_reply_root_uri is not None
                and post_record_reply_root_uri == BLESSED_HELLTHREAD
            ):
                hellthread_reply_uris.append(feed_item["post"]["uri"])

    print(f"{len(hellthread_reply_uris)} hellthread posts total", file=sys.stderr)
    for uri in hellthread_reply_uris:
        print(to_web_url(uri))


if __name__ == "__main__":
    main(sys.argv)
