import urllib.request
import json
import time
import os

with open('anime_songs_verified.json', 'r', encoding='utf-8') as f:
    songs = json.load(f)

unique_animes = sorted(list(set(s['anime'] for s in songs)))
print(f"Total de animes únicos para buscar cenas/banners: {len(unique_animes)}")

query = """
query ($search: String) {
  Media (search: $search, type: ANIME) {
    id
    title { romaji english }
    bannerImage
    coverImage { large }
    genres
    startDate { year }
    studios(isMain: true) { nodes { name } }
  }
}
"""

banners = {}
for i, name in enumerate(unique_animes):
    clean_name = name.split("(")[0].strip()
    payload = json.dumps({'query': query, 'variables': {'search': clean_name}}).encode('utf-8')
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media = data.get('data', {}).get('Media')
            if media and media.get('bannerImage'):
                studios = [s['name'] for s in media.get('studios', {}).get('nodes', [])]
                banners[name] = {
                    'banner': media['bannerImage'],
                    'cover': media.get('coverImage', {}).get('large'),
                    'genres': media.get('genres', [])[:3],
                    'year': media.get('startDate', {}).get('year'),
                    'studio': studios[0] if studios else None
                }
                print(f"[{i+1}/{len(unique_animes)}] {name} -> Banner OK!")
            else:
                print(f"[{i+1}/{len(unique_animes)}] {name} -> Sem banner direto.")
    except Exception as e:
        print(f"[{i+1}/{len(unique_animes)}] {name} Erro: {e}")
    time.sleep(0.3)

with open('tools/anime_banners_cache.json', 'w', encoding='utf-8') as f:
    json.dump(banners, f, ensure_ascii=False, indent=2)

print(f"\nTotal com banners encontrados: {len(banners)} / {len(unique_animes)}")
