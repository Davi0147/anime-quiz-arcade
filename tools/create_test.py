import subprocess
import time
import json
import urllib.request
import sys

# Test whether YT player allows playVideo
html_content = """<!DOCTYPE html>
<html>
<body>
  <div id="player"></div>
  <button id="pbtn" onclick="play()">PLAY</button>
  <div id="log">init</div>
  <script src="https://www.youtube.com/iframe_api"></script>
  <script>
    let p;
    function onYouTubeIframeAPIReady() {
      p = new YT.Player('player', {
        height: '200',
        width: '300',
        videoId: 'tkNfLYr-MyM',
        playerVars: { 'autoplay': 0, 'controls': 1 },
        events: {
          'onReady': () => { document.getElementById('log').innerText = 'READY'; },
          'onStateChange': (e) => { document.getElementById('log').innerText = 'STATE:' + e.data; }
        }
      });
    }
    function play() {
      if (p) p.playVideo();
    }
  </script>
</body>
</html>
"""

with open("C:/Users/luizd/.gemini/antigravity/scratch/test_api_headless.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved test_api_headless.html")
