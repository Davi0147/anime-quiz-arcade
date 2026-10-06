import threading
import http.client
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

# Import server handler
from server import QuietRangeHandler
import socketserver

PORT = 8999

class TestServer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.httpd = socketserver.TCPServer(("", PORT), QuietRangeHandler)

    def run(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()

server = TestServer()
server.start()
time.sleep(0.3)

try:
    conn = http.client.HTTPConnection("localhost", PORT)
    # Test 1: GET index.html
    conn.request("GET", "/index.html")
    res1 = conn.getresponse()
    print(f"GET /index.html Status: {res1.status} (Expected: 200)")
    assert res1.status == 200
    res1.read(100)

    # Test 2: Range request (bytes=0-49)
    conn.request("GET", "/index.html", headers={"Range": "bytes=0-49"})
    res2 = conn.getresponse()
    print(f"GET /index.html with Range bytes=0-49 Status: {res2.status} (Expected: 206)")
    assert res2.status == 206
    assert res2.getheader("Content-Range") is not None
    print(f"Content-Range Header: {res2.getheader('Content-Range')}")
    body = res2.read()
    assert len(body) == 50
    print(f"Range chunk size received: {len(body)} bytes")
    print("✅ Teste do servidor de streaming com Range headers concluído com sucesso!")
finally:
    server.shutdown()
