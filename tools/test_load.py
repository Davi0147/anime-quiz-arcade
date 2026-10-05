import json
import os

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
SONGS_FILE = os.path.join(DIR, "anime_songs_verified.json")
SCENES_FILE = os.path.join(DIR, "tools", "anime_scenes.json")

with open(SONGS_FILE, "r", encoding="utf-8") as f:
    songs = json.load(f)

with open(SCENES_FILE, "r", encoding="utf-8") as f:
    scenes = json.load(f)

songs_json = json.dumps(songs, ensure_ascii=False)
scenes_json = json.dumps(scenes, ensure_ascii=False)

print(f"Loaded {len(songs)} songs and {len(scenes)} scenes.")
