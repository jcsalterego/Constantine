#!/usr/bin/env python3

import json
import os
import sys

import requests

MAX_GET_AUTHOR_FEED_LIMIT = 100

BLESSED_HELLTHREAD = (
    "at://did:plc:wgaezxqi2spqm3mhrb5xvkzi/app.bsky.feed.post/3juzlwllznd24"
)


def usage():
    print("Usage: get-hellthreads.py <handle>", file=sys.stderr)
    sys.exit(1)


def create_session(app_user, app_token):
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    response = requests.post(url, json={"identifier": app_user, "password": app_token})
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_xrpc(session, endpoint, params={}):
    response = requests.get(
        f"https://bsky.social/xrpc/{endpoint}",
        params=params,
        headers={"Authorization": f"Bearer {session['accessJwt']}"},
    )
    return response.json()


def xrpc_app_bsky_feed_get_author_feed(
    session, actor, cursor=None, limit=MAX_GET_AUTHOR_FEED_LIMIT
):
    return get_xrpc(
        session,
        "app.bsky.feed.getAuthorFeed",
        params={
            "actor": actor,
            "limit": limit,
            "cursor": cursor,
        },
    )


def to_web_url(uri):
    web_url = uri.replace("at://", "https://bsky.app/profile/")
    web_url = web_url.replace("/app.bsky.feed.post/", "/post/")
    return web_url


def fetch_all_posts(session, actor):
    all_feed = []
    cursor = None
    while True:
        doc = xrpc_app_bsky_feed_get_author_feed(
            session, actor, cursor=cursor, limit=MAX_GET_AUTHOR_FEED_LIMIT
        )
        all_feed += doc["feed"]
        if "cursor" not in doc:
            break
        else:
            # set next cursor
            cursor = doc["cursor"]
            print(f"cursor = {cursor}", file=sys.stderr)
    return all_feed


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


def get_node(doc, path):
    path_words = path.split(".")
    node = doc
    for word in path_words:
        if word not in node:
            return None
        node = node[word]
    return node


if __name__ == "__main__":
    main(sys.argv)
