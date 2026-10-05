import urllib.request
import urllib.parse
import re
import json

q = "Highschool of the Dead opening full official audio"
url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:10]

for v in vids:
    try:
        data = json.loads(urllib.request.urlopen(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json").read().decode('utf-8'))
        print(v, "|", data.get("title"))
        break
    except:
        pass
