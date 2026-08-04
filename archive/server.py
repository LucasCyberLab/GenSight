#!/usr/bin/env python3
"""元晟传媒工作台轻量协同服务器：静态文件 + 共享 data.json API。"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data.json"

DEFAULT_DATA = {
    "version": 2,
    "updatedAt": None,
    "updatedBy": None,
    "prep": {},
    "daily": {},
    "week": {},
    "foundation": {},
    "foundationNote": "",
    "inquiries": [],
    "reviews": [],
    "handoffs": [],
    "handoffSeq": 0,
    "workItems": [],
    "workItemSeq": 0,
    "recentDocs": [],
    "finalizedAssets": [],
}


def read_data() -> dict:
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULT_DATA)


def write_data(data: dict) -> None:
    tmp = DATA_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    tmp.replace(DATA_FILE)


class GensightHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def guess_type(self, path: str) -> str:
        if path.lower().endswith(".md"):
            return "text/markdown; charset=utf-8"
        ctype = super().guess_type(path)
        if ctype.startswith("text/") and "charset=" not in ctype:
            return f"{ctype}; charset=utf-8"
        return ctype

    def do_GET(self) -> None:
        clean_path = self.path.split("?", 1)[0]
        if clean_path == "/api/data":
            self._serve_data()
            return
        # 工作台 JS 读取文档：/api/doc?file=xxx.md（始终返回正文，不被浏览器导航逻辑干扰）
        if clean_path == "/api/doc":
            self._serve_doc_api()
            return
        if clean_path.endswith(".md"):
            # 浏览器地址栏打开 .md → 跳文档库阅读器；JS fetch → 返回 Markdown 正文
            if self._is_browser_navigation():
                self._redirect_markdown(clean_path)
                return
            super().do_GET()
            return
        super().do_GET()

    def _serve_doc_api(self) -> None:
        from urllib.parse import parse_qs, unquote, urlparse

        query = parse_qs(urlparse(self.path).query)
        raw_name = (query.get("file") or [""])[0].strip()
        filename = unquote(raw_name).lstrip("/")
        if not filename.endswith(".md") or ".." in filename or filename.startswith("/"):
            self.send_error(400, "Invalid markdown file")
            return
        target = (ROOT / filename).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            self.send_error(403, "Forbidden")
            return
        if not target.is_file():
            self.send_error(404, "File not found")
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/markdown; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _is_browser_navigation(self) -> bool:
        mode = (self.headers.get("Sec-Fetch-Mode") or "").lower()
        if mode == "navigate":
            return True
        if mode in {"cors", "same-origin", "no-cors"}:
            return False
        accept = self.headers.get("Accept") or ""
        first = accept.split(",", 1)[0].strip().lower()
        return first.startswith("text/html")

    def _redirect_markdown(self, path: str) -> None:
        """浏览器直接打开 .md 时重定向到工作台文档库，避免裸显示乱码。"""
        filename = path.lstrip("/")
        target = f"/?doc={filename}"
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()

    def do_PUT(self) -> None:
        if self.path.split("?", 1)[0] == "/api/data":
            self._save_data()
            return
        self.send_error(404, "Not Found")

    def _serve_data(self) -> None:
        self._send_json(read_data())

    def _save_data(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            incoming = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        data = {
            "version": 2,
            "updatedAt": datetime.now(timezone.utc).isoformat(),
            "updatedBy": incoming.get("clientId", "unknown"),
            "prep": incoming.get("prep", {}),
            "daily": incoming.get("daily", {}),
            "week": incoming.get("week", {}),
            "foundation": incoming.get("foundation", {}),
            "foundationNote": incoming.get("foundationNote", ""),
            "inquiries": incoming.get("inquiries", []),
            "reviews": incoming.get("reviews", []),
            "handoffs": incoming.get("handoffs", []),
            "handoffSeq": incoming.get("handoffSeq", 0),
            "workItems": incoming.get("workItems", []),
            "workItemSeq": incoming.get("workItemSeq", 0),
            "recentDocs": incoming.get("recentDocs", []),
            "finalizedAssets": incoming.get("finalizedAssets", []),
        }
        write_data(data)
        self._send_json(data)

    def _send_json(self, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        if args and str(args[0]).startswith("GET /api/"):
            return
        if args and str(args[0]).startswith("PUT /api/"):
            return
        super().log_message(fmt, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description="元晟传媒工作台协同服务器")
    parser.add_argument("--port", type=int, default=8025)
    parser.add_argument("--bind", default="0.0.0.0", help="0.0.0.0 允许局域网访问")
    args = parser.parse_args()

    if not DATA_FILE.exists():
        write_data(dict(DEFAULT_DATA))

    server = HTTPServer((args.bind, args.port), GensightHandler)
    print("元晟传媒工作台已启动")
    print(f"  本机访问:   http://localhost:{args.port}")
    print(f"  局域网访问: http://<你的IP>:{args.port}")
    print(f"  共享数据:   {DATA_FILE}")
    print("  按 Ctrl+C 停止")
    server.serve_forever()


if __name__ == "__main__":
    main()
