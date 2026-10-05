import subprocess
import time
import urllib.request

html = """<!DOCTYPE html>
<html>
<body>
  <iframe id="f" width="300" height="200" src="https://www.youtube.com/embed/tkNfLYr-MyM?enablejsapi=1&autoplay=1" allow="autoplay"></iframe>
  <button id="p" onclick="pause()">PAUSE</button>
  <button id="r" onclick="resume()">PLAY</button>
  <script>
    function pause() {
      document.getElementById('f').contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
    }
    function resume() {
      document.getElementById('f').contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
    }
  </script>
</body>
</html>
"""

with open("C:/Users/luizd/.gemini/antigravity/scratch/test_postmessage.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Created test_postmessage.html")
