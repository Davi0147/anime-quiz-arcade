import urllib.request
import urllib.parse
import re
import json
import time
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    if not item.get("video_id"):
        q = item["query"]
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
            vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))
            vid_id = vids[0] if vids else ""
            title = ""
            if vid_id:
                try:
                    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid_id}&format=json"
                    oembed_req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
                    res = json.loads(urllib.request.urlopen(oembed_req, timeout=5).read().decode('utf-8'))
                    title = res.get("title", "")
                except Exception:
                    title = "YouTube Video"
            item["video_id"] = vid_id
            item["video_url"] = f"https://www.youtube.com/watch?v={vid_id}"
            item["video_title"] = title
            print(f"[RETRY OK] {item['anime']} -> {item['video_url']}")
        except Exception as e:
            print(f"[RETRY FAIL] {item['anime']}: {e}")
        time.sleep(0.5)

# Also check JoJo (item 23 had title truncated in print, let's verify item 23)
with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

missing = [x for x in items if not x.get("video_id")]
print(f"Total: {len(items)}, Faltando: {len(missing)}")
