import urllib.request
import urllib.parse
import json
import os
import time

DIR = "C:/Users/luizd/.gemini/antigravity/scratch/anime-music-quiz"
SCENES_PATH = os.path.join(DIR, "tools", "anime_scenes.json")
CACHE_PATH = os.path.join(DIR, "tools", "episode_screencaps_cache.json")

with open(SCENES_PATH, "r", encoding="utf-8") as f:
    scenes = json.load(f)

screencaps_cache = {}
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            screencaps_cache = json.load(f)
    except Exception:
        pass

used_urls = set()

def get_anilist_episode_thumbs(title):
    clean = title.split("(")[0].strip()
    query = """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        id
        title { romaji english }
        streamingEpisodes {
          title
          thumbnail
        }
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
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media = data.get('data', {}).get('Media', {})
            eps = media.get('streamingEpisodes', [])
            thumbs = [e['thumbnail'] for e in eps if e.get('thumbnail')]
            return thumbs
    except Exception as e:
        return []

def get_kitsu_episode_thumbs(title):
    clean = title.split("(")[0].strip()
    url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(clean)}&page[limit]=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                anime_id = items[0]['id']
                ep_url = f"https://kitsu.io/api/edge/episodes?filter[mediaId]={anime_id}&page[limit]=10"
                ep_req = urllib.request.Request(ep_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
                with urllib.request.urlopen(ep_req, timeout=8) as ep_resp:
                    ep_data = json.loads(ep_resp.read().decode('utf-8'))
                    eps = ep_data.get('data', [])
                    thumbs = []
                    for ep in eps:
                        t = ep.get('attributes', {}).get('thumbnail', {})
                        img = t.get('original') or t.get('large') or t.get('medium')
                        if img:
                            thumbs.append(img)
                    return thumbs
    except Exception as e:
        return []
    return []

print(f"Iniciando busca de capturas reais de episódios para {len(scenes)} animes...")

for idx, item in enumerate(scenes):
    name = item["anime"]
    chosen_thumb = screencaps_cache.get(name)

    if not chosen_thumb or chosen_thumb in used_urls:
        print(f"[{idx+1}/{len(scenes)}] Buscando frame real de episódio para: {name}...")
        # 1. Try AniList streaming episode thumbnails
        thumbs = get_anilist_episode_thumbs(name)
        time.sleep(0.4)

        # 2. Try Kitsu episode thumbnails if empty
        if not thumbs:
            thumbs = get_kitsu_episode_thumbs(name)
            time.sleep(0.4)

        # Pick a non-duplicate thumbnail (preferably episode 2 or 3 to avoid generic OP credit stills if possible)
        found = None
        for t in thumbs:
            if t not in used_urls:
                found = t
                break
        
        if found:
            chosen_thumb = found
            screencaps_cache[name] = chosen_thumb
            print(f"  -> OK! Frame de episódio encontrado: {chosen_thumb[:65]}...")
        else:
            # Fallback to existing if not found
            chosen_thumb = item.get("image_url")
            print(f"  -> Mantendo fallback para {name}")
    else:
        print(f"[{idx+1}/{len(scenes)}] {name} já em cache!")

    used_urls.add(chosen_thumb)
    item["image_url"] = chosen_thumb

# Save updated scenes and cache
with open(CACHE_PATH, "w", encoding="utf-8") as f:
    json.dump(screencaps_cache, f, ensure_ascii=False, indent=2)

with open(SCENES_PATH, "w", encoding="utf-8") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)

print("\nProcesso finalizado com sucesso!")
print(f"Total de cenas salvas: {len(scenes)}")
print(f"Total de URLs distintas: {len(used_urls)}")
