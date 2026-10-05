# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p3 = text.find('id="mode3-view"')
p4 = text.find('id="mode4-view"')
print("=== MODE 3 VIEW HTML ===")
print(text[p3:p4])
