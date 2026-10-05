# -*- coding: utf-8 -*-
"""
Script de teste de fusão e validação da Etapa 4
"""
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PATH = os.path.join(BASE_DIR, "tools", "generate_full_html.py")

with open(GEN_PATH, "r", encoding="utf-8") as f:
    orig = f.read()

print("Original generate_full_html.py carregado com sucesso:", len(orig), "bytes.")
