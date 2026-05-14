#!/usr/bin/env python3.12
"""
Postea el próximo tweet pendiente del schedule maestro.
Ignora slots horarios — agarra el primer no-postteado en orden.
Uso: python3 post-next-pending.py

Para catch-up rápido (48/día): correr cada 30 minutos.
Para ritmo normal (24/día): correr cada 60 minutos.
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
LOG_FILE = os.path.join(os.path.dirname(__file__), "posts/posting-log.json")


def load_creds():
    with open(CREDS_FILE) as f:
        return json.load(f)


def save_creds(creds):
    with open(CREDS_FILE, "w") as f:
        json.dump(creds, f, indent=2)


def refresh_access_token(creds):
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
    return creds["access_token"]


def get_valid_token(creds):
    if creds.get("token_expires_at") and time.time() < creds["token_expires_at"] - 60:
        return creds["access_token"]
    return refresh_access_token(creds)


def post_tweet(text, creds):
    token = get_valid_token(creds)
    if not token:
        return False, "No valid token"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{API_BASE}/tweets", headers=headers, json={"text": text})
    if resp.status_code == 201:
        return True, resp.json()["data"]["id"]
    elif resp.status_code == 429:
        return False, "RATE_LIMITED"
    elif resp.status_code == 401:
        token = refresh_access_token(creds)
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.post(f"{API_BASE}/tweets", headers=headers, json={"text": text})
            if resp.status_code == 201:
                return True, resp.json()["data"]["id"]
        return False, f"Auth failed: {resp.text[:200]}"
    else:
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"


def log_posting(entry):
    log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            log = json.load(f)
    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def main():
    if not os.path.exists(SCHEDULE_FILE):
        print(f"❌ Schedule not found: {SCHEDULE_FILE}")
        sys.exit(1)

    with open(SCHEDULE_FILE) as f:
        data = json.load(f)

    schedule = data.get("schedule", [])
    pending = [p for p in schedule if not p.get("posted")]

    if not pending:
        print("✅ No pending tweets. Schedule complete!")
        sys.exit(0)

    # Take the next pending tweet
    post = pending[0]
    print(f"📝 [{post['date']} {post['time']}] {post['emoji']} {post['name']}: {post['content'][:80]}...")

    creds = load_creds()
    success, result = post_tweet(post["content"], creds)

    if success:
        post["posted"] = True
        post["tweet_id"] = result
        post["posted_at"] = datetime.now(timezone.utc).isoformat()
        data["schedule"] = schedule
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        log_posting({
            "id": post.get("id", ""),
            "name": post["name"],
            "content": post["content"][:100],
            "tweet_id": result,
            "posted_at": post["posted_at"],
            "remaining": len(pending) - 1,
        })

        print(f"✅ Posted! ID: {result}")
        remaining = len(pending) - 1
        print(f"📊 {remaining} tweets pendientes ({remaining/48:.1f} días a 48/día)")
        sys.exit(0)
    elif result == "RATE_LIMITED":
        print(f"⚠️  Rate limited. Próximo intento en ~15 min.")
        sys.exit(75)  # Exit code for rate-limited (will auto-retry next cron tick)
    else:
        print(f"❌ Failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
