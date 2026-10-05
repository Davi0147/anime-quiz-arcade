# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p_body = text.find('<body>')
p_m1 = text.find('id="mode1-view"')
print("=== BETWEEN BODY AND MODE 1 ===")
print(text[p_body:p_m1])
