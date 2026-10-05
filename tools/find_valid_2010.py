import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

queries = [
    ("Angel Beats", "Lia My Soul Your Beats official opening"),
    ("Durarara!!", "Durarara Uragiri no Yuuyake opening"),
    ("Bleach 2010", "Bleach Ranbu no Melody opening"),
    ("K-ON!!", "K-ON GO GO MANIAC opening")
]

for title, q in queries:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:5]
    for v in vids:
        try:
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json"
            res = json.loads(urllib.request.urlopen(urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8'))
            print(f"FOUND VALID: {title} | ID: {v} | Title: {res.get('title')}")
            break
        except Exception as e:
            pass
