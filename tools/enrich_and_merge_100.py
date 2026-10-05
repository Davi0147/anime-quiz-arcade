import json
import urllib.request
import urllib.parse
import os
import time

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
BASE_JSON = os.path.join(DIR, "anime_songs_verified.json")
NEW_JSON = os.path.join(DIR, "tools", "found_25_songs.json")
BANNERS_CACHE = os.path.join(DIR, "tools", "anime_banners_cache.json")
COVERS_CACHE = os.path.join(DIR, "tools", "anime_covers_cache.json")
SCENES_PATH = os.path.join(DIR, "tools", "anime_scenes.json")

with open(BASE_JSON, "r", encoding="utf-8") as f:
    base_songs = json.load(f)

with open(NEW_JSON, "r", encoding="utf-8") as f:
    new_songs = json.load(f)

# Load caches if existing
banners = {}
if os.path.exists(BANNERS_CACHE):
    with open(BANNERS_CACHE, "r", encoding="utf-8") as f:
        banners = json.load(f)

covers = {}
if os.path.exists(COVERS_CACHE):
    with open(COVERS_CACHE, "r", encoding="utf-8") as f:
        covers = json.load(f)

# Function to query AniList or Kitsu for banner & poster
def fetch_anime_art(title):
    clean_title = title.split("(")[0].strip()
    
    # Try AniList GraphQL first
    query = """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        bannerImage
        coverImage { large }
        genres
        startDate { year }
        studios(isMain: true) { nodes { name } }
        description(asHtml: false)
      }
    }
    """
    try:
        payload = json.dumps({'query': query, 'variables': {'search': clean_title}}).encode('utf-8')
        req = urllib.request.Request(
            'https://graphql.anilist.co',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media = data.get('data', {}).get('Media')
            if media:
                b_img = media.get('bannerImage')
                c_img = media.get('coverImage', {}).get('large')
                studios = [s['name'] for s in media.get('studios', {}).get('nodes', [])]
                return {
                    'banner': b_img,
                    'cover': c_img,
                    'studio': studios[0] if studios else None,
                    'year': media.get('startDate', {}).get('year'),
                    'genres': media.get('genres', [])[:3]
                }
    except Exception as e:
        pass

    # Fallback to Kitsu API
    try:
        url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(clean_title)}&page[limit]=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                attr = items[0].get('attributes', {})
                cover_img = attr.get('coverImage', {})
                poster_img = attr.get('posterImage', {})
                return {
                    'banner': cover_img.get('large') or cover_img.get('original'),
                    'cover': poster_img.get('large') or poster_img.get('medium'),
                    'studio': None,
                    'year': attr.get('startDate', '')[:4] if attr.get('startDate') else None,
                    'genres': []
                }
    except Exception as e:
        pass

    return {'banner': None, 'cover': None, 'studio': None, 'year': None, 'genres': []}

# Fetch for the 25 new anime
for idx, s in enumerate(new_songs):
    name = s['anime']
    print(f"[{idx+1}/25] Buscando arte para: {name}...")
    art = fetch_anime_art(name)
    if art.get('cover'):
        s['image_url'] = art['cover']
        covers[name] = art['cover']
    if art.get('banner'):
        banners[name] = {
            'banner': art['banner'],
            'cover': art.get('cover'),
            'studio': art.get('studio'),
            'year': s['year'],
            'genres': s['tags'][:3]
        }
    time.sleep(0.4)

# Combine 75 + 25 = 100 songs
full_songs = base_songs + new_songs
for idx, s in enumerate(full_songs):
    s['id'] = idx + 1
    # Ensure image_url is populated from covers if missing
    if not s.get('image_url') and s['anime'] in covers:
        s['image_url'] = covers[s['anime']]

# Save updated anime_songs_verified.json (100 total songs!)
with open(BASE_JSON, "w", encoding="utf-8") as f:
    json.dump(full_songs, f, ensure_ascii=False, indent=2)

# Save updated caches
with open(COVERS_CACHE, "w", encoding="utf-8") as f:
    json.dump(covers, f, ensure_ascii=False, indent=2)

with open(BANNERS_CACHE, "w", encoding="utf-8") as f:
    json.dump(banners, f, ensure_ascii=False, indent=2)

print(f"\nSucesso! Total de músicas no catálogo: {len(full_songs)}")
print(f"Total de banners de cena em cache: {len(banners)}")
