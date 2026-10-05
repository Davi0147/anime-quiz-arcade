# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Scan HTML for div tags with line numbers
stack = []
lines = html.splitlines()

for line_idx, line in enumerate(lines, 1):
    # Find all <div or </div
    tokens = re.finditer(r'<(/?)div\b[^>]*>', line, re.IGNORECASE)
    for m in tokens:
        tag_str = m.group(0)
        is_closing = tag_str.startswith('</')
        if not is_closing:
            stack.append((line_idx, tag_str[:60]))
        else:
            if stack:
                stack.pop()
            else:
                print(f"Extra closing div at line {line_idx}: {line}")

if stack:
    print(f"Total unclosed divs: {len(stack)}")
    for line_idx, snippet in stack:
        print(f"Unclosed div opened at line {line_idx}: {snippet}")
else:
    print("All divs matched!")
