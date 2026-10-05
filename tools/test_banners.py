import urllib.request
import json

query = """
query ($search: String) {
  Media (search: $search, type: ANIME) {
    id
    title { romaji english }
    bannerImage
    coverImage { large }
  }
}
"""
for name in ['Death Note', 'Attack on Titan', 'Spy x Family', 'Jujutsu Kaisen', 'Chainsaw Man']:
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=json.dumps({'query': query, 'variables': {'search': name}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            media = res['data']['Media']
            print(name, '-> Banner:', media.get('bannerImage'))
    except Exception as e:
        print(name, 'Error:', e)
