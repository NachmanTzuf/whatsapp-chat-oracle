"""
WhatsApp Chat Oracle - Live Multimodal Backend & Static Server
Serves the editorial web publication on http://localhost:8089 and provides
POST /api/analyze to unpack uploaded .zip/.txt files, transcribe .opus/.ogg/.m4a
voice recordings with faster-whisper, analyze .jpg/.png photos with Pillow,
and return the complete narrative dossier JSON.
"""

import os
import sys
import json
import shutil
import tempfile
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
sys.path.insert(0, BASE_DIR)

from parser import WhatsAppParser
from analytics import ChatAnalytics
from interviewer import InterviewerEngine

# Pre-initialize parser with cached faster-whisper base model for instant transcription
print("[Server] Initializing Multimodal WhatsApp Parser (faster-whisper 'base' + PIL Forensics)...")
GLOBAL_PARSER = WhatsAppParser(transcribe_audio=True, model_size="base")
print("[Server] Multimodal Parser ready.")


class OracleRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Filename")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path.startswith("/api/analyze"):
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length <= 0:
                    self._send_json(400, {"error": "Empty upload payload."})
                    return

                raw_filename = self.headers.get("X-Filename", "uploaded_chat.zip")
                filename = urllib.parse.unquote(raw_filename)
                body = self.rfile.read(content_length)

                tmp_dir = tempfile.mkdtemp(prefix="wa_oracle_")
                try:
                    upload_path = os.path.join(tmp_dir, filename)
                    with open(upload_path, "wb") as f:
                        f.write(body)

                    extract_dir = os.path.join(tmp_dir, "extracted")
                    parsed = GLOBAL_PARSER.parse_archive(upload_path, extract_dir=extract_dir)
                    analytics = ChatAnalytics(parsed["messages"]).run_full_analysis()
                    script = InterviewerEngine(analytics).generate_full_interviewer_script()

                    bundle = {
                        "source": filename,
                        "analytics": analytics,
                        "interviewer_script": script
                    }

                    # Persist latest analysis to web/data.json
                    with open(os.path.join(WEB_DIR, "data.json"), "w", encoding="utf-8") as df:
                        json.dump(bundle, df, ensure_ascii=False, indent=2)

                    self._send_json(200, bundle)
                finally:
                    shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "Endpoint not found."})

    def _send_json(self, status_code: int, payload: dict):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class OracleServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def run_server(port: int = 8089):
    server = OracleServer(("0.0.0.0", port), OracleRequestHandler)
    print(f"[Server] WhatsApp Chat Oracle running at http://localhost:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    port_num = int(sys.argv[1]) if len(sys.argv) > 1 else 8089
    run_server(port_num)
