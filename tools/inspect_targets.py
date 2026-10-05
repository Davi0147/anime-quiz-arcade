# -*- coding: utf-8 -*-
"""
Script de Verificação de Alvos para as Correções v3.2
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

targets = [
    '--sidebar-w-expanded',
    'title="Modo 1: Blind Test"',
    'title="Modo 2: Qual é a Abertura?"',
    'id="m2-txt-0"',
    'function switchGameMode',
    '.mp-live-sidebar {',
    'mp-player-status-badge',
    'renderTags',
    'Configurações & Som',
    '.mode-split-grid {'
]

for t in targets:
    pos = text.find(t)
    print(f"{t:<35} -> {'ACHOU (pos ' + str(pos) + ')' if pos != -1 else 'NÃO ACHOU'}")
