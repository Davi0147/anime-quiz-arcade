import json

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for s in songs:
    if s["id"] == 18:
        s["anime"] = "Durarara!!"
        s["song"] = "Uragiri no Yuuyake"
        s["artist"] = "THEATRE BROOK"
        s["hint"] = "Mistério / Ikebukuro / Motoqueiro Sem Cabeça e Gangue dos Dollars"
        s["diff"] = "⭐⭐ Média"
        s["video_id"] = "oikvju7vAg4"
        s["video_url"] = "https://www.youtube.com/watch?v=oikvju7vAg4"

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print("Updated song 18 to Durarara!!")
