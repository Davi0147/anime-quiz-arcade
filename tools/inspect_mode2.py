# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p2 = text.find('id="mode2-view"')
p3 = text.find('id="mode3-view"')
print("=== MODE 2 VIEW HTML ===")
print(text[p2:p3])
