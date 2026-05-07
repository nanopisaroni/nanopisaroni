#!/usr/bin/env python3
"""Combine all 480 posts into a single 12-week posting schedule."""
import json, os, glob, random
from datetime import datetime, timedelta

posts_dir = "/home/nanobot/sitio/promocion/posts"
agents_dir = "/home/nanobot/sitio/promocion/agents"
os.makedirs(posts_dir, exist_ok=True)

persona_map = {
    "taleb": {"name":"Taleb","full":"Nassim Nicholas Taleb","emoji":"🦢","lang":"en"},
    "borges": {"name":"Borges","full":"Jorge Luis Borges","emoji":"📚","lang":"es"},
    "feynman": {"name":"Feynman","full":"Richard Feynman","emoji":"🔬","lang":"en"},
    "deutsch": {"name":"Deutsch","full":"David Deutsch","emoji":"🌌","lang":"en"},
    "thiel": {"name":"Thiel","full":"Peter Thiel","emoji":"🏢","lang":"en"},
    "popper": {"name":"Popper","full":"Karl Popper","emoji":"⚗️","lang":"en"},
    "munger": {"name":"Munger","full":"Charlie Munger","emoji":"🧠","lang":"en"},
    "kahneman": {"name":"Kahneman","full":"Daniel Kahneman","emoji":"🧪","lang":"en"},
    "graham": {"name":"PG","full":"Paul Graham","emoji":"✍️","lang":"en"},
    "yudkowsky": {"name":"Yudkowsky","full":"Eliezer Yudkowsky","emoji":"🤖","lang":"en"},
    "marcus": {"name":"Marco Aurelio","full":"Marco Aurelio","emoji":"🏛️","lang":"en"},
    "epicteto": {"name":"Epicteto","full":"Epicteto","emoji":"🔥","lang":"en"},
    "watts": {"name":"Alan Watts","full":"Alan Watts","emoji":"☯️","lang":"en"},
    "krishnamurti": {"name":"Krishnamurti","full":"Jiddu Krishnamurti","emoji":"🕊️","lang":"en"},
    "cabral": {"name":"Cabral","full":"Facundo Cabral","emoji":"🎸","lang":"es"},
    "naval": {"name":"Naval","full":"Naval Ravikant","emoji":"💎","lang":"en"},
}

# File mapping (handling different naming conventions)
file_map = {
    "taleb": ["taleb_tweets.json"],
    "borges": ["posts-borges.json"],
    "feynman": ["feynman_tweets.json"],
    "deutsch": ["deutsch_tweets.json"],
    "thiel": ["thiel_tweets.json"],
    "popper": ["popper_tweets.json"],
    "munger": ["munger_tweets.json"],
    "kahneman": ["kahneman_tweets.json"],
    "graham": ["pg-tweets.json"],
    "yudkowsky": ["yudkowsky_tweets.json"],
    "marcus": ["marcus_aurelius_tweets.json"],
    "epicteto": ["epictetus_tweets.json"],
    "watts": ["alan_watts_tweets.json"],
    "krishnamurti": ["krishnamurti_tweets.json"],
    "cabral": ["facundo_cabral_tweets.json"],
    "naval": ["naval_tweets.json"],
}

# Load all posts
all_posts = []
sources = ["/home/nanobot"]  # Where subagents saved files

for persona_id, filenames in file_map.items():
    loaded = False
    for src in sources:
        for fn in filenames:
            fpath = os.path.join(src, fn)
            if os.path.exists(fpath):
                try:
                    with open(fpath) as f:
                        posts = json.load(f)
                    info = persona_map[persona_id]
                    for p in posts:
                        text = p if isinstance(p, str) else p.get("content", str(p))
                        all_posts.append({
                            "persona_id": persona_id,
                            "name": info["name"],
                            "full_name": info["full"],
                            "emoji": info["emoji"],
                            "lang": info["lang"],
                            "content": text
                        })
                    print(f"✅ {persona_id}: {len(posts)} posts ({fn})")
                    loaded = True
                    break
                except Exception as e:
                    print(f"⚠️ {fn}: {e}")
        if loaded:
            break
    if not loaded:
        print(f"❌ {persona_id}: NO FILE FOUND")

print(f"\nTotal loaded: {len(all_posts)} posts")

if len(all_posts) < 400:
    print(f"⚠️ Only {len(all_posts)} posts — expected ~480. Will reuse for schedule.")
else:
    print("✅ Enough posts for full schedule")

# Shuffle posts for variety
random.shuffle(all_posts)

# Create schedule: 3 posts/day at 9AM, 2PM, 8PM ARG
start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
schedule = []
time_slots = [9, 14, 20]  # 9am, 2pm, 8pm

for day_offset in range(84):  # 12 weeks = 84 days
    date = start_date + timedelta(days=day_offset)
    for slot_idx, hour in enumerate(time_slots):
        if not all_posts:
            break
        post = all_posts.pop(0) if all_posts else all_posts[-1]
        minute = random.randint(0, 30)
        post_time = date.replace(hour=hour, minute=minute)
        schedule.append({
            "id": f"day{day_offset+1:03d}-{['morn','noon','eve'][slot_idx]}",
            "date": post_time.strftime("%Y-%m-%d"),
            "time": post_time.strftime("%H:%M"),
            "week": (day_offset // 7) + 1,
            "day_name": date.strftime("%A"),
            "slot": ["morning","noon","evening"][slot_idx],
            "persona_id": post["persona_id"],
            "name": post["name"],
            "full_name": post["full_name"],
            "emoji": post["emoji"],
            "lang": post["lang"],
            "content": post["content"],
            "posted": False
        })

# Save everything
output = {
    "account": "@PanteonBook",
    "total_posts": len(schedule),
    "generated_at": datetime.now().isoformat(),
    "posting_times": "9:00, 14:00, 20:00 ARG (3 posts/day)",
    "start_date": start_date.isoformat(),
    "end_date": (start_date + timedelta(days=83)).isoformat(),
    "schedule": schedule
}

master_file = os.path.join(posts_dir, "master-schedule.json")
with open(master_file, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Also save a readable version
readable = os.path.join(posts_dir, "readable-schedule.txt")
with open(readable, "w") as f:
    f.write(f"PANTEÓN POSTING SCHEDULE — 12 WEEKS\n")
    f.write(f"Account: @PanteonBook\n")
    f.write(f"Times: 9:00, 14:00, 20:00 ARG (3 posts/day)\n")
    f.write(f"Total: {len(schedule)} posts\n{'='*70}\n\n")
    for s in schedule[:30]:  # Show first 30 as preview
        f.write(f"[Week {s['week']:2d}] {s['date']} {s['time']} | {s['emoji']} {s['name']} ({s['slot']})\n")
        f.write(f"  → {s['content'][:120]}...\n\n")

print(f"\n📁 {master_file}")
print(f"📁 {readable}")
print(f"📊 {len(schedule)} posts scheduled over 12 weeks")
print(f"🎯 Starts: {start_date.strftime('%Y-%m-%d')}")
print(f"🏁 Ends: {(start_date + timedelta(days=83)).strftime('%Y-%m-%d')}")
