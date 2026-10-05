# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p1 = text.find('id="mode1-view"')
p2 = text.find('id="mode2-view"')
print("=== MODE 1 VIEW HTML ===")
print(text[p1:p2])
