from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from urllib.parse import unquote, urlparse
import os

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / "data"


class ExplorerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = unquote(urlparse(self.path).path)

        if parsed_path == "/data/Final_Index.csv":
            self._serve_csv()
        elif parsed_path == "/" or parsed_path == "/index.html":
            self._serve_file(ROOT / "index.html", "text/html")
        else:
            local = ROOT / parsed_path.lstrip("/")
            if local.exists() and local.is_file():
                self._serve_file(local)
            else:
                self.send_error(404)

    def _serve_csv(self):
        """Convert Final_Index.xlsx → CSV on-the-fly for local dev."""
        xlsx = DATA_ROOT / "Final_Index.xlsx"
        if not xlsx.exists():
            self.send_error(404, f"Data file not found: {xlsx}")
            return
        try:
            import pandas as pd
            df = pd.read_excel(xlsx, sheet_name="original_index")
            buf = StringIO()
            df.to_csv(buf, index=False)
            content = buf.getvalue().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(content)
        except Exception as exc:
            self.send_error(500, str(exc))

    def _serve_file(self, path: Path, content_type: str = None):
        suffix_map = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
        }
        ct = content_type or suffix_map.get(path.suffix, "application/octet-stream")
        try:
            content = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(content)
        except OSError:
            self.send_error(404)

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")


def main():
    port = int(os.environ.get("PORT", "8010"))
    server = ThreadingHTTPServer(("127.0.0.1", port), ExplorerHandler)
    print(f"LT4CR Risk Index Explorer  →  http://127.0.0.1:{port}/")
    print(f"Data: {DATA_ROOT / 'Final_Index.xlsx'}")
    print("Ctrl-C to stop")
    server.serve_forever()


if __name__ == "__main__":
    main()
