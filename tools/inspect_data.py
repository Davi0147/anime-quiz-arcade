import json

with open("C:/Users/luizd/.gemini/antigravity/scratch/anime_songs_verified.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"{'#':<3} | {'Ano':<4} | {'Anime':<32} | {'Música':<24} | {'Artista':<20} | {'URL'}")
print("-" * 120)
for x in items:
    print(f"{x['id']:<3} | {x['year']:<4} | {x['anime'][:32]:<32} | {x['song'][:24]:<24} | {x['artist'][:20]:<20} | {x['video_url']}")
