import urllib.request

vid = "yu0HjPzFYnY"
req = urllib.request.Request(f"https://www.youtube.com/embed/{vid}", headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://google.com'})
html = urllib.request.urlopen(req).read().decode('utf-8')
print("Status yu0HjPzFYnY:", "OK" if "status\":\"ERROR\"" not in html and "unavailable" not in html.lower() else "FAIL")
