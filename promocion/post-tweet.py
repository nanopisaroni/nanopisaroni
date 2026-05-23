#!/usr/bin/env python3.12
"""
Postea tweets desde master-schedule.json.
Solo POSTS. Cero reads. Cero verificaciones. Cero searches.
Uso: python3 post-tweet.py morning|noon|evening
"""
import json
import os
import sys
import time
import base64
import requests
from datetime import datetime, timezone, timedelta

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "posts/master-schedule.json")
CREDS_FILE = os.path.expanduser("~/.panteon_twitter.json")
TOKEN_URL = "https://api.x.com/2/oauth2/token"
API_BASE = "https://api.x.com/2"


def load_creds():
    with open(CREDS_FILE) as f:
        return json.load(f)


def save_creds(creds):
    with open(CREDS_FILE, "w") as f:
        json.dump(creds, f, indent=2)


def get_token(creds):
    """Get a valid access token. Solo refresh si expiró. Cero verificación extra."""
    if creds.get("token_expires_at") and time.time() < creds["token_expires_at"] - 60:
        return creds["access_token"]
    auth = base64.b64encode(f"{creds['client_id']}:{creds['client_secret']}".encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        data={"grant_type": "refresh_token", "refresh_token": creds["refresh_token"], "client_id": creds["client_id"]},
        headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {auth}"},
        timeout=15,
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    creds["access_token"] = data["access_token"]
    if "refresh_token" in data:
        creds["refresh_token"] = data["refresh_token"]
    creds["token_expires_at"] = time.time() + data.get("expires_in", 7200)
    save_creds(creds)
    return creds["access_token"]


def post_tweet(text, creds):
    """UN SOLO POST. Cero reads. Cero verificaciones."""
    token = get_token(creds)
    if not token:
        return False, "Token inválido"

    resp = requests.post(
        f"{API_BASE}/tweets",
        headers={"Authorization": f"Bearer {token}"},
        json={"text": text},
        timeout=15,
    )

    if resp.status_code == 201:
        return True, resp.json()["data"]["id"]
    # Solo un retry ante 401 (token expirado)
    elif resp.status_code == 401:
        token = get_token(creds)
        if token:
            resp = requests.post(
                f"{API_BASE}/tweets",
                headers={"Authorization": f"Bearer {token}"},
                json={"text": text},
                timeout=15,
            )
            if resp.status_code == 201:
                return True, resp.json()["data"]["id"]
        return False, f"Auth: {resp.text[:200]}"
    else:
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"


def get_now_arg():
    return datetime.now(timezone.utc) + timedelta(hours=-3)


def get_slot():
    if len(sys.argv) < 2:
        print("❌ Uso: python3 post-tweet.py morning|noon|evening")
        sys.exit(1)
    slot = sys.argv[1].lower()
    if slot not in ("morning", "noon", "evening"):
        print(f"❌ Slot invalido: {slot}")
        sys.exit(1)
    return slot


def find_post(schedule, today_str, slot):
    for post in schedule:
        if post["date"] == today_str and post["slot"] == slot and not post.get("posted", False):
            return post
    return None


def main():
    slot = get_slot()

    if not os.path.exists(SCHEDULE_FILE):
        print(f"❌ Schedule not found: {SCHEDULE_FILE}")
        sys.exit(1)

    with open(SCHEDULE_FILE) as f:
        data = json.load(f)

    now = get_now_arg()
    today = now.strftime("%Y-%m-%d")
    schedule = data["schedule"]
    post = find_post(schedule, today, slot)

    if not post:
        print(f"📭 No pending post for {today} ({slot}).")
        sys.exit(0)

    print(f"📝 [{post.get('emoji','')} {post['name']}] {post['content'][:80]}...")

    creds = load_creds()
    success, result = post_tweet(post["content"], creds)

    if success:
        post["posted"] = True
        post["tweet_id"] = result
        post["posted_at"] = now.isoformat()
        data["schedule"] = schedule
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Tuit posteado! ID: {result}")
    else:
        print(f"❌ {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
