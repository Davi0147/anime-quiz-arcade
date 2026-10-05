import urllib.request
import json
import re

vid = "yu0HjPzFYnY"
req = urllib.request.Request(f"https://www.youtube.com/embed/{vid}", headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Search for playabilityStatus in ytInitialPlayerResponse
status_match = re.search(r'"playabilityStatus":\{"status":"([^"]+)"', html)
if status_match:
    print(f"Status for {vid}: {status_match.group(1)}")
else:
    print(f"playabilityStatus not matched directly, status:\"ERROR\" present? {'status\":\"ERROR\"' in html}")
