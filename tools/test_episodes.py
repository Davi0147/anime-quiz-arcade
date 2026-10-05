import urllib.request
import json
import time

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

for name in ['Naruto', 'Death Note', 'Attack on Titan', 'Fate/Zero', 'Bleach']:
    payload = json.dumps({'query': query, 'variables': {'search': name}}).encode('utf-8')
    req = urllib.request.Request('https://graphql.anilist.co', data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media = data.get('data', {}).get('Media', {})
            eps = media.get('streamingEpisodes', [])
            print(name, '-> Episodes thumbnails count:', len(eps))
            if eps:
                print('   Sample thumb:', eps[0].get('thumbnail'))
    except Exception as e:
        print(name, 'error:', e)
    time.sleep(0.5)
