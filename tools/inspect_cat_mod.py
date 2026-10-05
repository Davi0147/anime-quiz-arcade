# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

p_cat = text.find('Catálogo Completo')
p_mod = text.find('settings-modal-card')
p_lb = text.find('<!-- Lightbox Modal -->')

print("p_cat:", p_cat)
print("p_mod:", p_mod)
print("p_lb:", p_lb)

if p_cat != -1:
    print("Catálogo snippet:")
    print(text[p_cat-150:p_cat+400])
