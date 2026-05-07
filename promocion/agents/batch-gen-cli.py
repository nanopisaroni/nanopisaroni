#!/usr/bin/env python3
"""Generate 30 posts for each specified persona by calling the agents CLI."""
import subprocess, sys, json, os

persona_ids = sys.argv[1:] if len(sys.argv) > 1 else []
if not persona_ids:
    print("Usage: batch-gen.py <persona_id1> <persona_id2> ...")
    sys.exit(1)

SCRIPT = "/home/nanobot/sitio/promocion/agents/panteon-agents.py"
OUT_DIR = "/home/nanobot/sitio/promocion/posts"

all_posts = []
for pid in persona_ids:
    posts = []
    attempts = 0
    while len(posts) < 30 and attempts < 100:
        result = subprocess.run(
            ["python3", SCRIPT, "--post", pid],
            capture_output=True, text=True, timeout=15
        )
        output = result.stdout or result.stderr
        # Extract the post content - it's between emoji line and hashtags
        lines = [l.strip() for l in output.split('\n') if l.strip()]
        # Find the actual tweet content
        content_lines = []
        in_post = False
        for line in lines:
            if line.startswith('📖 https://') or line.startswith('📚  @'):
                in_post = True
                continue
            if in_post and line and not line.startswith('--') and not line.startswith('📖'):
                content_lines.append(line)
        
        post_text = ' '.join(content_lines).strip()
        if post_text and len(post_text) > 20:
            if post_text not in [p['content'] for p in posts]:
                posts.append({
                    "persona_id": pid,
                    "content": post_text
                })
        attempts += 1
    
    all_posts.extend(posts)
    print(f"✅ {pid}: {len(posts)} posts")

# Save
os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, f"posts-{'-'.join(persona_ids)}.json"), "w") as f:
    json.dump(all_posts, f, indent=2, ensure_ascii=False)

print(f"\nTotal: {len(all_posts)} posts → {OUT_DIR}")
