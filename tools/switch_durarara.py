import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

q = 'Durarara opening 1 Uragiri no Yuuyake'
url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(q)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:10]

good_id = None
for v in vids:
    e_url = f'https://www.youtube.com/embed/{v}'
    try:
        r = urllib.request.urlopen(urllib.request.Request(e_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})).read().decode('utf-8')
        if 'UNPLAYABLE' not in r and 'status":"ERROR"' not in r and 'unavailable' not in r.lower():
            good_id = v
            print('Found good embed for Durarara:', v)
            break
    except Exception as e:
        pass

if good_id:
    with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
        songs = json.load(f)
    for s in songs:
        if s["id"] == 18:
            s["anime"] = "Durarara!!"
            s["song"] = "Uragiri no Yuuyake"
            s["artist"] = "THEATRE BROOK"
            s["hint"] = "Mistério / Ikebukuro / Motoqueiro Sem Cabeça e Gangue dos Dollars"
            s["diff"] = "⭐⭐ Média"
            s["video_id"] = good_id
            s["video_url"] = f"https://www.youtube.com/watch?v={good_id}"
    with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print("Updated song 18 to Durarara with working embed!")
