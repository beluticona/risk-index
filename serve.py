from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import os


ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data"


class ExplorerHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed_path = unquote(urlparse(path).path)
        if parsed_path.startswith("/data/"):
            return str(DATA_ROOT / parsed_path.removeprefix("/data/"))
        if parsed_path == "/":
            return str(ROOT / "index.html")
        return str(ROOT / parsed_path.lstrip("/"))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    port = int(os.environ.get("PORT", "8010"))
    server = ThreadingHTTPServer(("127.0.0.1", port), ExplorerHandler)
    print(f"Serving LT4CR Risk Index Explorer at http://127.0.0.1:{port}/")
    print(f"Data root: {DATA_ROOT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
