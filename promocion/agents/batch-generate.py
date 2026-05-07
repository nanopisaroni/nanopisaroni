#!/usr/bin/env python3
"""
Batch post generator — generates 30 posts per persona (480 total),
creates a 12-week posting schedule, and exports everything for cron.
"""
import json, os, random, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Extract PERSONAS and HASHTAGS from the main agents script
exec_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(exec_dir, 'panteon-agents.py')) as f:
    src = f.read()
# Remove the argparse part and exec just the data + definitions
cutoff = src.find('import argparse')
if cutoff > 0:
    src = src[:cutoff]
# Remove the main block
main_cutoff = src.find("if __name__")
if main_cutoff > 0:
    src = src[:main_cutoff]
exec(src)

OUT_DIR = os.path.join(exec_dir, '..', 'posts')
os.makedirs(OUT_DIR, exist_ok=True)

def generate_posts_for_persona(p, n=30):
    """Generate n posts for a single persona with maximum variety."""
    posts = []
    # Use all sample_tweets as base
    base_tweets = list(p.sample_tweets)
    catchphrases = list(p.catchphrases)
    
    idx = 0
    while len(posts) < n:
        # Cycle through sample tweets
        tweet = base_tweets[idx % len(base_tweets)]
        
        # Vary the structure
        variant = idx % 5
        if variant == 0:
            # Just the tweet
            content = tweet
        elif variant == 1:
            # Tweet + catchphrase
            content = f"{tweet}\n\n{random.choice(catchphrases)}"
        elif variant == 2:
            # Catchphrase + tweet
            content = f"{random.choice(catchphrases)}\n\n{tweet}"
        elif variant == 3:
            # Topic-based variation
            topic = random.choice(p.weekly_topics)
            content = f"On {topic}: {random.choice(catchphrases)}"
        elif variant == 4:
            # Book angle focused
            content = f"{tweet}\n\n📖 {p.book_angle[:200]}"
        
        # Add hashtags (different combinations)
        tags = random.choice([
            f"\n\n{HASHTAGS}",
            f"\n\n#PanteonBook #{p.name.replace(' ', '')} #Thinkers",
            f"\n\n#PersonalPantheon #{p.name.replace(' ', '')}",
            "",
        ])
        
        final = content + tags
        
        if final not in [po['content'] for po in posts]:
            posts.append({
                "persona_id": p.id,
                "persona_name": p.name,
                "full_name": p.full_name,
                "emoji": p.emoji,
                "content": final.strip(),
                "tags": tags.strip(),
            })
        
        idx += 1
    
    return posts[:n]

# Generate all posts
all_posts = []
for p in PERSONAS:
    p_posts = generate_posts_for_persona(p, 30)
    all_posts.extend(p_posts)
    print(f"✅ {p.id} ({p.name}): {len(p_posts)} posts generated")

print(f"\nTotal: {len(all_posts)} posts")

# Create schedule: 3 posts per day (morning, noon, evening)
# 4-week cycle, 16 personas, rotating
schedule = []
start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
persona_ids = [p.id for p in PERSONAS]

post_idx = 0
for week in range(12):  # 3 months
    for day in range(7):
        date = start_date + timedelta(weeks=week, days=day)
        # 3 posts per day
        for slot, hour in enumerate([9, 14, 20]):  # 9am, 2pm, 8pm
            if post_idx >= len(all_posts):
                print(f"⚠️ Ran out of posts at week {week}, day {day}, slot {slot}")
                break
            post = all_posts[post_idx]
            post_time = date.replace(hour=hour, minute=random.randint(0, 30), second=0)
            schedule.append({
                "id": f"post-{post_idx+1:03d}",
                "persona_id": post["persona_id"],
                "persona_name": post["persona_name"],
                "emoji": post["emoji"],
                "content": post["content"],
                "scheduled_for": post_time.isoformat(),
                "week": week + 1,
                "day": date.strftime("%A"),
                "slot": ["morning", "noon", "evening"][slot],
                "posted": False,
            })
            post_idx += 1

# Save everything
output = {
    "total_posts": len(all_posts),
    "total_scheduled": len(schedule),
    "account": "@PanteonBook (single account)",
    "generated_at": datetime.now().isoformat(),
    "posts": all_posts,
    "schedule": schedule,
}

with open(os.path.join(OUT_DIR, "all-posts.json"), "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Also save a human-readable schedule
with open(os.path.join(OUT_DIR, "schedule.txt"), "w") as f:
    f.write(f"PANTEÓN POSTING SCHEDULE — 12 weeks — {len(schedule)} posts\n")
    f.write(f"{'='*70}\n\n")
    for s in schedule:
        f.write(f"[{s['id']}] {s['scheduled_for'][:16]} | {s['emoji']} {s['persona_name']} ({s['slot']})\n")
        f.write(f"  → {s['content'][:100]}...\n\n")

print(f"\n✅ Saved: {len(schedule)} scheduled posts ({12} weeks, 3 posts/day)")
print(f"📁 {os.path.join(OUT_DIR, 'all-posts.json')}")
print(f"📁 {os.path.join(OUT_DIR, 'schedule.txt')}")
