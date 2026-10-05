# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tags = ['div', 'span', 'button', 'section', 'header', 'aside', 'main', 'nav', 'table', 'tbody', 'thead', 'tr', 'th', 'td']
all_ok = True
for t in tags:
    open_count = len(re.findall(rf'<{t}\b', html, re.IGNORECASE))
    close_count = len(re.findall(rf'</{t}>', html, re.IGNORECASE))
    status = 'OK' if open_count == close_count else 'MISMATCH'
    if status != 'OK':
        all_ok = False
    print(f"<{t}>: {open_count} open, {close_count} close -> {status}")

print("TAG BALANCE STATUS:", "100% BALANCED" if all_ok else "ERRORS FOUND")
