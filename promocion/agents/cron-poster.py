#!/usr/bin/env python3
"""Cron posting script — reads the master schedule and posts to X."""
import json, os, subprocess, sys

SCHEDULE_FILE = "/home/nanobot/sitio/promocion/posts/master-schedule.json"
POSTED_LOG = "/home/nanobot/sitio/promocion/posts/posted-log.json"
XURL = "/home/nanobot/.local/bin/xurl"

def main():
    # Load schedule
    with open(SCHEDULE_FILE) as f:
        data = json.load(f)
    
    # Load posted log
    posted = {}
    if os.path.exists(POSTED_LOG):
        with open(POSTED_LOG) as f:
            posted = json.load(f)
    
    # Find today's posts that haven't been posted
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    for entry in data["schedule"]:
        if entry["date"] != today:
            continue
        if entry["id"] in posted:
            continue
        
        # Post to X
        content = f'{entry["emoji"]} {entry["full_name"]}\n\n{entry["content"]}'
        try:
            result = subprocess.run(
                [XURL, "post", content],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                posted[entry["id"]] = {
                    "timestamp": datetime.now().isoformat(),
                    "status": "posted",
                    "response": result.stdout[:200]
                }
                print(f"✅ Posted: {entry['id']} - {entry['name']}")
            else:
                posted[entry["id"]] = {
                    "timestamp": datetime.now().isoformat(),
                    "status": "failed",
                    "error": result.stderr[:200]
                }
                print(f"❌ Failed: {entry['id']} - {result.stderr[:100]}")
        except Exception as e:
            posted[entry["id"]] = {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)[:200]
            }
            print(f"❌ Error: {entry['id']} - {e}")
    
    # Save posted log
    with open(POSTED_LOG, "w") as f:
        json.dump(posted, f, indent=2)
    
    print(f"\nDone. {len(posted)} total posts logged.")

if __name__ == "__main__":
    main()
