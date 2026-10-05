import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/anime_songs_verified.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for s in songs:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={s['video_id']}&format=json"
    try:
        data = json.loads(urllib.request.urlopen(url, timeout=5).read().decode('utf-8'))
        title = data.get("title", "")
        author = data.get("author_name", "")
        print(f"#{s['id']:02d} | {s['anime']:<25} | {author:<20} | {title}")
    except Exception as e:
        print(f"#{s['id']:02d} | {s['anime']:<25} | ERROR: {e}")
