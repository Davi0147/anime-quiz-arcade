import subprocess
import time
import urllib.request
import json

# Start chrome and check if audio is playing using chrome media indicators
# Chrome exposes media session info in devtools
cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--autoplay-policy=no-user-gesture-required",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_masked_play.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    res = urllib.request.urlopen("http://127.0.0.1:9222/json")
    targets = json.loads(res.read().decode('utf-8'))
    print("Chrome targets:", [t['url'] for t in targets])
finally:
    proc.terminate()
