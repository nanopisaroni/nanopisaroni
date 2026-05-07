#!/usr/bin/env python3
"""Fix cascading renumbering - apply high to low."""
import re

with open("/home/nanobot/sitio/panteon.html", "r") as f:
    html = f.read()

lines = html.split("\n")

# Apply renumbering HIGH to LOW to avoid cascade
# We need to shift each section by +1, but do it in reverse order
# Current: thinker-11, thinker-12, thinker-13, thinker-14, thinker-15
# Should be: thinker-12, thinker-13, thinker-14, thinker-15, thinker-16

# For IDs: do 15→16 first, then 14→15, etc.
for i in range(len(lines)):
    line = lines[i]
    new_line = line
    
    # Fix section IDs: 15→16, 14→15, ... 10→11
    # Also fix the visible numbers in headings
    replacements = [
        ('id="thinker-15"', 'id="thinker-16"', '#15', '#16'),
        ('id="thinker-14"', 'id="thinker-15"', '#14', '#15'),
        ('id="thinker-13"', 'id="thinker-14"', '#13', '#14'),
        ('id="thinker-12"', 'id="thinker-13"', '#12', '#13'),
        ('id="thinker-11"', 'id="thinker-12"', '#11', '#12'),
        ('id="thinker-10"', 'id="thinker-11"', '#10', '#11'),
    ]
    
    for old_id, new_id, old_num, new_num in replacements:
        if old_id in new_line or old_num in new_line:
            new_line = new_line.replace(old_id, new_id)
            new_line = new_line.replace(f'<span class="num">{old_num}</span>', f'<span class="num">{new_num}</span>')
    
    lines[i] = new_line

output = "\n".join(lines)
with open("/home/nanobot/sitio/panteon.html", "w") as f:
    f.write(output)

print("Done! Verifying...")

# Verify
for line in output.split("\n"):
    if '<h2><span class="num">' in line:
        print(f"  {line.strip()}")
        
# Check all thinker IDs
ids = re.findall(r'id="thinker-\d+"', output)
for s in sorted(set(ids)):
    print(f"  ID: {s}")
