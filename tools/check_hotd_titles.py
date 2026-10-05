import urllib.request
import json

for v in ["H0mCytVZQiY", "9z8wDkSz-tY", "M8tRBup0j9E", "8bZ31JmC6b8"]:
    try:
        data = json.loads(urllib.request.urlopen(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json").read().decode('utf-8'))
        print(v, "|", data.get("title"))
    except Exception as e:
        print(v, "error:", e)
