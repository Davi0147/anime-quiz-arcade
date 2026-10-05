import urllib.request
import urllib.parse
import json
import time
import os

CACHE_FILE = "tools/anime_covers_cache.json"

CUSTOM_SEARCH_MAP = {
    "Attack on Titan (Shingeki no Kyojin)": "Attack on Titan",
    "Attack on Titan Final Season Pt 2": "Attack on Titan: The Final Season Part 2",
    "Boku no Hero Academia S2": "My Hero Academia 2",
    "Boku no Hero Academia": "My Hero Academia",
    "Jujutsu Kaisen S2 (Shibuya)": "Jujutsu Kaisen 2nd Season",
    "Kimetsu no Yaiba (Demon Slayer)": "Demon Slayer: Kimetsu no Yaiba",
    "Your Lie in April (Shigatsu wa Kimi no Uso)": "Your Lie in April",
    "Mashle: Magic and Muscles S2": "Mashle 2nd Season",
    "Rosario + Vampire": "Rosario to Vampire",
    "Fate/stay night": "Fate/stay night",
    "Fate/Zero": "Fate/Zero",
    "IS: Infinite Stratos": "Infinite Stratos",
    "Kaiju No. 8": "Kaiju No. 8",
    "Sora no Otoshimono": "Sora no Otoshimono",
    "To LOVE-Ru Darkness": "To Love-Ru Darkness",
    "Trinity Seven": "Trinity Seven",
    "Gakusen Toshi Asterisk": "The Asterisk War",
    "Rakudai Kishi no Cavalry": "Chivalry of a Failed Knight",
    "Monster Musume no Iru Nichijou": "Monster Musume",
}

def get_kitsu_poster(title):
    search_q = CUSTOM_SEARCH_MAP.get(title) or title.split("(")[0].strip()
    url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(search_q)}&page[limit]=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': 'application/vnd.api+json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                poster = items[0].get('attributes', {}).get('posterImage', {})
                img = poster.get('large') or poster.get('original') or poster.get('medium')
                if img:
                    return img
    except Exception as e:
        print(f"Error {title}: {e}")
    return None

def main():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)

    with open('anime_songs_verified.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)

    unique_animes = sorted(list(set(s['anime'] for s in songs)))
    print(f"Total unique animes: {len(unique_animes)}")

    for i, anime in enumerate(unique_animes):
        if anime in cache and cache[anime]:
            print(f"[{i+1}/{len(unique_animes)}] (Cached) {anime} -> {cache[anime][:60]}...")
            continue
        print(f"[{i+1}/{len(unique_animes)}] Fetching {anime} via Kitsu...")
        img = get_kitsu_poster(anime)
        if not img and "(" in anime:
            alt = anime.split("(")[1].replace(")", "").strip()
            print(f"  Trying alternative '{alt}'...")
            img = get_kitsu_poster(alt)
        
        if img:
            cache[anime] = img
            print(f"  -> Found: {img}")
        else:
            print(f"  -> FAILED to find cover for '{anime}'")
        time.sleep(0.15)

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    missing = [a for a in unique_animes if not cache.get(a)]
    if missing:
        print("Still missing:", missing)
    else:
        print("ALL 73 ANIMES HAVE HIGH-QUALITY COVERS!")

    # Update anime_songs_verified.json
    for s in songs:
        s['image_url'] = cache.get(s['anime'], '')

    with open('anime_songs_verified.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print("anime_songs_verified.json successfully updated!")

if __name__ == '__main__':
    main()
