import subprocess
import time
import json
import urllib.request
import asyncio

# Connect via websocket to chrome devtools
import urllib.request

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--remote-debugging-port=9222",
    "--headless=new",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_yt.html"
]

proc = subprocess.Popen(cmd)
time.sleep(3)

try:
    res = urllib.request.urlopen("http://localhost:9222/json")
    targets = json.loads(res.read().decode('utf-8'))
    page = next(t for t in targets if 'test_yt.html' in t.get('url', ''))
    ws_url = page['webSocketDebuggerUrl']
    print("WebSocket URL:", ws_url)
finally:
    proc.terminate()
