import subprocess
import time
import json
import urllib.request
import urllib.error

# We can use websocket-client or simple script to evaluate JS
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--remote-debugging-port=9222",
    "--headless=new",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_yt.html"
]

proc = subprocess.Popen(cmd)
time.sleep(3)

try:
    import urllib.request
    res = urllib.request.urlopen("http://localhost:9222/json")
    targets = json.loads(res.read().decode('utf-8'))
    page = next(t for t in targets if 'test_yt.html' in t.get('url', ''))
    
    # We can connect using python websockets or just write a small script
    print("Page found:", page['title'])
finally:
    proc.terminate()
