import urllib.request
import urllib.parse
import json

test_animes = ['Naruto', 'One Piece', 'Hunter x Hunter', 'Death Note', 'Bleach', 'Dragon Ball']

for name in test_animes:
    url = f"https://kitsu.io/api/edge/anime?filter[text]={urllib.parse.quote(name)}&page[limit]=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.api+json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('data', [])
            if items:
                attr = items[0].get('attributes', {})
                cover = attr.get('coverImage', {})
                print(name, '-> Kitsu Scene Banner:', cover.get('large') or cover.get('original'))
    except Exception as e:
        print(name, 'Error:', e)
