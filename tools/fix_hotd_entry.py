import json

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/harem_songs_verified.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for s in songs:
    if s["anime"] == "Highschool of the Dead":
        s["video_id"] = "H0mCytVZQiY"
        s["video_url"] = "https://www.youtube.com/watch?v=H0mCytVZQiY"
        s["video_title"] = "HIGHSCHOOL OF THE DEAD - Kishida Kyoudan"

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz/tools/harem_songs_verified.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print("HOTD ID set to H0mCytVZQiY")
