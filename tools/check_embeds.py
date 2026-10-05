import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

print("Checking embed availability for all 42 videos...")
blocked = []

for s in songs:
    vid = s["video_id"]
    embed_url = f"https://www.youtube.com/embed/{vid}"
    try:
        req = urllib.request.Request(embed_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com'
        })
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
        
        # Check signs of embedding restriction
        if "UNPLAYABLE" in html or "Video unavailable" in html or "Playback on other websites has been disabled" in html or "status\":\"ERROR\"" in html:
            print(f"❌ BLOCKED: #{s['id']} {s['anime']} ({vid})")
            blocked.append(s)
        else:
            print(f"✅ OK: #{s['id']} {s['anime']}")
    except Exception as e:
        print(f"⚠️ ERROR checking #{s['id']} {s['anime']}: {e}")
        blocked.append(s)

print(f"\nTotal checked: {len(songs)}, Blocked from embed: {len(blocked)}")
