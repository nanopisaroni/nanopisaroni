#!/usr/bin/env python3.12
"""
Postea tweets desde master-schedule.json usando OAuth 2.0 con auto-refresh.
Soporta imágenes por capítulo (episode artwork).
Uso: python3 post-tweet.py morning|noon|evening
"""
import json
import os
import sys
import time
import base64
import mimetypes
import requests
from datetime import datetime, timezone, timedelta

# Config
SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "posts/master-schedule.json")
CREDS_FILE = os.path.expanduser("~/.panteon_twitter.json")
IMAGES_DIR = os.path.expanduser("~/sitio/audiolibro/images")
ARG_TIMEZONE = -3  # Argentina UTC-3

# X API OAuth 2.0
TOKEN_URL = "https://api.x.com/2/oauth2/token"
API_BASE = "https://api.x.com/2"

# Image mapping: persona_id -> image filename
IMAGE_MAP = {
    "borges": "ep01_borges.jpg",
    "feynman": "ep02_feynman.jpg",
    "taleb": "ep03_taleb.jpg",
    "deutsch": "ep04_deutsch.jpg",
    "thiel": "ep05_thiel.jpg",
    "popper": "ep06_popper.jpg",
    "munger": "ep07_munger.jpg",
    "kahneman": "ep08_kahneman.jpg",
    "graham": "ep09_graham.jpg",
    "yudkowsky": "ep10_yudkowsky.jpg",
    "marco aurelio": "ep11_marco_aurelio.jpg",
    "epicteto": "ep12_epicteto_seneca.jpg",
    "watts": "ep13_watts.jpg",
    "krishnamurti": "ep14_krishnamurti.jpg",
    "cabral": "ep15_cabral.jpg",
    "naval": "ep16_naval.jpg",
}


def load_creds():
    with open(CREDS_FILE) as f:
        return json.load(f)


def save_creds(creds):
    with open(CREDS_FILE, "w") as f:
        json.dump(creds, f, indent=2)


def refresh_access_token(creds):
    """Refresh the access token using the refresh token."""
    auth = base64.b64encode(f"{creds['client_id']}:{creds['client_secret']}".encode()).decode()
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": creds["refresh_token"],
            "client_id": creds["client_id"],
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth}",
        },
    )
    if resp.status_code != 200:
        print(f"❌ Refresh failed: {resp.status_code} {resp.text[:200]}")
        return None

    data = resp.json()
    creds["access_token"] = data["access_token"]
    if "refresh_token" in data:
        creds["refresh_token"] = data["refresh_token"]
    creds["token_expires_at"] = time.time() + data.get("expires_in", 7200)
    save_creds(creds)
    print(f"🔄 Token refreshed (expires in {data.get('expires_in', 7200)}s)")
    return creds["access_token"]


def get_valid_token(creds):
    """Get a valid access token, refreshing if needed."""
    if creds.get("token_expires_at") and time.time() < creds["token_expires_at"] - 60:
        return creds["access_token"]
    return refresh_access_token(creds)


def media_upload(image_path, creds):
    """Upload media to X using v1.1 API (INIT/APPEND/FINALIZE). Returns media_id_string or None."""
    token = get_valid_token(creds)
    if not token:
        return None

    total_bytes = os.path.getsize(image_path)
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"

    headers = {"Authorization": f"Bearer {token}"}

    # INIT
    init_resp = requests.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        headers=headers,
        data={
            "command": "INIT",
            "media_type": mime_type,
            "total_bytes": total_bytes,
        }
    )
    if init_resp.status_code != 202:
        print(f"⚠️ Media INIT failed: {init_resp.status_code} {init_resp.text[:200]}")
        return None
    media_id = init_resp.json()["media_id_string"]

    # APPEND
    with open(image_path, "rb") as f:
        chunk = f.read()
    append_resp = requests.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        headers=headers,
        data={
            "command": "APPEND",
            "media_id": media_id,
            "segment_index": 0,
        },
        files={"media": (os.path.basename(image_path), chunk, mime_type)}
    )
    if append_resp.status_code != 204:
        print(f"⚠️ Media APPEND failed: {append_resp.status_code} {append_resp.text[:200]}")
        return None

    # FINALIZE
    final_resp = requests.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        headers=headers,
        data={
            "command": "FINALIZE",
            "media_id": media_id,
        }
    )
    if final_resp.status_code != 201:
        print(f"⚠️ Media FINALIZE failed: {final_resp.status_code} {final_resp.text[:200]}")
        return None

    print(f"📸 Media uploaded: {media_id}")
    return media_id


def post_tweet(text, creds, persona_id=None):
    """Post a tweet with optional episode image. Returns (success, tweet_id_or_error)."""
    token = get_valid_token(creds)
    if not token:
        return False, "No valid token"

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"text": text}

    # Upload episode image if available
    if persona_id:
        img_name = IMAGE_MAP.get(persona_id.lower())
        if img_name:
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                media_id = media_upload(img_path, creds)
                if media_id:
                    payload["media"] = {"media_ids": [media_id]}
                else:
                    print("⚠️ Media upload failed, posting without image")
            else:
                print(f"⚠️ Image not found: {img_path}")
        else:
            print(f"⚠️ No image mapping for persona: {persona_id}")

    resp = requests.post(f"{API_BASE}/tweets", headers=headers, json=payload)

    if resp.status_code == 201:
        tweet_id = resp.json()["data"]["id"]
        return True, tweet_id
    elif resp.status_code == 401:
        token = refresh_access_token(creds)
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.post(f"{API_BASE}/tweets", headers=headers, json=payload)
            if resp.status_code == 201:
                return True, resp.json()["data"]["id"]
        return False, f"Auth failed: {resp.text[:200]}"
    else:
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"


def get_now_arg():
    """Get current time in Argentina."""
    now = datetime.now(timezone.utc) + timedelta(hours=ARG_TIMEZONE)
    return now


def get_slot():
    """Determine the slot from command line argument."""
    if len(sys.argv) < 2:
        print("❌ Uso: python3 post-tweet.py morning|noon|evening")
        sys.exit(1)
    slot = sys.argv[1].lower()
    if slot not in ("morning", "noon", "evening"):
        print(f"❌ Slot invalido: {slot}. Usa morning, noon, o evening.")
        sys.exit(1)
    return slot


def find_post(schedule, today_str, slot):
    """Find the first unposted post for today and slot."""
    for post in schedule:
        if post["date"] == today_str and post["slot"] == slot and not post.get("posted", False):
            return post
    return None


def main():
    slot = get_slot()

    if not os.path.exists(SCHEDULE_FILE):
        print(f"❌ Schedule file not found: {SCHEDULE_FILE}")
        sys.exit(1)

    with open(SCHEDULE_FILE) as f:
        data = json.load(f)

    now = get_now_arg()
    today = now.strftime("%Y-%m-%d")

    schedule = data["schedule"]
    post = find_post(schedule, today, slot)

    if not post:
        print(f"📭 No pending post for {today} ({slot}). Checking if already posted or no schedule.")
        today_posts = [p for p in schedule if p["date"] == today and p["slot"] == slot]
        if today_posts:
            print(f"   Already posted: {today_posts[0].get('posted', False)}")
        sys.exit(0)

    print(f"📝 Posting: [{post.get('emoji','')} {post['name']}] {post['content'][:80]}...")

    creds = load_creds()
    success, result = post_tweet(post["content"], creds, persona_id=post.get("persona_id"))

    if success:
        post["posted"] = True
        post["tweet_id"] = result
        post["posted_at"] = now.isoformat()
        data["schedule"] = schedule
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Posted! ID: {result}")
    else:
        print(f"❌ Failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
