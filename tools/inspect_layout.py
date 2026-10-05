# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

sections = [
    '<style>',
    '<header',
    'id="game-container"',
    'id="mode1-view"',
    'id="mode2-view"',
    'id="mode3-view"',
    'id="mode4-view"',
    'id="mode5-view"',
    'id="full-catalog-panel"',
    'id="main-scoreboard"',
    'function switchGameMode',
    'function switchMpSubTab',
    'function setupAutocomplete'
]

for s in sections:
    pos = text.find(s)
    line_no = text[:pos].count('\n') + 1 if pos != -1 else -1
    print(f"{s:<30} -> line {line_no}")
