#!/usr/bin/env python3
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


def get_node(doc, path):
    path_words = path.split(".")
    node = doc
    for word in path_words:
        if word not in node:
            return None
        node = node[word]
    return node


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


def require_bluesky_creds_from_env():
    bluesky_user = os.getenv("BLUESKY_USER")
    bluesky_app_password = os.getenv("BLUESKY_APP_PASSWORD")
    if not bluesky_user or not bluesky_app_password:
        print("BLUESKY_USER and BLUESKY_APP_PASSWORD have to be set", file=sys.stderr)
        sys.exit(1)
    return bluesky_user, bluesky_app_password
