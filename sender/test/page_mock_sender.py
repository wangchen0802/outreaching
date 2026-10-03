"""A local stand-in for the 发信助手 web app, for page_test.py.

Speaks the SPEC.md contract (ping / enqueue / status / cancel / test) on 127.0.0.1: POST in the
fetch form and the HTML form fallback, and GET as the link transport sends it (enqueue with z or j,
cancel, ping, test, status, dashboard). Records every request. It sends nothing.
"""

import base64
import gzip
import json
import re
import threading
import zlib
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ADDR_RE = re.compile(r"^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]{2,}$")
PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{0,80}\]")
PATH = "/macros/s/AKfake/exec"
WINDOW_NOTE = "会在对方当地工作日 8–18 点按分组顺序发出，每封间隔至少 4 分钟；对方回复后自动停止跟进。"
STATUS_LABEL = {"queued": "排队中", "active": "发送中", "finished": "已发完", "replied": "已回复", "bounced": "退信",
                "cancelled": "已取消", "error": "发送失败"}


def decode_messages(q):
    """The {"messages": [...]} a GET enqueue carries: z = base64url (with = padding) of gzip(UTF-8
    JSON), j = base64url of the plain UTF-8 JSON. Raises ValueError when it does not decode."""
    try:
        if q.get("z"):
            raw = gzip.decompress(base64.urlsafe_b64decode(q["z"]))
        elif q.get("j"):
            raw = base64.urlsafe_b64decode(q["j"])
        else:
            raise ValueError("没有 z 或 j")
        body = json.loads(raw.decode("utf-8"))
    except (ValueError, OSError, EOFError, zlib.error) as e:
        raise ValueError(str(e) or e.__class__.__name__)
    if not isinstance(body, dict):
        raise ValueError("不是对象")
    return body


def page(title, body):
    return ("<!doctype html><meta charset=utf-8><meta name=viewport content=\"width=device-width,initial-scale=1\">"
            "<title>发信助手</title><h1>%s</h1>%s" % (escape(title), body))


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
                action = q.get("action") or "dashboard"
                data = {k: v for k, v in q.items() if k not in ("z", "j")}
                data["action"] = action
                problem = None
                if action == "enqueue":
                    try:
                        body = decode_messages(q)
                        data["messages"] = body.get("messages")
                        data["encoding"] = "z" if q.get("z") else "j"
                    except ValueError as e:
                        problem = str(e)
                if action == "status" and "slugs" in q:
                    data["slugs"] = [s for s in q["slugs"].split(",") if s]
                mock.record({"method": "GET", "via": "get", "data": data, "query": q, "content_type": "", "origin": self.headers.get("Origin")})
                html = "text/html; charset=utf-8"
                if action == "status":
                    self.reply(200, json.dumps(mock.handle(data), ensure_ascii=False), "application/json")
                elif data.get("token") != mock.token:
                    self.reply(200, page("发信助手", "<p>口令不对。</p>"), html)
                elif problem is not None:
                    self.reply(200, page("发信助手", "<p>没有完成：链接里的数据读不出来（%s）。</p>" % escape(problem)), html)
                elif action == "dashboard":
                    self.reply(200, page("发信助手", "<p>发信助手（模拟）</p>"), html)
                else:
                    self.reply(200, page("发信助手", mock.result_html(data, mock.handle(data))), html)

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
            with self.lock:
                return {"ok": True, "results": [self.enqueue_one(m if isinstance(m, dict) else {}) for m in msgs]}
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
                return {"ok": False, "error": "bad_request", "message": "队列里没有 %s。" % slug}
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
        if row and (row["status"] != "queued" or row.get("sent")):
            return {"slug": slug, "result": "duplicate", "reason": ""}
        result = "updated" if row else "queued"
        self.rows[slug] = {"status": "queued", "msg": m}
        return {"slug": slug, "result": result, "reason": ""}

    def item(self, slug):
        if slug in self.status_items:
            return self.status_items[slug]
        row = self.rows[slug]
        return {"slug": slug, "to": row["msg"].get("to"), "status": row["status"], "step": row.get("sent") or 0,
                "total": 1 + len(row["msg"].get("followups") or []), "log": [], "nextAt": None,
                "outcome": None, "outcomeAt": None, "error": None, "revision": row["msg"].get("revision")}

    def summary(self, data, out):
        if not out.get("ok"):
            return "没有成功：" + out.get("message", "")
        if (data or {}).get("action") == "enqueue":
            n = sum(1 for r in out["results"] if r["result"] in ("queued", "updated"))
            return "已加入发送队列 %d 封，跳过 %d 封。可以关掉这个标签页。" % (n, len(out["results"]) - n)
        return "完成。可以关掉这个标签页。"

    def card_text(self, r):
        """One card's line on the enqueue result page, worded as Code.gs cardText_ words it. A row may
        carry "sent" and "total" (emails the sender has sent from it)."""
        if r["result"] == "queued":
            return "已加入发送队列"
        if r["result"] == "updated":
            return "已更新（还没发出，内容换成了这一版）"
        if r["result"] == "rejected":
            return "跳过：" + (r.get("reason") or "")
        row = self.rows.get(r["slug"]) or {}
        label = STATUS_LABEL.get(row.get("status"), row.get("status"))
        if row.get("sent"):
            total = row.get("total") or 1 + len(row["msg"].get("followups") or [])
            return "跳过：已发出 %d/%d 封（%s），不会重复发" % (row["sent"], total, label)
        return "跳过：这一封已是「%s」，没有改动" % label

    def result_html(self, data, out):
        """The Chinese result page a GET action answers with (SPEC "Backend: GET actions")."""
        if not out.get("ok"):
            return "<p>没有完成：%s</p>" % escape(out.get("message", ""))
        action = data.get("action")
        dash = '<p><a href="%s?action=dashboard&amp;token=%s">打开发信助手</a></p>' % (escape(self.url), escape(self.token))
        if action == "enqueue":
            by = {m.get("slug"): m for m in data.get("messages") or [] if isinstance(m, dict)}
            lines = []
            for r in out["results"]:
                m = by.get(r["slug"]) or {}
                who = (m.get("company") or r["slug"] or "") + ("（%s）" % m["contact"] if m.get("contact") else "")
                lines.append("<li>%s：%s</li>" % (escape(who), escape(self.card_text(r))))
            return "<ul>%s</ul><p>%s</p>%s" % ("".join(lines), WINDOW_NOTE, dash)
        if action == "cancel":
            if out["status"] == "cancelled":
                text = "已停止 %s 的自动发送。" % out["slug"]
            else:
                text = "%s 现在是「%s」，没有改动。" % (out["slug"], STATUS_LABEL.get(out["status"], out["status"]))
            return "<p>%s</p>%s" % (escape(text), dash)
        if action == "ping":
            text = "已连接 %s · 今天已发 %d/%d · 排队 %d 封 · %s · 版本 %s" % (
                out["from"], out["sentToday"], out["dailyCap"], out["counts"]["queued"], "已暂停" if out["paused"] else "运行中", out["version"])
            return "<p>%s</p>%s" % (escape(text), dash)
        if action == "test":
            return "<p>测试邮件已发出，请到收件箱查看。</p>" + dash
        return "<p>完成。</p>" + dash
