import urllib.request, urllib.parse, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

q = 'Highschool of the Dead opening Kishida'
url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(q)}'
html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:10]

for v in vids:
    e_url = f'https://www.youtube.com/embed/{v}'
    try:
        r = urllib.request.urlopen(urllib.request.Request(e_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})).read().decode('utf-8')
        if 'UNPLAYABLE' not in r and 'status":"ERROR"' not in r and 'unavailable' not in r.lower():
            print('Found working embed:', v)
            with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
                songs = json.load(f)
            songs[17]["anime"] = "Highschool of the Dead"
            songs[17]["song"] = "HIGHSCHOOL OF THE DEAD"
            songs[17]["artist"] = "Kishida Kyoudan & THE Akeboshi Rockets"
            songs[17]["hint"] = "Ação / Apocalipse Zumbi no Colégio / Ecchi e Sobrevivência"
            songs[17]["diff"] = "⭐⭐ Média"
            songs[17]["video_id"] = v
            songs[17]["video_url"] = f"https://www.youtube.com/watch?v={v}"
            with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "w", encoding="utf-8") as f:
                json.dump(songs, f, ensure_ascii=False, indent=2)
            print("Successfully updated song 18!")
            sys.exit(0)
    except:
        pass
print("Not found")
