import urllib.request
import json

cands = ["p65nNUgyQ7g", "L1FdEBTJXus", "1oMxrHXzOsY", "o6zeTU-iJTI", "Th7MAZYFIMc", "kpKaA1IajR4"]

for c in cands:
    try:
        req = urllib.request.Request(f"https://www.youtube.com/embed/{c}", headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        if 'status":"ERROR"' not in html and 'unavailable' not in html.lower():
            print(f"OK: {c}")
            break
        else:
            print(f"Blocked: {c}")
    except Exception as e:
        print(f"Error {c}: {e}")
