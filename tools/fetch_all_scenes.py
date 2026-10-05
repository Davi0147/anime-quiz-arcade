import json
import urllib.request
import urllib.parse
import os
import time

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
SONGS_PATH = os.path.join(DIR, "anime_songs_verified.json")
BANNERS_CACHE = os.path.join(DIR, "tools", "anime_banners_cache.json")
SCENES_PATH = os.path.join(DIR, "tools", "anime_scenes.json")

with open(SONGS_PATH, "r", encoding="utf-8") as f:
    songs = json.load(f)

banners = {}
if os.path.exists(BANNERS_CACHE):
    with open(BANNERS_CACHE, "r", encoding="utf-8") as f:
        banners = json.load(f)

# Group songs by canonical anime name
anime_dict = {}
for s in songs:
    name = s["anime"]
    if name not in anime_dict:
        anime_dict[name] = {
            "anime": name,
            "year": s.get("year", 2000),
            "tags": s.get("tags", []),
            "synonyms": s.get("synonyms", [name.lower()]),
            "hint": s.get("hint", " / ".join(s.get("tags", []))),
            "cover": s.get("image_url", ""),
            "scene_url": ""
        }

print(f"Total de animes únicos para buscar cenas/frames: {len(anime_dict)}")

def fetch_scene_frame(title):
    clean = title.split("(")[0].strip()
    # 1. Kitsu API coverImage (usually 16:9 cinematic landscape)
    try:
        url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(clean)}&page[limit]=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                attr = items[0].get('attributes', {})
                cover = attr.get('coverImage', {})
                img = cover.get('large') or cover.get('original')
                if img:
                    return img
    except Exception:
        pass

    # 2. AniList GraphQL bannerImage
    query = """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        bannerImage
      }
    }
    """
    try:
        payload = json.dumps({'query': query, 'variables': {'search': clean}}).encode('utf-8')
        req = urllib.request.Request(
            'https://graphql.anilist.co',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media = data.get('data', {}).get('Media')
            if media and media.get('bannerImage'):
                return media['bannerImage']
    except Exception:
        pass

    return ""

scene_list = []
for idx, (name, info) in enumerate(anime_dict.items()):
    # Check if banner already in cache
    banner_img = ""
    if name in banners and banners[name].get('banner'):
        banner_img = banners[name]['banner']
    
    if not banner_img:
        print(f"[{idx+1}/{len(anime_dict)}] Buscando cena online para '{name}'...")
        banner_img = fetch_scene_frame(name)
        if banner_img:
            banners[name] = banners.get(name, {})
            banners[name]['banner'] = banner_img
            print(f"  -> Sucesso: {banner_img[:60]}...")
        else:
            print(f"  -> Não encontrado direto. Usando poster com corte cinematográfico.")
        time.sleep(0.3)
    else:
        print(f"[{idx+1}/{len(anime_dict)}] '{name}' já em cache!")

    # If banner_img exists use it, otherwise use cover
    final_scene = banner_img if banner_img else info['cover']

    scene_list.append({
        "id": len(scene_list) + 1,
        "anime": name,
        "image_url": final_scene,
        "has_cinematic_banner": bool(banner_img),
        "year": info["year"],
        "tags": info["tags"],
        "synonyms": info["synonyms"],
        "hint": info["hint"]
    })

# Save caches
with open(BANNERS_CACHE, "w", encoding="utf-8") as f:
    json.dump(banners, f, ensure_ascii=False, indent=2)

with open(SCENES_PATH, "w", encoding="utf-8") as f:
    json.dump(scene_list, f, ensure_ascii=False, indent=2)

total_cinematic = sum(1 for s in scene_list if s["has_cinematic_banner"])
print(f"\nFinalizado! Total de cenas montadas: {len(scene_list)}")
print(f"Cenas com frames 16:9 cinematográficos: {total_cinematic} / {len(scene_list)}")
