import urllib.request
import urllib.parse
import re

queries = [
    "Porno Graffitti THE DAY official audio",
    "THE DAY Porno Graffitti topic",
    "My Hero Academia OP 1 TV size audio",
    "THE DAY Boku no Hero Academia audio"
]

found = []
for q in queries:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
    vids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))[:6]
    for v in vids:
        try:
            req = urllib.request.Request(f"https://www.youtube.com/embed/{v}", headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})
            h = urllib.request.urlopen(req).read().decode('utf-8')
            if 'status":"ERROR"' not in h and 'unavailable' not in h.lower():
                print(f"FOUND WORKING: {v} for query '{q}'")
                found.append(v)
                break
        except:
            pass
    if found:
        break

if not found:
    print("None found in initial queries")
