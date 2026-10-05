# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p4 = text.find('id="mode4-view"')
p_cat = text.find('<!-- Full Table Overview -->')
print("=== MODE 4 AND MODE 5 VIEW HTML ===")
print(text[p4:p_cat])
