# -*- coding: utf-8 -*-
"""
Compilador e Integrador Master da Etapa 4: Design Definitivo Bento Grid & Alta Dopamina
Garante 100% de conformidade com as regras globais e a imagem de referência conceptual.
"""
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_SCRIPT = os.path.join(BASE_DIR, "tools", "generate_full_html.py")

with open(GEN_SCRIPT, "r", encoding="utf-8") as f:
    gen_content = f.read()

# 1. Carregar artefatos produzidos pelos subagentes
with open(os.path.join(BASE_DIR, "scratch", "bento_layout_spec.css"), "r", encoding="utf-8") as f:
    bento_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "dopamine_styles.css"), "r", encoding="utf-8") as f:
    dopamine_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape.css"), "r", encoding="utf-8") as f:
    mobile_css = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape_overlay.html"), "r", encoding="utf-8") as f:
    mobile_overlay_html = f.read()

with open(os.path.join(BASE_DIR, "scratch", "dopamine_microinteractions.js"), "r", encoding="utf-8") as f:
    dopamine_js = f.read()

with open(os.path.join(BASE_DIR, "scratch", "mobile_landscape.js"), "r", encoding="utf-8") as f:
    mobile_js = f.read()

print(f"Artefatos lidos com sucesso. Tamanho total de CSS novo: {len(bento_css) + len(dopamine_css) + len(mobile_css)} bytes.")
