#!/usr/bin/env python3
"""Fix all remaining numbering in panteon.html - shift #10->#16."""
import re

with open("/home/nanobot/sitio/panteon.html", "r") as f:
    html = f.read()

lines = html.split("\n")

# Fix H2 headings (the span.num ones)
# Current -> Correct:
# #10 Yudkowsky -> #11
# #11 Marco Aurelio -> #12
# #12 Epicteto -> #13
# #13 Alan Watts -> #14
# #14 Krishnamurti -> #15
# #16 Facundo Cabral -> #16 (stays)

fix_map = {
    '#10</span> Eliezer Yudkowsky': '#11</span> Eliezer Yudkowsky',
    '#11</span> Marco Aurelio': '#12</span> Marco Aurelio',
    '#12</span> Epicteto': '#13</span> Epicteto',
    '#13</span> Alan Watts': '#14</span> Alan Watts',
    '#14</span> Jiddu Krishnamurti': '#15</span> Jiddu Krishnamurti',
}

for i, line in enumerate(lines):
    for old, new in fix_map.items():
        if old in line:
            lines[i] = line.replace(old, new)
            print(f"  Line {i+1}: fixed {old.split('</span>')[0]} -> {new.split('</span>')[0]}")

# Fix section IDs that are wrong
# thinker-14 should be thinker-15 for Krishnamurti
fix_ids = {'id="thinker-14"': 'id="thinker-15"'}
for i, line in enumerate(lines):
    if 'id="thinker-14"' in line and 'Krishnamurti' in html.split('\n')[i]:
        lines[i] = line.replace('id="thinker-14"', 'id="thinker-15"')
        print(f"  Line {i+1}: fixed id from thinker-14 to thinker-15")

# Verify Ayudkowsky's heading and section id
for i, line in enumerate(lines):
    if 'id="thinker-10"' in line and 'Yudkowsky' in line:
        print(f"  Line {i+1}: Yudkowsky has thinker-10 id - THIS IS WRONG, shifting issue!")
    if 'id="thinker-11"' in line and 'Yudkowsky' in line:
        print(f"  Line {i+1}: Yudkowsky has thinker-11 id - correct!")

# Check Naval
for i, line in enumerate(lines):
    if 'id="thinker-10"' in line and 'Naval' in line:
        print(f"  Line {i+1}: Naval has thinker-10 id - correct!")

output = "\n".join(lines)
with open("/home/nanobot/sitio/panteon.html", "w") as f:
    f.write(output)

print("\nDone!")

# Final verification
for i, line in enumerate(output.split("\n")):
    if '<h2><span class="num">' in line:
        print(f"  Section: {line.strip()}")
