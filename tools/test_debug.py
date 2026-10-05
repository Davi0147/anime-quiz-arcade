import subprocess
import time
import json
import urllib.request

# Start chrome with remote debugging
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--remote-debugging-port=9222",
    "--headless=new",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_yt.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    # Query devtools targets
    res = urllib.request.urlopen("http://localhost:9222/json")
    targets = json.loads(res.read().decode('utf-8'))
    print("DevTools targets:", len(targets))
    for t in targets:
        print(t.get('title'), t.get('url'))
finally:
    proc.terminate()
