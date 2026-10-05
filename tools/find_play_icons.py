with open('tools/generate_full_html.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if any(w in line for w in ['▶️', '⏸️', 'play-btn', 'playBtnIcon', 'm2-icon', 'm2-btn']):
            clean = line.strip().encode('ascii', 'replace').decode('ascii')
            print(f'{i+1}: {clean[:110]}')
