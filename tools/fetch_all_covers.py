import urllib.request
import json
import time
import os

CACHE_FILE = "tools/anime_covers_cache.json"

CUSTOM_SEARCH_MAP = {
    "Attack on Titan (Shingeki no Kyojin)": "Shingeki no Kyojin",
    "Attack on Titan Final Season Pt 2": "Shingeki no Kyojin: The Final Season Part 2",
    "Boku no Hero Academia S2": "Boku no Hero Academia 2nd Season",
    "Jujutsu Kaisen S2 (Shibuya)": "Jujutsu Kaisen 2nd Season",
    "Kimetsu no Yaiba (Demon Slayer)": "Kimetsu no Yaiba",
    "Your Lie in April (Shigatsu wa Kimi no Uso)": "Shigatsu wa Kimi no Uso",
    "Mashle: Magic and Muscles S2": "Mashle: Kami Shinkakusha Kouho Senbatsu Shiken-hen",
    "Rosario + Vampire": "Rosario to Vampire",
    "Fate/stay night": "Fate/stay night",
    "IS: Infinite Stratos": "Infinite Stratos",
}

query = """
query ($search: String) {
  Media (search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    coverImage {
      extraLarge
      large
      medium
    }
  }
}
"""

def fetch_cover_from_anilist(search_term):
    url = 'https://graphql.anilist.co'
    payload = json.dumps({'query': query, 'variables': {'search': search_term}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            media = res.get('data', {}).get('Media')
            if media and media.get('coverImage'):
                return (
                    media['coverImage'].get('extraLarge') or
                    media['coverImage'].get('large') or
                    media['coverImage'].get('medium')
                )
    except Exception as e:
        print(f"Error fetching '{search_term}': {e}")
    return None

def main():
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    with open('anime_songs_verified.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)

    unique_animes = sorted(list(set(s['anime'] for s in songs)))
    print(f"Total unique animes to process: {len(unique_animes)}")

    updated = False
    for i, anime in enumerate(unique_animes):
        if anime in cache and cache[anime]:
            continue
        
        search_query = CUSTOM_SEARCH_MAP.get(anime)
        if not search_query:
            search_query = anime.split("(")[0].strip()

        print(f"[{i+1}/{len(unique_animes)}] Fetching cover for '{anime}' (query: '{search_query}')...")
        cover_url = fetch_cover_from_anilist(search_query)
        if not cover_url and "(" in anime:
            # Fallback to text inside parentheses
            alt = anime.split("(")[1].replace(")", "").strip()
            print(f"  Trying alternative '{alt}'...")
            cover_url = fetch_cover_from_anilist(alt)

        if cover_url:
            cache[anime] = cover_url
            print(f"  -> Found: {cover_url}")
            updated = True
        else:
            print(f"  -> FAILED to find cover for '{anime}'")
        
        time.sleep(0.3)

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    # Now verify all songs have image_url
    missing = [a for a in unique_animes if not cache.get(a)]
    print("\n--- Summary ---")
    print(f"Cached covers: {len(cache)} / {len(unique_animes)}")
    if missing:
        print("Missing covers for:", missing)
    else:
        print("All 73 unique animes have covers!")

    # Update anime_songs_verified.json with image_url
    for s in songs:
        s['image_url'] = cache.get(s['anime'], '')

    with open('anime_songs_verified.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print("Successfully updated anime_songs_verified.json with image_url!")

if __name__ == '__main__':
    main()
