import socket
import json
import urllib.request
import time
import subprocess
import base64
import os

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--headless=new",
    "file:///C:/Users/luizd/.gemini/antigravity/scratch/test_yt.html"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    res = urllib.request.urlopen("http://localhost:9222/json")
    targets = json.loads(res.read().decode('utf-8'))
    page = next(t for t in targets if 'test_yt.html' in t.get('url', ''))
    ws_url = page['webSocketDebuggerUrl']
    
    from urllib.parse import urlparse
    parsed = urlparse(ws_url)
    host = parsed.hostname
    port = parsed.port
    path = parsed.path
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: localhost:{port}\r\n"
        f"Origin: http://localhost:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode('utf-8'))
    resp = s.recv(4096).decode('utf-8', errors='ignore')
    print("Handshake:", resp.splitlines()[0])
    
    def send_ws_frame(msg):
        payload = msg.encode('utf-8')
        length = len(payload)
        frame = bytearray()
        frame.append(0x81)
        if length < 126:
            frame.append(0x80 | length)
        elif length < 65536:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, 'big'))
        else:
            frame.append(0x80 | 127)
            frame.extend(length.to_bytes(8, 'big'))
        mask = b'\x12\x34\x56\x78'
        frame.extend(mask)
        masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        s.sendall(frame)

    def read_ws_frame():
        header = s.recv(2)
        if not header: return None
        length = header[1] & 0x7F
        if length == 126:
            length = int.from_bytes(s.recv(2), 'big')
        elif length == 127:
            length = int.from_bytes(s.recv(8), 'big')
        data = s.recv(length)
        return data.decode('utf-8', errors='ignore')

    send_ws_frame(json.dumps({"id": 1, "method": "Runtime.enable"}))
    send_ws_frame(json.dumps({"id": 2, "method": "Console.enable"}))
    
    # Wait 3s for YT player to be ready
    time.sleep(3)
    
    # Click button
    send_ws_frame(json.dumps({
        "id": 3,
        "method": "Runtime.evaluate",
        "params": {"expression": "document.getElementById('btn').click(); document.getElementById('status').textContent"}
    }))
    
    time.sleep(2)
    
    send_ws_frame(json.dumps({
        "id": 4,
        "method": "Runtime.evaluate",
        "params": {"expression": "document.getElementById('status').textContent"}
    }))
    
    s.settimeout(3.0)
    while True:
        try:
            msg = read_ws_frame()
            if not msg: break
            parsed = json.loads(msg)
            if parsed.get('id') in [3, 4]:
                val = parsed.get('result', {}).get('result', {}).get('value')
                print(f"Status (msg {parsed.get('id')}):", val)
            elif parsed.get('method') == 'Runtime.consoleAPICalled':
                print("LOG:", parsed.get('params', {}).get('args'))
        except socket.timeout:
            break
finally:
    proc.terminate()
