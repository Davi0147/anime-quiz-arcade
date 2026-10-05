import json
import os

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"

with open(os.path.join(DIR, "anime_songs_verified.json"), "r", encoding="utf-8") as f:
    master = json.load(f)

with open(os.path.join(DIR, "tools", "harem_songs_verified.json"), "r", encoding="utf-8") as f:
    harem_songs = json.load(f)

# Avoid duplicates if any already exist by anime name
existing_names = {s["anime"].lower() for s in master}

added = 0
for h in harem_songs:
    if h["anime"].lower() not in existing_names:
        master.append(h)
        added += 1

# Sort chronologically by year, then by anime
master.sort(key=lambda x: (x["year"], x["anime"]))

# Re-index ids from 1 to N
for idx, s in enumerate(master, start=1):
    s["id"] = idx

print(f"Total songs now: {len(master)} (Adicionados: {added})")

# Save master json
with open(os.path.join(DIR, "anime_songs_verified.json"), "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Saved updated master JSON!")
