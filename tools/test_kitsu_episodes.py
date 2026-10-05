import urllib.request
import urllib.parse
import json

test_animes = ['Cowboy Bebop', 'Neon Genesis Evangelion', 'InuYasha', 'Fullmetal Alchemist', 'Steins;Gate']

for name in test_animes:
    # 1. Search anime ID in Kitsu
    url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(name)}&page[limit]=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                anime_id = items[0]['id']
                # 2. Fetch episodes
                ep_url = f"https://kitsu.io/api/edge/episodes?filter[mediaId]={anime_id}&page[limit]=5"
                ep_req = urllib.request.Request(ep_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
                with urllib.request.urlopen(ep_req, timeout=5) as ep_resp:
                    ep_data = json.loads(ep_resp.read().decode('utf-8'))
                    eps = ep_data.get('data', [])
                    for ep in eps:
                        thumb = ep.get('attributes', {}).get('thumbnail', {})
                        img = thumb.get('original') or thumb.get('large')
                        if img:
                            print(name, '-> Kitsu Episode Frame:', img)
                            break
    except Exception as e:
        print(name, 'error:', e)
