# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Find non-ASCII characters outside standard latin/portuguese accented letters
# Regex for emojis: unicode ranges
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]')

found = emoji_pattern.findall(text)
unique_emojis = sorted(list(set(found)))

print(f"Total emojis found: {len(found)}")
print(f"Unique emojis: {len(unique_emojis)}")

for e in unique_emojis:
    count = text.count(e)
    # Find sample context
    p = text.find(e)
    ctx = text[max(0, p-30):min(len(text), p+40)].replace('\n', ' ')
    print(f"{e} (x{count}): {ctx}")
