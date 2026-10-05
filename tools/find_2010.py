import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    {"anime": "Bleach", "song": "Ranbu no Melody", "artist": "SID", "year": 2010, "hint": "Ação / Batalha de Karakura / Ichigo vs Aizen", "q": "Bleach opening 13 Ranbu no Melody SID official"},
    {"anime": "Durarara!!", "song": "Uragiri no Yuuyake", "artist": "THEATRE BROOK", "year": 2010, "hint": "Mistério / Ikebukuro / Motoqueiro Sem Cabeça e Dollars", "q": "Durarara opening 1 official"},
    {"anime": "Fullmetal Alchemist: Brotherhood", "song": "Period", "artist": "CHEMISTRY", "year": 2010, "hint": "Ação / Alquimia / Dia Prometido", "q": "Fullmetal Alchemist Brotherhood opening 4 Period"}
]

for cand in candidates:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(cand['q'])}"
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:5]
    for v in vids:
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"https://www.youtube.com/embed/{v}", headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})).read().decode('utf-8')
            if 'status":"ERROR"' not in r and 'unavailable' not in r.lower():
                print(f"SUCCESS: {cand['anime']} - {cand['song']} -> {v}")
                sys.exit(0)
        except Exception as e:
            pass
