import subprocess
import time
import json
import urllib.request
import re

# Test if Chrome with test_masked_play.html actually starts audio
html_test = """<!DOCTYPE html>
<html>
<body>
  <div id="status">not clicked</div>
  <iframe id="f" width="300" height="200" allow="autoplay; encrypted-media"></iframe>
  <button id="b" onclick="go()">GO</button>
  <script>
    function go() {
      document.getElementById('status').innerText = 'clicked';
      document.getElementById('f').src = 'https://www.youtube.com/embed/tkNfLYr-MyM?autoplay=1';
    }
  </script>
</body>
</html>
"""

with open("C:/Users/luizd/.gemini/antigravity/scratch/test_autoplay_check.html", "w", encoding="utf-8") as f:
    f.write(html_test)

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9333",
    "--remote-allow-origins=*",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_autoplay_check.html"
]

p = subprocess.Popen(cmd)
time.sleep(2)

try:
    res = urllib.request.urlopen("http://127.0.0.1:9333/json")
    targets = json.loads(res.read().decode('utf-8'))
    print("Targets:", len(targets))
    for t in targets:
        print(t.get('title'), t.get('url'))
finally:
    p.terminate()
