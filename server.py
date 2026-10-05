import http.server
import socketserver
import webbrowser
import os
import sys
import re

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

class RangeFileWrapper:
    def __init__(self, file_obj, length):
        self.file_obj = file_obj
        self.remaining = length

    def read(self, size=-1):
        if self.remaining <= 0:
            return b""
        if size < 0 or size > self.remaining:
            size = self.remaining
        chunk = self.file_obj.read(size)
        self.remaining -= len(chunk)
        return chunk

    def close(self):
        self.file_obj.close()

class QuietRangeHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Keep terminal clean, only log non-200/206 if error
        pass

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()

        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        total_length = fs.st_size

        range_header = self.headers.get('Range')
        if not range_header or not range_header.startswith('bytes='):
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Length", str(total_length))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            return f

        match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            self.send_error(416, "Requested Range Not Satisfiable")
            f.close()
            return None

        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else total_length - 1

        if start >= total_length:
            self.send_error(416, "Requested Range Not Satisfiable")
            f.close()
            return None

        end = min(end, total_length - 1)
        length = end - start + 1

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{total_length}")
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        f.seek(start)
        return RangeFileWrapper(f, length)

if __name__ == '__main__':
    ports = [8000, 8080, 8081, 8888, 5000]
    httpd = None
    selected_port = None

    for port in ports:
        try:
            httpd = socketserver.TCPServer(("", port), QuietRangeHandler)
            selected_port = port
            break
        except OSError:
            continue

    if not httpd:
        print("ERRO: Nenhuma porta disponivel!")
        input("Pressione Enter para sair...")
        sys.exit(1)

    url = f"http://localhost:{selected_port}/desafio_anime_quiz.html"

    print("=" * 60)
    print(f"  DESAFIO DE ABERTURAS & CENAS DE ANIMES (v2.2.0)")
    print("=" * 60)
    print(f"\n[OK] Servidor com suporte a Range Requests rodando na porta {selected_port}!")
    print(f"[OK] Pasta: {DIR}")
    print(f"[OK] Abrindo: {url}\n")
    print("Mantenha esta janela aberta enquanto joga.")
    print("Para encerrar, feche esta janela ou pressione Ctrl + C.\n")

    webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

