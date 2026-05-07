#!/usr/bin/env python3
"""Fix TOC in panteon.html - add Naval, renumber to 16."""

with open("/home/nanobot/sitio/panteon.html", "r") as f:
    html = f.read()

# The old TOC line content
old_toc = ('<a href="#thinker-1">#1 Jorge Luis Borges</a>'
           '<a href="#thinker-2">#2 Richard Feynman</a>'
           '<a href="#thinker-3">#3 Nassim Nicholas Taleb</a>'
           '<a href="#thinker-4">#4 David Deutsch</a>'
           '<a href="#thinker-5">#5 Peter Thiel</a>'
           '<a href="#thinker-6">#6 Karl Popper</a>'
           '<a href="#thinker-7">#7 Charlie Munger</a>'
           '<a href="#thinker-8">#8 Daniel Kahneman</a>'
           '<a href="#thinker-9">#9 Paul Graham</a>'
           '<a href="#thinker-10">#10 Eliezer Yudkowsky</a>'
           '<a href="#thinker-11">#11 Marco Aurelio</a>'
           '<a href="#thinker-12">#12 Epicteto (y S\u00e9neca)</a>'
           '<a href="#thinker-13">#13 Alan Watts</a>'
           '<a href="#thinker-14">#14 Jiddu Krishnamurti</a>'
           '<a href="#thinker-15">#15 Facundo Cabral</a>')

new_toc = ('<a href="#thinker-1">#1 Jorge Luis Borges</a>'
           '<a href="#thinker-2">#2 Richard Feynman</a>'
           '<a href="#thinker-3">#3 Nassim Nicholas Taleb</a>'
           '<a href="#thinker-4">#4 David Deutsch</a>'
           '<a href="#thinker-5">#5 Peter Thiel</a>'
           '<a href="#thinker-6">#6 Karl Popper</a>'
           '<a href="#thinker-7">#7 Charlie Munger</a>'
           '<a href="#thinker-8">#8 Daniel Kahneman</a>'
           '<a href="#thinker-9">#9 Paul Graham</a>'
           '<a href="#thinker-10">#10 Naval Ravikant</a>'
           '<a href="#thinker-11">#11 Eliezer Yudkowsky</a>'
           '<a href="#thinker-12">#12 Marco Aurelio</a>'
           '<a href="#thinker-13">#13 Epicteto (y S\u00e9neca)</a>'
           '<a href="#thinker-14">#14 Alan Watts</a>'
           '<a href="#thinker-15">#15 Jiddu Krishnamurti</a>'
           '<a href="#thinker-16">#16 Facundo Cabral</a>')

if old_toc in html:
    html = html.replace(old_toc, new_toc)
    with open("/home/nanobot/sitio/panteon.html", "w") as f:
        f.write(html)
    print("TOC updated successfully!")
else:
    print("ERROR: Could not find old TOC in file")
    # Debug: find where it breaks
    idx = html.find('<a href="#thinker-1">#1 Jorge Luis Borges</a>')
    if idx >= 0:
        # Show what's around it
        snippet = html[idx:idx+len(old_toc)]
        print(f"Found at pos {idx}")
        print(f"Expected length: {len(old_toc)}, Actual snippet length: {len(snippet)}")
        # Find first difference
        for i, (a, b) in enumerate(zip(old_toc, snippet)):
            if a != b:
                print(f"First diff at index {i}: expected {repr(a)}, got {repr(b)}")
                print(f"Context: {repr(old_toc[max(0,i-10):i+10])}")
                print(f"Context: {repr(snippet[max(0,i-10):i+10])}")
                break
