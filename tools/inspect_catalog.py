# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('Catálogo Completo')
start = max(0, p - 300)
end = min(len(text), p + 1500)
print("=== CATALOG CONTEXT ===")
print(text[start:end])
