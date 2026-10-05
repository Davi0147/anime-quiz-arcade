# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('<header')
p_end = text.find('id="mode1-view"')
print("=== HEADER AND CONTAINER ===")
print(text[p-200:p_end])
