"""A local stand-in for the 发信助手 web app, for page_test.py.

Speaks the SPEC.md contract (ping / enqueue / status / cancel / test, fetch form and HTML form
fallback, GET status) on 127.0.0.1 and records every request. It sends nothing.
"""

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ADDR_RE = re.compile(r"^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]{2,}$")
PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{0,80}\]")
PATH = "/macros/s/AKfake/exec"


class MockSender:
    def __init__(self, token):
        self.token = token
        self.requests = []  # {"method", "via": "fetch"|"form"|"get"|"preflight", "data", "content_type", "origin"}
        self.rows = {}  # slug -> {"status", "msg"}
        self.status_items = {}  # slug -> Item returned by status, set by tests
        self.suppressed = set()  # addresses enqueue rejects as suppressed
        self.lock = threading.Lock()
        mock = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def cors(self):
                self.send_header("Access-Control-Allow-Origin", "*")

            def reply(self, code, body, ctype):
                raw = body.encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(raw)))
                self.cors()
                self.end_headers()
                self.wfile.write(raw)

            def do_OPTIONS(self):
                mock.record({"method": "OPTIONS", "via": "preflight", "data": None, "content_type": "", "origin": self.headers.get("Origin")})
                self.send_response(204)
                self.cors()
                self.end_headers()

            def do_GET(self):
                q = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
                mock.record({"method": "GET", "via": "get", "data": q, "content_type": "", "origin": self.headers.get("Origin")})
                out = mock.handle(dict(q))
                if q.get("action") == "status":
                    self.reply(200, json.dumps(out, ensure_ascii=False), "application/json")
                else:
                    self.reply(200, "<!doctype html><meta charset=utf-8><title>发信助手</title><p>发信助手（模拟）</p>", "text/html; charset=utf-8")

            def do_POST(self):
                n = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(n).decode("utf-8")
                ctype = self.headers.get("Content-Type", "")
                via = "form" if ctype.startswith("application/x-www-form-urlencoded") else "fetch"
                try:
                    data = json.loads(parse_qs(raw).get("payload", [""])[0] if via == "form" else raw)
                except ValueError:
                    data = None
                mock.record({"method": "POST", "via": via, "data": data, "raw": raw, "content_type": ctype, "origin": self.headers.get("Origin")})
                out = mock.handle(data if isinstance(data, dict) else {})
                if via == "form":
                    self.reply(200, "<!doctype html><meta charset=utf-8><p>" + mock.summary(data, out) + "</p>", "text/html; charset=utf-8")
                else:
                    self.reply(200, json.dumps(out, ensure_ascii=False), "application/json")

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self):
        return "http://127.0.0.1:%d%s" % (self.server.server_address[1], PATH)

    def start(self):
        self.thread.start()
        return self

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def record(self, entry):
        with self.lock:
            self.requests.append(entry)

    def calls(self, action=None, via=None):
        with self.lock:
            out = list(self.requests)
        return [r for r in out
                if (action is None or (r["data"] or {}).get("action") == action)
                and (via is None or r["via"] == via)]

    # --- the contract -------------------------------------------------------------------

    def handle(self, data):
        if data.get("token") != self.token:
            return {"ok": False, "error": "unauthorized", "message": "口令不对。"}
        action = data.get("action")
        if action == "ping":
            return {"ok": True, "from": "business@simreal.co", "paused": False, "dailyCap": 30, "sentToday": 3,
                    "counts": {"queued": 5, "active": 2, "finished": 0, "replied": 1, "bounced": 0, "cancelled": 0, "error": 0},
                    "version": "mock"}
        if action == "enqueue":
            msgs = data.get("messages")
            if not isinstance(msgs, list) or len(msgs) > 60:
                return {"ok": False, "error": "bad_request", "message": "messages 最多 60 封。"}
            return {"ok": True, "results": [self.enqueue_one(m) for m in msgs]}
        if action == "status":
            slugs = data.get("slugs")
            if isinstance(slugs, str):
                slugs = [slugs]
            keys = slugs if slugs else sorted(set(self.rows) | set(self.status_items))
            items = [self.item(s) for s in keys if s in self.status_items or s in self.rows]
            return {"ok": True, "paused": False, "sentToday": 3, "dailyCap": 30, "now": "2026-10-03T08:00:00Z", "items": items}
        if action == "cancel":
            slug = data.get("slug")
            row = self.rows.get(slug)
            item = self.status_items.get(slug)
            status = row["status"] if row else item["status"] if item else None
            if status is None:
                return {"ok": False, "error": "bad_request", "message": "没有这一封。"}
            if status in ("queued", "active"):
                status = "cancelled"
                if row:
                    row["status"] = status
                if item:
                    item["status"] = status
                    item["outcome"] = "cancelled"
            return {"ok": True, "slug": slug, "status": status}
        if action == "test":
            return {"ok": True, "messageId": "<test-1@mock>", "threadId": "t-test-1"}
        if action in ("pause", "resume"):
            return {"ok": True, "paused": action == "pause"}
        return {"ok": False, "error": "bad_request", "message": "未知操作。"}

    def enqueue_one(self, m):
        slug = m.get("slug")
        to = str(m.get("to") or "").strip().lower()
        texts = [m.get("subject") or "", m.get("body") or ""] + [f.get("text") or "" for f in m.get("followups") or []]
        if not ADDR_RE.match(to):
            return {"slug": slug, "result": "rejected", "reason": "invalid_to"}
        if not str(m.get("subject") or "").strip() or not str(m.get("body") or "").strip():
            return {"slug": slug, "result": "rejected", "reason": "empty"}
        for t in texts:
            hit = PLACEHOLDER_RE.search(t)
            if hit:
                return {"slug": slug, "result": "rejected", "reason": "placeholder:" + hit.group(0)}
        if m.get("wave") == 9:
            return {"slug": slug, "result": "rejected", "reason": "wave_hold"}
        if to in self.suppressed:
            return {"slug": slug, "result": "rejected", "reason": "suppressed"}
        row = self.rows.get(slug)
        if row and row["status"] != "queued":
            return {"slug": slug, "result": "duplicate", "reason": ""}
        result = "updated" if row else "queued"
        self.rows[slug] = {"status": "queued", "msg": m}
        return {"slug": slug, "result": result, "reason": ""}

    def item(self, slug):
        if slug in self.status_items:
            return self.status_items[slug]
        row = self.rows[slug]
        return {"slug": slug, "to": row["msg"].get("to"), "status": row["status"], "step": 0,
                "total": 1 + len(row["msg"].get("followups") or []), "log": [], "nextAt": None,
                "outcome": None, "outcomeAt": None, "error": None, "revision": row["msg"].get("revision")}

    def summary(self, data, out):
        if not out.get("ok"):
            return "没有成功：" + out.get("message", "")
        if (data or {}).get("action") == "enqueue":
            n = sum(1 for r in out["results"] if r["result"] in ("queued", "updated"))
            return "已加入发送队列 %d 封，跳过 %d 封。可以关掉这个标签页。" % (n, len(out["results"]) - n)
        return "完成。可以关掉这个标签页。"
