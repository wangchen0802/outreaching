"""Approval page <-> 发信助手 integration test (SPEC.md, "Approval page integration").

Serves approval/index.html locally, gives it a fake claude.ai runtime (page_fake_claude.js) and a
mock sender (page_mock_sender.py), and drives it in headless Chromium. Nothing is sent anywhere.
Fetch mode talks to the mock directly; link mode ("Link transport (claude.ai)") runs the page under
a CSP like claude.ai's and follows its links into new tabs.

    python sender/test/page_test.py              # needs the playwright package
    PAGE_TEST_SHOTS=/some/dir python sender/test/page_test.py   # also writes screenshots

PAGE_TEST_CHROMIUM points at a Chromium binary; without it Playwright's own is used.
"""

import base64
import gzip
import json
import os
import random
import re
import secrets
import string
import sys
import threading
import time
import unittest
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from playwright.sync_api import expect, sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from page_mock_sender import MockSender  # noqa: E402

ROOT = HERE.parents[1]
PAGE = ROOT / "approval" / "index.html"
FAKE_JS = HERE / "page_fake_claude.js"
CHROME = os.environ.get("PAGE_TEST_CHROMIUM", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
SHOTS = os.environ.get("PAGE_TEST_SHOTS")
NO_LINK = "连不上发信助手：检查地址以 /exec 结尾、部署时「谁有权访问」选了「任何人」、网络正常；也可以点「打开发信助手」核对。"
# Link mode.
LINK_MAX = 6000
LINK_STATUS = "这个页面不能直接读取发信助手；点「测试连接」会在新标签页显示结果。"
HANDED = "已交给发信助手 · 发送和跟进状态在发信助手页面看"
STOP_ASKED = "已在新标签页提交停止，请在那一页确认"
TOO_LONG = "邮件太长，链接放不下，请用 Gmail 手动发"
# Counts form submissions of any kind, so a test can show the page never posts one.
NO_FORMS = """(function () {
  window.__formSubmits = 0;
  var submit = HTMLFormElement.prototype.submit, request = HTMLFormElement.prototype.requestSubmit;
  HTMLFormElement.prototype.submit = function () { window.__formSubmits++; return submit.apply(this, arguments); };
  if (request) HTMLFormElement.prototype.requestSubmit = function () { window.__formSubmits++; return request.apply(this, arguments); };
  document.addEventListener("submit", function () { window.__formSubmits++; }, true);
})();"""
# After letting window.__passFetch fetches to the sender through, makes the next window.__failFetch
# reject like a network error (no CSP involved).
FLAKY_FETCH = """(function () {
  var real = window.fetch;
  window.__passFetch = 0;
  window.__failFetch = 0;
  window.fetch = function (u) {
    if (/\\/exec$/.test(String(u))) {
      if (window.__passFetch > 0) window.__passFetch--;
      else if (window.__failFetch > 0) { window.__failFetch--; return Promise.reject(new TypeError("Failed to fetch")); }
    }
    return real.apply(this, arguments);
  };
})();"""
# Wraps the fake db so window.__rejectReview makes every update that carries a review fail.
FAILING_REVIEW_WRITES = """(function () {
  var orig = window.claude;
  if (!orig) return;
  window.__rejectReview = false;
  window.claude = { use: function (name) {
    return orig.use(name).then(function (cap) {
      if (name !== "db" || !cap) return cap;
      return { collection: cap.collection, doc: function (path) {
        var r = cap.doc(path);
        return { id: r.id, path: r.path, get: r.get, set: r.set, delete: r.delete, onSnapshot: r.onSnapshot,
          update: function (data) {
            if (window.__rejectReview && data.review) { var e = new Error("offline"); e.code = "unavailable"; return Promise.reject(e); }
            return r.update(data);
          } };
      } };
    });
  } };
})();"""

DECK = "https://simreal.co/deck"
SETTINGS = {"from": "business@simreal.co", "nameEn": "Charles", "nameZh": "查尔斯", "contact": "simreal-charles", "deck": ""}
SETTINGS_DECK = dict(SETTINGS, deck=DECK)


# --- seed docs, shaped like build/db/*.json ------------------------------------------------

def base_doc(**kw):
    doc = {
        "slug": "", "track": "", "company": "", "category": "", "region": "", "contact": "", "role": "",
        "sources": ["https://example.com/source"], "angle": "", "confidence": "中", "to": "", "toSource": "",
        "channel": "", "toGeneric": "", "order": 9999, "updatedAt": "2026-09-27T13:45:40Z", "lang": "en",
        "subject": "", "body": "", "salutation": "", "opening": "", "domains": "", "followups": [],
        "wechat": "", "dm": "", "meta_md": "", "notes_md": "**切入点**\n- 测试数据。",
    }
    doc.update(kw)
    return doc


INVESTOR_BODY = (
    "Hi Hunter,\n\nHomebrew backs technical seed teams and has written about RL post-training; we're building for that shift, starting with finance.\n\n"
    "I'm [Your name], co-founder of SimReal. We're four quants from Jane Street, Citadel, Millennium and Optiver (Cambridge, LSE, Duke).\n\n"
    "SimReal builds RL environments and verifiers where AI models do real work and are scored on real outcomes.\n\n"
    "Traction: our trading environment, Xitadel, lifted Qwen3.8-27B's trading performance 12% on unseen market data, reproduced across independent runs.\n\n"
    "We're raising a $20M seed and are in conversations with tier-1 funds. Deck: [Deck link]. Worth 20 minutes next week?\n\n"
    "Best,\n[Your name]\nCo-founder, SimReal\nbusiness@simreal.co | simreal.co"
)
INVESTOR_FUS = [
    {"day": 5, "text": "Hi Hunter,\n\nFollowing up in case this got buried. Happy to send the deck and the Xitadel run logs; 30 minutes next week would be enough to walk through both.\n\nBest,\n[Your name]"},
    {"day": 12, "text": "Hi Hunter,\n\nOne update and then I'll leave it with you: the round is moving, and we'd like Homebrew to see it before it closes. If it isn't a fit, a one-line reply is plenty.\n\nBest,\n[Your name]"},
]


def seed_docs():
    investor = base_doc(
        slug="v-homebrew", track="investor", company="Homebrew", category="VC", region="海外", contact="Hunter Walk",
        role="合伙人", to="hunter@homebrew.example", toSource="https://example.com/team", order=2010, lang="en",
        subject="Ex-Jane Street quants building RL environments, supplying Surge AI", body=INVESTOR_BODY,
        salutation="Hi Hunter,", opening="Homebrew backs technical seed teams and has written about RL post-training; we're building for that shift, starting with finance.",
        followups=INVESTOR_FUS, wave=1, waveWhy="种子基金，先发练手。",
        meta_md="- 类别：VC｜地区：海外（美国）\n- 收件人：**Hunter Walk**，合伙人\n- 置信度：中",
    )
    hold = base_doc(
        slug="v-01-advisors", track="investor", company="01 Advisors", category="VC", region="海外", contact="Adam Bain",
        role="合伙人", to="adam@01a.example", order=3840, lang="en",
        subject="SimReal: RL environments where AI learns from real outcomes (seed)",
        body="Hi Adam,\n\nShort note from SimReal. Can I send you the deck?\n\nBest,\n[Your name]",
        salutation="Hi Adam,", opening="Short note from SimReal.",
        followups=[{"day": 5, "text": "Hi Adam,\n\nFollowing up.\n\nBest,\n[Your name]"}, {"day": 12, "text": "Hi Adam,\n\nLast note.\n\nBest,\n[Your name]"}],
        wave=9, waveWhy="偏后期，先放一放。",
        meta_md="- 类别：VC｜地区：海外（美国）\n- 收件人：**Adam Bain**，合伙人",
    )
    customer = base_doc(
        slug="deepseek", track="customer", company="DeepSeek 深度求索", category="国内大模型公司", region="国内",
        contact="邵智宏（Zhihong Shao）", role="研究员", to="shao@deepseek.example", order=3250, lang="zh",
        subject="SimReal｜DeepSeek 后训练环境与专家数据",
        body="邵老师您好，\n\n我是 SimReal（simreal.co）联合创始人[姓名]，我们为大模型后训练提供 RL 环境、验证器和专家数据。\n\n下周是否方便约 20 分钟聊聊？\n\n[姓名]\nSimReal 联合创始人\nbusiness@simreal.co｜微信/电话：[ ]",
        salutation="邵老师您好，", opening="我们为大模型后训练提供 RL 环境、验证器和专家数据。",
        followups=[{"day": 4, "text": "邵老师您好，\n\n跟进一下前几天的邮件。\n\n[姓名]"}, {"day": 10, "text": "邵老师您好，\n\n最后跟进一次。\n\n[姓名]"}],
        wechat="邵老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。",
        meta_md="- 类别：国内大模型公司｜地区：国内（杭州）\n- 收件人：**邵智宏（Zhihong Shao）**",
    )
    partner = base_doc(
        slug="p-abaka-ai", track="partner", company="Abaka AI", category="数据供应商", region="海外", contact="未找到",
        channel="https://abaka.example/contact", order=1100, lang="en",
        subject="Expert supply for your RL environments",
        body="Hi Abaka team,\n\nWe can supply experts.\n\nBest,\n[Your name]",
        salutation="Hi Abaka team,", opening="We can supply experts.",
        followups=[{"day": 4, "text": "Hi,\n\nFollowing up.\n\n[Your name]"}, {"day": 10, "text": "Hi,\n\nLast note.\n\n[Your name]"}],
        meta_md="- 类别：数据供应商｜地区：海外（新加坡）",
    )
    return {d["slug"]: d for d in (investor, hold, customer, partner)}


def approved(doc, **send):
    doc = dict(doc, review={"status": "approved", "comment": "", "at": "2026-09-30T08:00:00Z", "forRevision": 1})
    if send:
        doc["send"] = send
    return doc


def customer_doc(slug, company, order, send=None, **kw):
    """An approved customer card that can be handed over once 发件设置 has the 中文署名."""
    doc = approved(base_doc(
        slug=slug, track="customer", company=company, category="测试", region="国内", contact="某人",
        to="%s@example.com" % slug, order=order, lang="zh", subject="主题 " + company,
        body="您好，\n\n正文。\n\n[姓名]", followups=[{"day": 4, "text": "跟进。[姓名]"}],
        meta_md="- 类别：测试｜地区：国内（北京）", **kw))
    if send:
        doc["send"] = send
    return doc


HANDED_AUTO = {"status": "handed", "via": "link", "at": "2026-10-01T08:00:00Z", "sig": None, "revision": 1}


def finalize(text, lang, s):
    t = text
    if lang == "en" and s.get("nameEn"):
        t = t.replace("[Your name]", s["nameEn"])
    if s.get("nameZh"):
        t = t.replace("[姓名]", s["nameZh"])
    if s.get("contact"):
        t = t.replace("微信/电话：[ ]", "微信/电话：" + s["contact"])
    if s.get("deck"):
        t = t.replace("[Deck link]", s["deck"]).replace("[BP 链接]", s["deck"])
    return t


def expected_msg(doc, s, region, tz):
    """The Msg the page must hand over for doc under settings s (SPEC "Building a Msg from a card")."""
    lang = "en" if doc["lang"] == "en" else "zh"
    return {
        "slug": doc["slug"], "track": doc["track"], "company": doc["company"], "contact": doc["contact"],
        "to": (doc.get("to") or doc.get("toManual") or doc.get("toGeneric") or "").strip(),
        "subject": doc["subject"], "body": finalize(doc["body"], lang, s),
        "followups": [{"day": f["day"], "text": finalize(f["text"], lang, s)} for f in doc["followups"]],
        "lang": lang, "region": region, "tz": tz,
        "wave": (doc.get("wave") or 2) if doc["track"] == "investor" else 2,
        "order": doc.get("order") or 9999, "revision": doc.get("revision") or 1,
        "fromName": (s.get("nameEn") if lang == "en" else s.get("nameZh")) or "",
    }


def split_link(href):
    """(base url, decoded query, raw query) of a sender link."""
    u = urlparse(href)
    raw = {}
    for part in u.query.split("&"):
        k, _, v = part.partition("=")
        raw[k] = v
    return "%s://%s%s" % (u.scheme, u.netloc, u.path), {k: unquote(v) for k, v in raw.items()}, raw


# 地区 -> zone the page must pick (SPEC list, plus the European/Indian/Australian additions).
TZ_CASES = [
    ("海外（美国）", "America/Los_Angeles"), ("海外（美国，纽约）", "America/New_York"),
    ("海外（美国，芝加哥）", "America/Chicago"), ("海外（美国，西雅图）", "America/Los_Angeles"),
    ("海外（美国，康涅狄格）", "America/New_York"), ("海外（美国，费城）", "America/New_York"),
    ("海外（英国，伦敦）", "Europe/London"), ("海外（新加坡）", "Asia/Singapore"), ("海外（香港）", "Asia/Hong_Kong"),
    ("国内（香港）", "Asia/Hong_Kong"), ("海外（荷兰/美国）", "Europe/Amsterdam"), ("海外（以色列/美国）", "Asia/Jerusalem"),
    ("海外（美国/以色列）", "America/Los_Angeles"), ("海外（韩国）", "Asia/Seoul"), ("海外（日本）", "Asia/Tokyo"),
    ("海外（加拿大/美国）", "America/Toronto"), ("国内（北京）", "Asia/Shanghai"), ("国内", "Asia/Shanghai"),
    ("海外（法国）", "Europe/Amsterdam"), ("海外（印度）", "Asia/Kolkata"), ("海外（澳大利亚）", "Australia/Sydney"),
    ("海外（美国/拉美）", "America/Los_Angeles"), (None, "America/Los_Angeles"),
]


# --- local page server ---------------------------------------------------------------------

class PageServer:
    """Serves approval/index.html at / inside the skeleton the Artifact tool publishes it in.
    /?csp=<policy> also sends that Content-Security-Policy header; /?meta=<policy> puts the policy
    in a <meta http-equiv> tag in the head instead."""

    def __init__(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                url = urlparse(self.path)
                if url.path != "/":
                    self.send_response(404)
                    self.end_headers()
                    return
                q = parse_qs(url.query)
                meta = '<meta http-equiv="Content-Security-Policy" content="%s">' % escape(q["meta"][0]) if q.get("meta") else ""
                html = ('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
                        + meta + "</head><body>" + PAGE.read_text(encoding="utf-8") + "</body></html>").encode("utf-8")
                csp = q.get("csp")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                if csp:
                    self.send_header("Content-Security-Policy", csp[0])
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.origin = "http://127.0.0.1:%d" % self.server.server_address[1]

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


class PageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        kw = {"headless": True}
        if os.path.exists(CHROME):
            kw["executable_path"] = CHROME
        cls.browser = cls.pw.chromium.launch(**kw)
        cls.site = PageServer()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.site.stop()

    def setUp(self):
        self.token = "tok" + secrets.token_hex(16)
        self.mock = MockSender(self.token).start()
        self.ctx = None
        self.page = None

    def tearDown(self):
        try:
            if self.page and not self.page.is_closed():
                self.assert_db_has_no_secret()
        finally:
            if self.ctx:
                self.ctx.close()
            self.mock.stop()

    # --- helpers ---------------------------------------------------------------------------

    def open(self, docs, settings=SETTINGS, connected=True, color_scheme="light", width=1200, height=900,
             init=None, clock=False, extra_docs=None, csp=None, csp_meta=None):
        self.ctx = self.browser.new_context(viewport={"width": width, "height": height}, color_scheme=color_scheme,
                                            timezone_id="Asia/Shanghai", locale="zh-CN")
        self.ctx.route(re.compile(r"^https://fonts\.(googleapis|gstatic)\.com/"), lambda route: route.abort())
        store = {"prospects/" + slug: d for slug, d in docs.items()}
        if settings is not None:
            store["settings/sender"] = settings
        store.update(extra_docs or {})
        seed = {"docs": store, "canEdit": True, "pageOrigin": self.site.origin}
        self.ctx.add_init_script(script="window.__PAGE_SEED__ = " + json.dumps(seed, ensure_ascii=False) + ";")
        self.ctx.add_init_script(path=str(FAKE_JS))
        if connected:
            conn = json.dumps({"url": self.mock.url, "token": self.token})
            self.ctx.add_init_script(script="if (location.origin === %s) localStorage.setItem('simreal.sender', %s);"
                                     % (json.dumps(self.site.origin), json.dumps(conn)))
        if init:
            self.ctx.add_init_script(script=init)
        self.page = self.ctx.new_page()
        if clock:
            self.page.clock.install()
        query = (["csp=" + quote(csp)] if csp else []) + (["meta=" + quote(csp_meta)] if csp_meta else [])
        self.page.goto(self.site.origin + "/" + ("?" + "&".join(query) if query else ""))
        # The default filter may show none of them.
        self.page.wait_for_selector("article.card", state="attached")
        return self.page

    def link_csp(self):
        # What claude.ai is expected to set (research Q9): fetch only to itself and its static
        # server, forms only to itself. The mock sender is another origin, so its fetch is blocked.
        return "connect-src 'self' %s; form-action 'self'" % self.site.origin

    def open_links(self, docs, init="", **kw):
        """Opens the page under link_csp() and waits until it has switched to links."""
        page = self.open(docs, csp_meta=self.link_csp(), init=NO_FORMS + init, **kw)
        expect(page.locator("#s-conn")).to_have_text("链接方式")
        return page

    def click_tab(self, link):
        """Clicks a link and returns the new tab it opened, loaded."""
        with self.ctx.expect_page() as info:
            link.click()
        tab = info.value
        tab.wait_for_load_state()
        return tab

    def enqueue_link(self, href, key="z"):
        """The Msgs an enqueue link carries, after checking its shape. key is z (gzip) or j (plain)."""
        self.assertLessEqual(len(href), LINK_MAX)
        base, q, raw = split_link(href)
        self.assertEqual(base, self.mock.url)
        self.assertEqual(set(q), {"action", "token", key})
        self.assertEqual(q["action"], "enqueue")
        self.assertEqual(q["token"], self.token)
        # base64url with its "=" padding, then encodeURIComponent: the padding arrives as %3D.
        self.assertRegex(raw[key], r"^[A-Za-z0-9_-]+(%3D){0,2}$")
        self.assertEqual(len(q[key]) % 4, 0)
        data = base64.urlsafe_b64decode(q[key])
        body = json.loads((gzip.decompress(data) if key == "z" else data).decode("utf-8"))
        self.assertEqual(list(body), ["messages"])
        return body["messages"]

    def assert_new_tab(self, link):
        self.assertEqual(link.get_attribute("target"), "_blank")
        self.assertIn("noopener", link.get_attribute("rel"))

    def assert_no_post(self):
        self.assertEqual([r for r in self.mock.requests if r["method"] != "GET"], [])
        self.assertEqual(self.page.evaluate("window.__formSubmits"), 0)

    def assert_fits(self, width, where):
        page = self.page
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        self.assertLessEqual(overflow, 0, "horizontal scroll: " + where)
        boxes = page.evaluate("""() => Array.from(document.querySelectorAll('a[data-link], #s-dash, .auto-line, .auto-links'))
          .filter(e => e.offsetParent !== null)
          .map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim().slice(0, 40), r.left, r.right]; })""")
        self.assertTrue(boxes, where)
        for text, left, right in boxes:
            self.assertGreaterEqual(left, 0, "%s sticks out on the left: %s" % (text, where))
            self.assertLessEqual(right, width + 0.5, "%s sticks out on the right: %s" % (text, where))

    def card(self, slug):
        return self.page.locator('article.card[data-slug="%s"]' % slug)

    def show(self, tab, status):
        self.page.click("#tabbtn-" + tab)
        self.page.click('.chip[data-status="%s"]' % status)

    def writes(self):
        return self.page.evaluate("window.__dbWrites")

    def store(self):
        return self.page.evaluate("window.__dbStore()")

    def doc(self, slug):
        return self.store().get("prospects/" + slug)

    def wait_until(self, fn, what, timeout=6.0):
        end = time.time() + timeout
        while time.time() < end:
            value = fn()
            if value:
                return value
            self.page.wait_for_timeout(40)
        self.fail("timed out waiting for " + what)

    def settle(self, ms=600):
        self.page.wait_for_timeout(ms)

    def enqueues(self):
        return [r["data"] for r in self.mock.calls("enqueue")]

    def assert_db_has_no_secret(self):
        dump = json.dumps([self.writes(), self.store()], ensure_ascii=False)
        port = str(self.mock.server.server_address[1])
        self.assertNotIn(self.token, dump, "token reached the db")
        self.assertNotIn(self.mock.url, dump, "sender url reached the db")
        self.assertNotIn("127.0.0.1:" + port, dump, "sender host reached the db")
        for w in self.writes():
            if w["path"] == "settings/sender":
                self.assertLessEqual(set(w["data"]), {"from", "nameEn", "nameZh", "contact", "deck", "autoSend"})
                if "autoSend" in w["data"]:
                    self.assertIsInstance(w["data"]["autoSend"], bool)

    # --- tests -----------------------------------------------------------------------------

    def test_connect_ping_test_dashboard_disconnect(self):
        page = self.open(seed_docs(), connected=False)
        self.show("investor", "pending")
        expect(self.card("v-homebrew").locator('[data-act="approve"]')).to_have_text("批准")
        expect(page.locator("#s-conn")).to_have_text("未连接")
        self.assertTrue(page.locator("#s-ping").is_disabled())
        self.assertTrue(page.locator("#s-dash").is_hidden())

        # A /dev address only works for its owner while signed in: refused before anything is saved.
        page.fill("#s-url", self.mock.url[:-len("exec")] + "dev")
        page.fill("#s-token", self.token)
        page.click("#s-save")
        expect(page.locator("#s-state")).to_contain_text("以 /dev 结尾的测试地址")
        expect(page.locator("#s-conn")).to_have_text("未连接")
        self.assertEqual(self.mock.requests, [])

        page.fill("#s-url", self.mock.url)
        page.fill("#s-token", "wrong-token")
        page.click("#s-save")
        expect(page.locator("#s-state")).to_contain_text("口令不对")
        expect(page.locator("#s-conn")).to_have_text("口令不对")

        page.fill("#s-token", self.token)
        page.click("#s-save")
        expect(page.locator("#s-state")).to_have_text("已连接 business@simreal.co · 今天已发 3/30 · 排队 5 封 · 运行中")
        page.click("#s-ping")
        self.wait_until(lambda: len(self.mock.calls("ping")) == 3, "second ping")
        expect(page.locator("#s-state")).to_have_text("已连接 business@simreal.co · 今天已发 3/30 · 排队 5 封 · 运行中")
        expect(page.locator("#s-conn")).to_have_text("已连接")

        saved = json.loads(page.evaluate("localStorage.getItem('simreal.sender')"))
        self.assertEqual(saved, {"url": self.mock.url, "token": self.token})
        self.wait_until(lambda: self.store()["settings/sender"].get("autoSend") is True, "autoSend flag")
        self.assertEqual({k: v for k, v in self.store()["settings/sender"].items() if k != "autoSend"}, SETTINGS)

        dash = page.locator("#s-dash")
        self.assertEqual(dash.get_attribute("href"), self.mock.url + "?action=dashboard&token=" + self.token)
        self.assertEqual(dash.get_attribute("target"), "_blank")
        self.assertIn("noopener", dash.get_attribute("rel"))

        page.click("#s-test")
        expect(page.locator("#s-state")).to_have_text("已发出一封测试邮件到 business@simreal.co，去收件箱看看。")
        self.assertEqual(len(self.mock.calls("test")), 1)

        # Every call went as a simple text/plain POST: no preflight, token in the body.
        for r in self.mock.calls(via="fetch"):
            self.assertTrue(r["content_type"].startswith("text/plain"), r["content_type"])
        self.assertEqual(self.mock.calls(via="preflight"), [])

        expect(self.card("v-homebrew").locator('[data-act="approve"]')).to_have_text("批准并自动发送")
        page.click("#s-off")
        expect(page.locator("#s-conn")).to_have_text("未连接")
        self.assertIsNone(page.evaluate("localStorage.getItem('simreal.sender')"))
        self.wait_until(lambda: self.store()["settings/sender"].get("autoSend") is False, "autoSend off")
        expect(self.card("v-homebrew").locator('[data-act="approve"]')).to_have_text("批准")

    def test_approve_blocked_while_deck_missing(self):
        page = self.open(seed_docs())
        self.show("investor", "pending")
        btn = self.card("v-homebrew").locator('[data-act="approve"]')
        expect(btn).to_have_text("批准并自动发送")
        btn.click()
        expect(page.locator("#toast")).to_contain_text("没交给发信助手：还要补 BP 链接")
        self.wait_until(lambda: (self.doc("v-homebrew").get("review") or {}).get("status") == "approved", "approval")
        self.settle()
        self.assertEqual(self.enqueues(), [])
        self.assertNotIn("auto", self.doc("v-homebrew").get("send") or {})
        self.show("investor", "todo")
        card = self.card("v-homebrew")
        expect(card.locator(".review-note.warn")).to_contain_text("还不能交给发信助手：还要补 BP 链接")
        expect(card.locator('[data-act="autosend"]')).to_be_disabled()
        # The manual path is still there for this card.
        expect(card.locator('a[href^="https://mail.google.com/mail/?"]')).to_have_text("在 Gmail 打开第 1 封")

    def test_approve_and_send_after_setting_deck(self):
        page = self.open(seed_docs())
        page.fill("#f-deck", DECK)
        self.wait_until(lambda: self.store()["settings/sender"].get("deck") == DECK, "deck saved")
        self.show("investor", "pending")
        self.card("v-homebrew").locator('[data-act="approve"]').click()
        self.wait_until(lambda: self.enqueues(), "enqueue")
        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "send.auto")
        self.settle()
        calls = self.enqueues()
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["token"], self.token)
        msgs = calls[0]["messages"]
        self.assertEqual(len(msgs), 1)
        m = msgs[0]
        src = seed_docs()["v-homebrew"]
        self.assertEqual(m["slug"], "v-homebrew")
        self.assertEqual(m["track"], "investor")
        self.assertEqual(m["company"], "Homebrew")
        self.assertEqual(m["contact"], "Hunter Walk")
        self.assertEqual(m["to"], "hunter@homebrew.example")
        self.assertEqual(m["subject"], src["subject"])
        self.assertEqual(m["body"], finalize(src["body"], "en", SETTINGS_DECK))
        self.assertIn("Deck: " + DECK + ".", m["body"])
        self.assertNotRegex(m["body"], r"\[[^\]\n]{0,80}\]")
        self.assertEqual(m["followups"], [{"day": f["day"], "text": finalize(f["text"], "en", SETTINGS_DECK)} for f in src["followups"]])
        self.assertEqual(m["lang"], "en")
        self.assertEqual(m["region"], "海外（美国）")
        self.assertEqual(m["tz"], "America/Los_Angeles")
        self.assertEqual(m["wave"], 1)
        self.assertEqual(m["order"], 2010)
        self.assertEqual(m["revision"], 1)
        self.assertEqual(m["fromName"], "Charles")

        doc = self.doc("v-homebrew")
        self.assertEqual(doc["review"]["status"], "approved")
        auto = doc["send"]["auto"]
        self.assertEqual(auto["status"], "queued")
        self.assertEqual(auto["revision"], 1)
        self.assertRegex(auto["queuedAt"], r"^\d{4}-\d\d-\d\dT")
        self.assertNotIn("log", doc["send"])
        expect(page.locator("#toast")).to_contain_text("已交给发信助手")

        self.show("investor", "waiting")
        card = self.card("v-homebrew")
        expect(card.locator(".status")).to_have_text("排队中（自动）")
        expect(card.locator(".auto-line")).to_contain_text("排队中（预计按分组顺序在工作时间发出）")
        expect(card.locator('[data-act="autostop"]')).to_have_text("停止自动发送")
        self.assertEqual(card.locator('a[href^="https://mail.google.com/mail/?"]').count(), 0)
        self.assertEqual(card.locator('[data-act="sent"]').count(), 0)
        expect(page.locator("#t-todo-sub")).to_contain_text("自动排队 1")

        # A Chinese customer: Shanghai time, the Chinese signature, contact filled in.
        self.show("customer", "pending")
        self.card("deepseek").locator('[data-act="approve"]').click()
        self.wait_until(lambda: len(self.enqueues()) == 2, "second enqueue")
        m = self.enqueues()[1]["messages"][0]
        zh = seed_docs()["deepseek"]
        self.assertEqual(m["tz"], "Asia/Shanghai")
        self.assertEqual(m["region"], "国内（杭州）")
        self.assertEqual(m["fromName"], "查尔斯")
        self.assertEqual(m["wave"], 2)
        self.assertEqual(m["lang"], "zh")
        self.assertEqual(m["body"], finalize(zh["body"], "zh", SETTINGS_DECK))
        self.assertIn("微信/电话：simreal-charles", m["body"])
        self.assertEqual([f["day"] for f in m["followups"]], [4, 10])

    def test_wave_9_and_missing_address_refused(self):
        page = self.open(seed_docs(), settings=SETTINGS_DECK)
        self.show("investor", "pending")
        self.card("v-01-advisors").locator('[data-act="approve"]').click()
        expect(page.locator("#toast")).to_contain_text("暂缓组不自动发送")
        self.show("partner", "pending")
        self.card("p-abaka-ai").locator('[data-act="approve"]').click()
        expect(page.locator("#toast")).to_contain_text("没有邮箱")
        self.settle()
        self.assertEqual(self.enqueues(), [])
        self.show("investor", "todo")
        expect(self.card("v-01-advisors").locator(".review-note.warn", has_text="还不能交给发信助手")).to_have_text("还不能交给发信助手：暂缓组不自动发送")
        self.show("partner", "todo")
        expect(self.card("p-abaka-ai").locator(".review-note.warn")).to_contain_text("没有邮箱")

    def test_sender_rejection_and_errors_show_on_the_card(self):
        self.mock.suppressed.add("hunter@homebrew.example")
        page = self.open(seed_docs(), settings=SETTINGS_DECK)
        self.show("partner", "pending")
        expect(self.card("p-abaka-ai").locator(".missing", has_text="批准后不会自动发")).to_have_text("批准后不会自动发：没有邮箱")
        self.show("investor", "pending")
        self.card("v-homebrew").locator('[data-act="approve"]').click()
        expect(page.locator("#toast")).to_contain_text("发信助手没收：这个邮箱在屏蔽名单里")
        self.assertEqual(len(self.enqueues()), 1)
        self.settle()
        self.assertNotIn("auto", self.doc("v-homebrew").get("send") or {})
        self.show("investor", "todo")
        card = self.card("v-homebrew")
        expect(card.locator(".review-note.warn", has_text="发信助手没收")).to_contain_text("这个邮箱在屏蔽名单里")
        expect(card.locator('[data-act="autosend"]')).to_be_enabled()

        # A wrong token: nothing is written and the card says why.
        self.mock.token = "rotated"
        self.show("customer", "pending")
        self.card("deepseek").locator('[data-act="approve"]').click()
        expect(page.locator("#toast")).to_contain_text("但没交上：口令不对")
        self.settle()
        self.assertNotIn("send", self.doc("deepseek"))

    def test_batch_hands_over_only_eligible_cards(self):
        docs = seed_docs()
        for slug in ("v-homebrew", "v-01-advisors", "p-abaka-ai"):
            docs[slug] = approved(docs[slug])
        page = self.open(docs, settings=SETTINGS_DECK)
        self.show("investor", "pending")
        self.assertTrue(page.locator("#auto-all-btn").is_hidden(), "batch button belongs to 今天要发")
        self.show("investor", "todo")
        btn = page.locator("#auto-all-btn")
        expect(btn).to_have_text("全部交给发信助手（1 封）")
        expect(page.locator("#auto-hint")).to_contain_text("暂缓组不自动发送 1 封")
        expect(self.card("v-homebrew").locator('[data-act="autosend"]')).to_have_text("交给发信助手")
        btn.click()
        expect(page.locator("#auto-hint")).to_have_text("已交给发信助手 1 封。")
        calls = self.enqueues()
        self.assertEqual(len(calls), 1)
        self.assertEqual([m["slug"] for m in calls[0]["messages"]], ["v-homebrew"])
        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "send.auto")
        self.assertNotIn("send", self.doc("v-01-advisors"))
        self.show("partner", "todo")
        expect(page.locator("#auto-all-btn")).to_have_text("全部交给发信助手（0 封）")
        expect(page.locator("#auto-all-btn")).to_be_disabled()
        expect(page.locator("#auto-hint")).to_contain_text("没有邮箱 1 封")

    def test_batch_sends_50_per_request_and_maps_time_zones(self):
        docs, want = {}, {}
        for i in range(55):
            place, tz = TZ_CASES[i % len(TZ_CASES)]
            slug = "c-gen-%02d" % i
            meta = ("- 类别：测试｜地区：" + place) if place else "- 类别：测试"
            docs[slug] = approved(base_doc(
                slug=slug, track="customer", company="Gen %02d" % i, category="测试", region="海外" if not place or "海外" in place else "国内",
                contact="Someone", to="c%d@example.com" % i, order=5000 + i, lang="zh", subject="主题 %d" % i,
                body="您好，\n\n正文。\n\n[姓名]", followups=[{"day": 4, "text": "跟进。[姓名]"}], meta_md=meta))
            want[slug] = tz
        page = self.open(docs, settings=SETTINGS_DECK)
        self.show("customer", "todo")
        expect(page.locator("#auto-all-btn")).to_have_text("全部交给发信助手（55 封）")
        page.click("#auto-all-btn")
        expect(page.locator("#auto-hint")).to_have_text("已交给发信助手 55 封。", timeout=10000)
        calls = self.enqueues()
        self.assertEqual([len(c["messages"]) for c in calls], [50, 5])
        got = {m["slug"]: m["tz"] for c in calls for m in c["messages"]}
        self.assertEqual(got, want)
        self.assertTrue(all(m["body"].endswith("查尔斯") for c in calls for m in c["messages"]))
        self.wait_until(lambda: all((d.get("send") or {}).get("auto", {}).get("status") == "queued"
                                    for p, d in self.store().items() if p.startswith("prospects/")), "all queued")

    def test_status_sync_maps_items_and_writes_only_on_change(self):
        docs = seed_docs()
        queued = {"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1}
        for slug in docs:
            docs[slug] = approved(docs[slug], auto=dict(queued))
        self.mock.status_items = {
            "v-homebrew": {"slug": "v-homebrew", "to": "hunter@homebrew.example", "status": "active", "step": 1, "total": 3,
                           "log": [{"step": 1, "at": "2026-10-01T09:12:00Z", "messageId": "<a@x>", "threadId": "t1"}],
                           "nextAt": "2026-10-06T02:00:00Z", "outcome": None, "outcomeAt": None, "error": None, "revision": 1},
            "deepseek": {"slug": "deepseek", "to": "shao@deepseek.example", "status": "replied", "step": 1, "total": 3,
                         "log": [{"step": 1, "at": "2026-10-01T02:00:00Z", "messageId": "<b@x>", "threadId": "t2"}],
                         "nextAt": None, "outcome": "replied", "outcomeAt": "2026-10-02T03:00:00Z", "error": None, "revision": 1},
            "v-01-advisors": {"slug": "v-01-advisors", "to": "adam@01a.example", "status": "bounced", "step": 1, "total": 3,
                              "log": [{"step": 1, "at": "2026-10-01T03:00:00Z", "messageId": "<c@x>", "threadId": "t3"}],
                              "nextAt": None, "outcome": "bounced", "outcomeAt": "2026-10-01T03:05:00Z", "error": None, "revision": 1},
            "p-abaka-ai": {"slug": "p-abaka-ai", "to": "", "status": "error", "step": 0, "total": 3, "log": [], "nextAt": None,
                           "outcome": None, "outcomeAt": None, "error": "Invalid To header", "revision": 1},
        }
        page = self.open(docs, settings=SETTINGS_DECK, clock=True)
        self.wait_until(lambda: self.mock.calls("status"), "first sync")
        # Every row is read, so a handover whose db write was lost still reaches its card.
        self.assertNotIn("slugs", self.mock.calls("status")[0]["data"])
        self.wait_until(lambda: len(self.writes()) == 4, "four sync writes")

        home = self.doc("v-homebrew")["send"]
        self.assertEqual(home["log"], [{"step": 0, "at": "2026-10-01T09:12:00Z"}])
        self.assertIsNone(home["outcome"])
        self.assertEqual(home["auto"]["status"], "active")
        self.assertEqual(home["auto"]["step"], 1)
        self.assertEqual(home["auto"]["total"], 3)
        self.assertEqual(home["auto"]["nextAt"], "2026-10-06T02:00:00Z")
        self.assertEqual(home["auto"]["queuedAt"], "2026-09-30T08:00:00Z")
        self.assertEqual(home["auto"]["revision"], 1)
        self.assertRegex(home["auto"]["syncedAt"], r"^\d{4}-")
        ds = self.doc("deepseek")["send"]
        self.assertEqual(ds["outcome"], "replied")
        self.assertEqual(ds["outcomeAt"], "2026-10-02T03:00:00Z")
        self.assertEqual(ds["log"], [{"step": 0, "at": "2026-10-01T02:00:00Z"}])
        self.assertEqual(ds["auto"]["outcome"], "replied")
        self.assertEqual(self.doc("v-01-advisors")["send"]["outcome"], "stopped")
        self.assertEqual(self.doc("p-abaka-ai")["send"]["outcome"], "stopped")
        self.assertEqual(self.doc("p-abaka-ai")["send"]["auto"]["error"], "Invalid To header")

        self.show("customer", "closed")
        card = self.card("deepseek")
        expect(card.locator(".status")).to_have_text("已回复")
        expect(card.locator(".auto-line")).to_contain_text("已回复")
        expect(card.locator('[data-act="meeting"]')).to_be_visible()
        self.show("investor", "waiting")
        card = self.card("v-homebrew")
        expect(card.locator(".status")).to_have_text("自动跟进")
        expect(card.locator(".auto-line")).to_contain_text("已发首封 10-01 17:12，第 2 封约 10-06")
        expect(card.locator(".seq")).to_contain_text("自动发")
        self.assertEqual(card.locator('[data-act="sent"]').count(), 0)
        self.assertEqual(card.locator('[data-copy^="fu"]').count(), 0)
        self.show("investor", "closed")
        expect(self.card("v-01-advisors").locator(".status")).to_have_text("退信")
        # A failed send needs Charles: it is listed under 今天要发, not filed away as finished.
        self.show("partner", "todo")
        card = self.card("p-abaka-ai")
        expect(card.locator(".status")).to_have_text("发送失败")
        expect(card.locator(".auto-line")).to_contain_text("发送失败：Invalid To header")
        expect(page.locator("#t-todo-sub")).to_contain_text("发送失败 1")
        expect(page.locator("#s-sync")).to_contain_text("今天已发 3/30 · 运行中")

        # Three minutes later the page syncs again; nothing changed, so nothing is written.
        page.clock.fast_forward("03:05")
        self.wait_until(lambda: len(self.mock.calls("status")) == 2, "interval sync")
        self.settle(400)
        self.assertEqual(len(self.writes()), 4)

        # A failed row can be taken back by hand; that drops send.auto.
        card.locator('[data-act="resume"]').click()
        self.wait_until(lambda: self.doc("p-abaka-ai")["send"].get("auto", 1) is None, "auto dropped")
        self.assertIsNone(self.doc("p-abaka-ai")["send"]["outcome"])

    def test_stop_calls_cancel(self):
        docs = seed_docs()
        docs["v-homebrew"] = approved(docs["v-homebrew"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
        self.mock.rows["v-homebrew"] = {"status": "queued", "msg": {"followups": [{}, {}], "revision": 1}}
        page = self.open(docs, settings=SETTINGS_DECK)
        self.show("investor", "all")
        card = self.card("v-homebrew")
        stop = card.locator('[data-act="autostop"]')
        expect(stop).to_have_text("停止自动发送")
        stop.click()
        expect(stop).to_have_text("确定停止？再点一次")
        self.assertEqual(self.mock.calls("cancel"), [])
        stop.click()
        self.wait_until(lambda: self.mock.calls("cancel"), "cancel")
        self.assertEqual(self.mock.calls("cancel")[0]["data"]["slug"], "v-homebrew")
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"]["status"] == "cancelled", "cancelled")
        send = self.doc("v-homebrew")["send"]
        self.assertEqual(send["outcome"], "stopped")
        self.assertEqual(send["auto"]["queuedAt"], "2026-09-30T08:00:00Z")
        expect(card.locator(".auto-line")).to_contain_text("已取消")
        expect(card.locator('[data-act="resume"]')).to_have_text("改为手动发送")
        self.assertEqual(self.mock.rows["v-homebrew"]["status"], "cancelled")

    def test_stop_reads_back_what_the_sender_sent(self):
        # The page last saw the row queued; the sender has since sent the first email.
        docs = seed_docs()
        docs["v-homebrew"] = approved(docs["v-homebrew"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
        item = {"slug": "v-homebrew", "to": "hunter@homebrew.example", "status": "queued", "step": 0, "total": 3, "log": [],
                "nextAt": None, "outcome": None, "outcomeAt": None, "error": None, "revision": 1}
        self.mock.status_items = {"v-homebrew": dict(item)}
        self.open(docs, settings=SETTINGS_DECK)
        self.wait_until(lambda: self.mock.calls("status"), "first sync")
        self.settle()
        self.mock.status_items["v-homebrew"] = dict(item, status="active", step=1, nextAt="2026-10-06T02:00:00Z",
                                                    log=[{"step": 0, "at": "2026-10-01T09:12:00Z", "messageId": "<a@x>", "threadId": "t1"}])
        self.show("investor", "all")
        card = self.card("v-homebrew")
        stop = card.locator('[data-act="autostop"]')
        stop.click()
        stop.click()
        self.wait_until(lambda: (self.doc("v-homebrew")["send"]["auto"] or {}).get("status") == "cancelled", "cancelled")
        send = self.doc("v-homebrew")["send"]
        self.assertEqual(send["log"], [{"step": 0, "at": "2026-10-01T09:12:00Z"}])
        self.assertEqual(send["outcome"], "stopped")
        self.assertGreaterEqual(send["auto"]["syncedAt"], send["auto"]["cancelledAt"])
        # Back to manual, the card offers follow-up 1, never a second first email.
        card.locator('[data-act="resume"]').click()
        self.wait_until(lambda: self.doc("v-homebrew")["send"].get("auto", 1) is None, "auto dropped")
        self.assertEqual(self.doc("v-homebrew")["send"]["log"], [{"step": 0, "at": "2026-10-01T09:12:00Z"}])
        expect(card.locator('[data-copy="fu1"]')).to_have_text("复制跟进 1")
        self.assertEqual(card.locator('a[href^="https://mail.google.com/mail/?"]').count(), 0)

    def test_stop_without_read_back_waits_for_the_next_sync(self):
        docs = seed_docs()
        docs["deepseek"] = approved(docs["deepseek"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
        item = {"slug": "deepseek", "to": "shao@deepseek.example", "status": "queued", "step": 0, "total": 3, "log": [],
                "nextAt": None, "outcome": None, "outcomeAt": None, "error": None, "revision": 1}
        self.mock.status_items = {"deepseek": dict(item)}
        page = self.open(docs, settings=SETTINGS_DECK, clock=True, init=FLAKY_FETCH)
        self.wait_until(lambda: self.mock.calls("status"), "first sync")
        self.settle()
        self.mock.status_items["deepseek"] = dict(item, status="active", step=1,
                                                  log=[{"step": 0, "at": "2026-10-01T02:00:00Z", "messageId": "<b@x>", "threadId": "t2"}])
        self.show("customer", "all")
        card = self.card("deepseek")
        stop = card.locator('[data-act="autostop"]')
        stop.click()
        # The cancel lands but the read-back after it fails: no way back to manual yet.
        page.evaluate("window.__passFetch = 1; window.__failFetch = 1")
        stop.click()
        self.wait_until(lambda: self.mock.calls("cancel"), "cancel")
        self.wait_until(lambda: (self.doc("deepseek")["send"]["auto"] or {}).get("status") == "cancelled", "cancelled")
        self.settle()
        self.assertEqual(self.doc("deepseek")["send"].get("log"), [])
        expect(card.locator(".auto-line")).to_contain_text("还没读到停下前发了几封")
        self.assertEqual(card.locator('[data-act="resume"]').count(), 0)
        # The next sync reads it back and only then offers 改为手动发送.
        page.clock.fast_forward("03:05")
        self.wait_until(lambda: self.doc("deepseek")["send"].get("log"), "log read back")
        expect(card.locator('[data-act="resume"]')).to_have_text("改为手动发送")

    # --- link mode (SPEC "Link transport (claude.ai)") ------------------------------------

    def test_link_mode_when_csp_blocks_fetch(self):
        page = self.open_links(seed_docs(), settings=SETTINGS_DECK)
        expect(page.locator("#s-state")).to_have_text(LINK_STATUS)
        # The blocked ping never left the page, and nothing is handed over or written on load.
        self.settle()
        self.assertEqual(self.mock.requests, [])
        self.assertEqual(self.writes(), [])
        expect(page.locator("#s-ping")).to_be_hidden()
        expect(page.locator("#s-test")).to_be_hidden()
        ping, test, dash = page.locator("#s-ping-link"), page.locator("#s-test-link"), page.locator("#s-dash")
        expect(ping).to_have_text("测试连接 ↗")
        expect(test).to_have_text("试发一封给自己 ↗")
        expect(dash).to_have_text("打开发信助手 ↗")
        for a, action in ((ping, "ping"), (test, "test"), (dash, "dashboard")):
            self.assertEqual(a.get_attribute("href"), self.mock.url + "?action=" + action + "&token=" + self.token)
            self.assert_new_tab(a)

        tab = self.click_tab(ping)
        self.assertIn("已连接 business@simreal.co · 今天已发 3/30 · 排队 5 封 · 运行中", tab.content())
        tab = self.click_tab(test)
        self.assertIn("测试邮件已发出", tab.content())
        expect(page.locator("#s-state")).to_contain_text("已在新标签页试发")
        self.assertEqual([(r["via"], r["data"]["action"], r["data"]["token"]) for r in self.mock.requests],
                         [("get", "ping", self.token), ("get", "test", self.token)])
        self.assert_no_post()
        self.assertEqual(page.evaluate("document.querySelectorAll('form').length"), 0)

    def test_link_mode_links_carry_the_finalized_msg(self):
        docs = seed_docs()
        docs["deepseek"] = approved(docs["deepseek"])
        self.open_links(docs, settings=SETTINGS_DECK)
        self.show("investor", "pending")
        link = self.card("v-homebrew").locator('a[data-link="approve"]')
        expect(link).to_have_text("批准并交给发信助手 ↗")
        self.assert_new_tab(link)
        self.assertIn("btn-primary", link.get_attribute("class"))
        self.assertEqual(self.enqueue_link(link.get_attribute("href")),
                         [expected_msg(docs["v-homebrew"], SETTINGS_DECK, "海外（美国）", "America/Los_Angeles")])
        # A refused card keeps the plain 批准 and says why.
        hold = self.card("v-01-advisors")
        expect(hold.locator('[data-act="approve"]')).to_have_text("批准")
        self.assertEqual(hold.locator("a[data-link]").count(), 0)
        expect(hold.locator(".missing", has_text="批准后不会自动发")).to_have_text("批准后不会自动发：暂缓组不自动发送")

        self.show("customer", "todo")
        card = self.card("deepseek")
        link = card.locator('a[data-link="hand"]')
        expect(link).to_have_text("交给发信助手 ↗")
        self.assert_new_tab(link)
        self.assertEqual(self.enqueue_link(link.get_attribute("href")),
                         [expected_msg(docs["deepseek"], SETTINGS_DECK, "国内（杭州）", "Asia/Shanghai")])
        # Until it is handed over, the manual path stays.
        expect(card.locator('a[href^="https://mail.google.com/mail/?"]')).to_have_text("在 Gmail 打开第 1 封")
        expect(card.locator('[data-act="sent"]')).to_have_text("标记已发送")
        # Building links hands nothing over and writes nothing.
        self.settle()
        self.assertEqual(self.mock.requests, [])
        self.assertEqual(self.writes(), [])

    def test_link_without_compression_stream_falls_back_to_j(self):
        docs = seed_docs()
        docs["deepseek"] = approved(docs["deepseek"])
        self.open_links(docs, settings=SETTINGS_DECK, init="window.CompressionStream = undefined;")
        self.show("customer", "todo")
        link = self.card("deepseek").locator('a[data-link="hand"]')
        expect(link).to_have_text("交给发信助手 ↗")
        want = expected_msg(docs["deepseek"], SETTINGS_DECK, "国内（杭州）", "Asia/Shanghai")
        self.assertEqual(self.enqueue_link(link.get_attribute("href"), key="j"), [want])
        self.assertIn("DeepSeek 深度求索（邵智宏（Zhihong Shao））：已加入发送队列", self.click_tab(link).content())
        gets = self.mock.calls("enqueue", via="get")
        self.assertEqual([(g["data"]["encoding"], g["data"]["messages"]) for g in gets], [("j", [want])])
        self.wait_until(lambda: ((self.doc("deepseek").get("send") or {}).get("auto") or {}).get("status") == "handed", "handed")
        self.assertNotIn("review", self.writes()[-1]["data"], "an approved card is only handed over, not approved again")
        self.assert_no_post()

    def test_link_handover_drift_and_stop(self):
        docs = seed_docs()
        page = self.open_links(docs, settings=SETTINGS_DECK)
        self.show("investor", "pending")
        card = self.card("v-homebrew")
        link = card.locator('a[data-link="approve"]')
        sig = link.get_attribute("data-sig")
        want = expected_msg(docs["v-homebrew"], SETTINGS_DECK, "海外（美国）", "America/Los_Angeles")
        text = self.click_tab(link).content()
        self.assertIn("Homebrew（Hunter Walk）：已加入发送队列", text)
        self.assertIn("会在对方当地工作日 8–18 点按分组顺序发出", text)
        gets = self.mock.calls("enqueue")
        self.assertEqual(len(gets), 1)
        self.assertEqual(gets[0]["via"], "get")
        self.assertEqual(gets[0]["data"]["encoding"], "z")
        self.assertEqual(gets[0]["data"]["token"], self.token)
        self.assertEqual(gets[0]["data"]["messages"], [want])
        self.assertEqual(self.mock.rows["v-homebrew"]["status"], "queued")

        # One write: the approval and the handover together.
        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "send.auto")
        writes = [w for w in self.writes() if w["path"] == "prospects/v-homebrew"]
        self.assertEqual(len(writes), 1)
        data = writes[0]["data"]
        at = data["review"]["at"]
        self.assertRegex(at, r"^\d{4}-\d\d-\d\dT")
        self.assertEqual(data, {"review": {"status": "approved", "comment": "", "at": at, "forRevision": 1},
                                "send": {"auto": {"status": "handed", "via": "link", "at": at, "sig": sig, "revision": 1}}})
        expect(page.locator("#toast")).to_contain_text("已在新标签页交给发信助手")

        # Handed: no manual first send, the sender's links, the outcome buttons.
        self.show("investor", "waiting")
        expect(card.locator(".status")).to_have_text("已交给发信助手")
        expect(card.locator(".auto-line")).to_contain_text(HANDED)
        self.assertEqual(card.locator('a[href^="https://mail.google.com/mail/?"]').count(), 0)
        self.assertEqual(card.locator('[data-act="sent"]').count(), 0)
        self.assertEqual(card.locator('[data-act="autostop"]').count(), 0)
        self.assertEqual(card.locator('[data-link="rehand"]').count(), 0)
        expect(card.locator('[data-act="replied"]')).to_have_text("对方已回复")
        expect(card.locator('[data-act="meeting"]')).to_have_text("已约见")
        dash = card.locator("a.btn", has_text="打开发信助手 ↗")
        self.assertEqual(dash.get_attribute("href"), self.mock.url + "?action=dashboard&token=" + self.token)
        self.assert_new_tab(dash)
        stop = card.locator('a[data-link="cancel"]')
        expect(stop).to_have_text("停止自动发送 ↗")
        self.assertEqual(stop.get_attribute("href"), self.mock.url + "?action=cancel&token=" + self.token + "&slug=v-homebrew")
        self.assert_new_tab(stop)

        # A settings change after the handover: the card offers to hand the new text over again.
        page.fill("#f-name-en", "Charlie")
        self.wait_until(lambda: self.store()["settings/sender"].get("nameEn") == "Charlie", "settings saved")
        expect(card.locator(".review-note.warn", has_text="不一样了")).to_contain_text("重新交给发信助手")
        again = card.locator('a[data-link="rehand"]')
        expect(again).to_have_text("重新交给发信助手 ↗")
        charlie = dict(SETTINGS_DECK, nameEn="Charlie")
        self.assertEqual(self.enqueue_link(again.get_attribute("href")),
                         [expected_msg(docs["v-homebrew"], charlie, "海外（美国）", "America/Los_Angeles")])
        sig2 = again.get_attribute("data-sig")
        self.assertNotEqual(sig2, sig)
        # Opening it again is safe: the queued row is updated.
        self.assertIn("Homebrew（Hunter Walk）：已更新", self.click_tab(again).content())
        self.assertEqual(self.mock.rows["v-homebrew"]["msg"]["fromName"], "Charlie")
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"]["sig"] == sig2, "new signature")
        at2 = self.doc("v-homebrew")["send"]["auto"]["at"]
        self.assertEqual(self.writes()[-1], {"op": "update", "path": "prospects/v-homebrew",
                                             "data": {"send": {"auto": {"status": "handed", "via": "link", "at": at2, "sig": sig2, "revision": 1}}}})
        expect(card.locator(".review-note.warn", has_text="不一样了")).to_have_count(0)
        self.assertEqual(card.locator('[data-link="rehand"]').count(), 0)

        # 停止自动发送 ↗ opens the cancel link; the card only records that a stop was asked for.
        self.assertIn("已停止 v-homebrew 的自动发送", self.click_tab(stop).content())
        self.assertEqual([(c["via"], c["data"]["slug"]) for c in self.mock.calls("cancel")], [("get", "v-homebrew")])
        self.assertEqual(self.mock.rows["v-homebrew"]["status"], "cancelled")
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"].get("cancelRequested"), "stop recorded")
        auto = self.doc("v-homebrew")["send"]["auto"]
        self.assertEqual(auto["status"], "handed")
        self.assertRegex(auto["cancelRequested"], r"^\d{4}-\d\d-\d\dT")
        self.assertEqual(self.writes()[-1]["data"], {"send": {"auto": {"cancelRequested": auto["cancelRequested"]}}})
        self.assertNotIn("outcome", self.doc("v-homebrew")["send"])
        expect(card.locator(".auto-line")).to_contain_text(STOP_ASKED)
        self.assertEqual(card.locator('a[data-link="cancel"]').count(), 0)
        # The page cannot tell whether anything went out before the stop: it says what to check,
        # and the card can still go back to manual.
        expect(card.locator(".auto-line .sub")).to_contain_text("停止页写着「队列里没有」，或者发信助手页面上这一封「已发」是 0，才点「改回手动」")
        expect(card.locator('[data-act="resume"]')).to_have_text("改回手动")
        self.assert_no_post()

    def test_link_handover_keeps_a_retry_when_the_approval_write_fails(self):
        page = self.open_links(seed_docs(), settings=SETTINGS_DECK, init=FAILING_REVIEW_WRITES)
        page.evaluate("window.__rejectReview = true")
        self.show("investor", "pending")
        card = self.card("v-homebrew")
        self.click_tab(card.locator('a[data-link="approve"]'))
        self.assertEqual(len(self.mock.calls("enqueue", via="get")), 1)
        note = card.locator(".review-note.warn", has_text="没保存上")
        expect(note).to_contain_text("已在新标签页交给发信助手，但批准没保存上")
        self.assertNotIn("review", self.doc("v-homebrew"))
        self.assertNotIn("send", self.doc("v-homebrew"))
        page.evaluate("window.__rejectReview = false")
        note.locator('[data-act="linkretry"]').click()
        self.wait_until(lambda: (self.doc("v-homebrew").get("review") or {}).get("status") == "approved", "approval saved")
        self.assertEqual(self.doc("v-homebrew")["send"]["auto"]["status"], "handed")
        expect(note).to_have_count(0)
        # The retry only saves; nothing is handed over a second time.
        self.assertEqual(len(self.mock.calls("enqueue")), 1)
        self.assert_no_post()

    def test_link_batch_chunks_cover_exactly_the_eligible_cards(self):
        rnd = random.Random(20261003)

        def noise(n):  # incompressible, so the cards need several links
            return "".join(rnd.choice(string.ascii_letters + string.digits) for _ in range(n))

        def gen(slug, company, order, body, to=None, **kw):
            return approved(base_doc(
                slug=slug, track="customer", company=company, category="测试", region="国内", contact="某人",
                to=("%s@example.com" % slug) if to is None else to, order=order, lang="zh", subject="主题 " + company,
                body="您好，\n\n" + body + "\n\n[姓名]", followups=[{"day": 4, "text": "跟进。[姓名]"}],
                meta_md="- 类别：测试｜地区：国内（北京）"), **kw)

        docs, want = {}, {}
        for i in range(40):
            d = gen("c-gen-%02d" % i, "Gen %02d" % i, 5000 + i, noise(400))
            docs[d["slug"]], want[d["slug"]] = d, expected_msg(d, SETTINGS_DECK, "国内（北京）", "Asia/Shanghai")
        # Its own link cannot fit; no address; already handed over.
        docs["c-long"] = gen("c-long", "Long Co", 4000, noise(7000))
        docs["c-noaddr"] = gen("c-noaddr", "No Addr", 4001, "正文。", to="")
        docs["c-handed"] = gen("c-handed", "Handed Co", 4002, "正文。",
                               auto={"status": "handed", "via": "link", "at": "2026-10-01T08:00:00Z", "sig": "x", "revision": 1})
        page = self.open_links(docs, settings=SETTINGS_DECK)
        self.show("customer", "todo")
        btn = page.locator("#auto-all-btn")
        expect(btn).to_have_text("全部交给发信助手（41 封）")
        expect(page.locator("#auto-hint")).to_contain_text("没有邮箱 1 封")
        long_card = self.card("c-long")
        expect(long_card.locator(".review-note.warn")).to_contain_text("还不能交给发信助手：" + TOO_LONG)
        self.assertEqual(long_card.locator("a[data-link]").count(), 0)
        expect(long_card.locator('[data-act="autosend"]')).to_be_disabled()

        btn.click()
        panel = page.locator("#auto-links")
        expect(panel.locator(".auto-links-note")).to_contain_text("40 封分成")
        expect(panel.locator(".auto-links-note")).to_contain_text("1 封" + TOO_LONG + "：Long Co")
        links = panel.locator('a[data-link="chunk"]')
        n = links.count()
        self.assertGreaterEqual(n, 3)
        chunks = []
        for k in range(n):
            a = links.nth(k)
            self.assert_new_tab(a)
            msgs = self.enqueue_link(a.get_attribute("href"))
            self.assertLessEqual(len(msgs), 50)
            for m in msgs:
                self.assertEqual(m, want[m["slug"]])
            names = [m["company"] for m in msgs]
            expect(a).to_have_text("第 %d 批：%s%s（%d 封） ↗" % (k + 1, "、".join(names[:3]), "…" if len(names) > 3 else "", len(names)))
            chunks.append([m["slug"] for m in msgs])
        seen = [s for c in chunks for s in c]
        self.assertEqual(sorted(seen), sorted(want), "every eligible card exactly once, nothing else")
        self.assertEqual(seen, sorted(seen), "in send order")
        self.settle()
        self.assertEqual(self.mock.requests, [])
        self.assertEqual(self.writes(), [])

        # Opening batch 1 hands over exactly its cards and marks exactly those handed.
        tab = self.click_tab(links.nth(0))
        self.assertEqual(tab.content().count("已加入发送队列"), len(chunks[0]))
        self.assertEqual([[m["slug"] for m in g["data"]["messages"]] for g in self.mock.calls("enqueue", via="get")], [chunks[0]])
        self.wait_until(lambda: len(self.writes()) == len(chunks[0]), "batch marked handed")
        self.assertEqual(sorted(w["path"] for w in self.writes()), sorted("prospects/" + s for s in chunks[0]))
        at = self.writes()[0]["data"]["send"]["auto"]["at"]
        for w in self.writes():
            auto = w["data"]["send"]["auto"]
            self.assertEqual(list(w["data"]), ["send"])
            self.assertEqual(dict(auto, sig=None), {"status": "handed", "via": "link", "at": at, "sig": None, "revision": 1})
            self.assertTrue(auto["sig"])
        expect(panel.locator(".auto-links-row").nth(0)).to_contain_text("已打开")
        expect(links.nth(0)).not_to_have_class(re.compile(r"btn-primary"))
        expect(btn).to_have_text("全部交给发信助手（%d 封）" % (41 - len(chunks[0])))
        # The signature written is the one of the text in the link: the card does not read as drifted.
        self.show("customer", "waiting")
        card = self.card(chunks[0][0])
        expect(card.locator(".auto-line")).to_contain_text(HANDED)
        self.assertEqual(card.locator(".review-note.warn", has_text="不一样了").count(), 0)
        # Opening the same batch again is safe: the sender only updates what is still queued.
        self.show("customer", "todo")
        self.assertEqual(self.click_tab(links.nth(0)).content().count("已更新"), len(chunks[0]))
        self.assert_no_post()

    def test_link_batch_is_made_again_when_its_cards_change(self):
        docs = {d["slug"]: d for d in (customer_doc("c-a", "A Co", 5001), customer_doc("c-b", "B Co", 5002),
                                       customer_doc("c-c", "C Co", 5003))}
        page = self.open_links(docs, settings=SETTINGS_DECK)
        self.show("customer", "todo")
        page.click("#auto-all-btn")
        panel = page.locator("#auto-links")
        links = panel.locator('a[data-link="chunk"]')
        expect(links).to_have_count(1)
        expect(links.nth(0)).to_have_text("第 1 批：A Co、B Co、C Co（3 封） ↗")
        # Approval undone on one card, another sent by hand: neither may go out with the batch.
        self.card("c-a").locator('[data-act="reopen"]').click()
        self.wait_until(lambda: self.doc("c-a")["review"]["status"] == "pending", "approval undone")
        self.card("c-b").locator('[data-act="sent"]').click()
        self.wait_until(lambda: (self.doc("c-b").get("send") or {}).get("log"), "sent by hand")
        expect(links.nth(0)).to_have_text("第 1 批：C Co（1 封） ↗")
        expect(panel.locator(".auto-links-note")).to_contain_text("卡片有变动，已按现在的卡片重新分批")
        self.assertEqual([m["slug"] for m in self.enqueue_link(links.nth(0).get_attribute("href"))], ["c-c"])
        # A settings change after the batch was made: its links carry the new text.
        page.fill("#f-name-zh", "小查")
        self.wait_until(lambda: self.store()["settings/sender"].get("nameZh") == "小查", "settings saved")
        want = expected_msg(docs["c-c"], dict(SETTINGS_DECK, nameZh="小查"), "国内（北京）", "Asia/Shanghai")
        self.wait_until(lambda: links.count() == 1 and self.enqueue_link(links.nth(0).get_attribute("href")) == [want], "new text")
        n = len(self.writes())
        self.click_tab(links.nth(0))
        self.assertEqual([g["data"]["messages"] for g in self.mock.calls("enqueue")], [[want]])
        self.wait_until(lambda: ((self.doc("c-c").get("send") or {}).get("auto") or {}).get("status") == "handed", "c-c handed")
        self.settle()
        self.assertEqual([w["path"] for w in self.writes()[n:]], ["prospects/c-c"])
        self.assertNotIn("send", self.doc("c-a"))
        self.assertNotIn("auto", self.doc("c-b")["send"])
        # Handed over with the text in its link, the opened batch stays as it is.
        expect(panel.locator(".auto-links-row").nth(0)).to_contain_text("已打开")
        self.assert_no_post()

    def test_link_handed_card_says_when_it_may_go_back_to_manual(self):
        docs = seed_docs()
        # Handed over; the sender has sent the first email since, which the page cannot see. Its
        # signature is from other settings, so it can be handed over again.
        docs["v-homebrew"] = approved(docs["v-homebrew"], auto=dict(HANDED_AUTO, sig="old"))
        self.mock.rows["v-homebrew"] = {"status": "active", "sent": 1, "msg": {"followups": [{}, {}], "revision": 1}}
        # Handed over, but the sender never got it.
        docs["deepseek"] = approved(docs["deepseek"], auto=dict(HANDED_AUTO))
        # Handed over, then revised: back for review.
        docs["c-rev"] = customer_doc("c-rev", "Rev Co", 3300, send={"auto": dict(HANDED_AUTO)}, revision=2)
        page = self.open_links(docs, settings=SETTINGS_DECK)

        self.show("investor", "waiting")
        card = self.card("v-homebrew")
        sub = card.locator(".auto-line .sub")
        expect(sub).to_contain_text("新标签页写着「没有完成」，或「跳过」的原因是地址、占位符、暂缓、屏蔽这类，才是没交上")
        expect(sub).to_contain_text("写着「已发出」或「已是…」的，发信助手已经有这一封，改回手动会重复发")
        expect(card.locator('[data-act="resume"]')).to_have_text("没交上，改回手动")
        # Handing it over again gets 跳过 for a card the sender has: the page says what that means.
        text = self.click_tab(card.locator('a[data-link="rehand"]')).content()
        self.assertIn("Homebrew（Hunter Walk）：跳过：已发出 1/3 封（发送中），不会重复发", text)
        expect(page.locator("#toast")).to_contain_text("已在新标签页重新交给发信助手：那一页写着「已更新」才换成了这一版，写着「已发出」的照之前交出去的发")
        self.assertEqual(self.mock.rows["v-homebrew"]["status"], "active")

        # Revised after the handover: the note does not promise the new version replaces the old one,
        # and the card names no button it does not have.
        self.show("customer", "pending")
        card = self.card("c-rev")
        note = card.locator(".review-note.warn", has_text="批准的是")
        expect(note).to_contain_text("发信助手可能已经按批准过的那一版发出：重新批准后，新标签页写着「已更新」才换成了这一版")
        expect(note).not_to_contain_text("重新批准会换成这一版")
        expect(card.locator(".auto-line")).to_contain_text(HANDED)
        self.assertEqual(card.locator(".auto-line .sub").count(), 0)
        self.assertEqual(card.locator('[data-act="resume"]').count(), 0)
        expect(card.locator('a[data-link="approve"]')).to_have_text("批准并交给发信助手 ↗")
        # Stop first, then it can be returned to Claude.
        self.assertEqual(card.locator('[data-act="return"]').count(), 0)
        self.assertIn("没有完成：队列里没有 c-rev。", self.click_tab(card.locator('a[data-link="cancel"]')).content())
        self.wait_until(lambda: self.doc("c-rev")["send"]["auto"].get("cancelRequested"), "stop recorded")
        expect(card.locator('[data-act="return"]')).to_have_text("退回修改")
        self.assertEqual(card.locator('a[data-link="cancel"]').count(), 0)
        expect(note).not_to_contain_text("不想发就点")
        card.locator('[data-act="return"]').click()
        card.locator(".return-form textarea").fill("换一个联系人")
        card.locator('.return-form button[type="submit"]').click()
        self.wait_until(lambda: self.doc("c-rev")["review"]["status"] == "changes", "returned")

        # A stop the sender answered with 队列里没有: the card can go back to manual.
        self.show("customer", "waiting")
        card = self.card("deepseek")
        self.assertIn("没有完成：队列里没有 deepseek。", self.click_tab(card.locator('a[data-link="cancel"]')).content())
        self.wait_until(lambda: self.doc("deepseek")["send"]["auto"].get("cancelRequested"), "stop recorded")
        expect(card.locator(".auto-line")).to_contain_text(STOP_ASKED)
        expect(card.locator(".auto-line .sub")).to_contain_text("停止页写着「队列里没有」")
        card.locator('[data-act="resume"]', has_text="改回手动").click()
        self.wait_until(lambda: self.doc("deepseek")["send"].get("auto", 1) is None, "back to manual")
        self.show("customer", "todo")
        expect(card.locator('a[href^="https://mail.google.com/mail/?"]')).to_have_text("在 Gmail 打开第 1 封")
        expect(card.locator('a[data-link="hand"]')).to_have_text("交给发信助手 ↗")
        # (The 退回 form above is the page's own and never leaves it.)
        self.assertEqual([r for r in self.mock.requests if r["method"] != "GET"], [])

    def test_link_reply_marked_by_hand_keeps_the_stop_link(self):
        docs = seed_docs()
        docs["v-homebrew"] = approved(docs["v-homebrew"], auto=dict(HANDED_AUTO))
        self.mock.rows["v-homebrew"] = {"status": "queued", "msg": {"followups": [{}, {}], "revision": 1}}
        self.open_links(docs, settings=SETTINGS_DECK)
        self.show("investor", "waiting")
        card = self.card("v-homebrew")
        card.locator('[data-act="replied"]').click()
        self.wait_until(lambda: self.doc("v-homebrew")["send"].get("outcome") == "replied", "reply marked")
        self.show("investor", "closed")
        expect(card.locator(".status")).to_have_text("已回复")
        # The sender keeps sending follow-ups until it is stopped.
        stop = card.locator('a[data-link="cancel"]')
        expect(stop).to_have_text("停止自动发送 ↗")
        self.assertEqual(card.locator(".auto-line .sub").count(), 0)
        self.assertIn("已停止 v-homebrew 的自动发送", self.click_tab(stop).content())
        self.assertEqual(self.mock.rows["v-homebrew"]["status"], "cancelled")
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"].get("cancelRequested"), "stop recorded")
        expect(stop).to_have_count(0)
        expect(card.locator(".status")).to_have_text("已回复")
        expect(card.locator('[data-act="resume"]')).to_have_text("撤销「已回复」")
        self.assert_no_post()

    def test_reply_marked_by_hand_keeps_the_stop_button(self):
        docs = seed_docs()
        # Handed over by link and marked 已回复 by hand; this browser can read the sender, still sending.
        docs["v-homebrew"] = approved(docs["v-homebrew"], outcome="replied", outcomeAt="2026-10-02T03:00:00Z", auto=dict(HANDED_AUTO))
        self.mock.status_items["v-homebrew"] = {
            "slug": "v-homebrew", "to": "hunter@homebrew.example", "status": "active", "step": 1, "total": 3,
            "log": [{"step": 0, "at": "2026-10-01T09:12:00Z"}], "nextAt": "2026-10-06T02:00:00Z", "outcome": None,
            "outcomeAt": None, "error": None, "revision": 1}
        self.open(docs, settings=SETTINGS_DECK)
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"]["status"] == "active", "synced")
        self.show("investor", "closed")
        card = self.card("v-homebrew")
        expect(card.locator(".status")).to_have_text("已回复")
        stop = card.locator('[data-act="autostop"]')
        expect(stop).to_have_text("停止自动发送")
        stop.click()
        stop.click()
        self.wait_until(lambda: self.mock.calls("cancel"), "cancel")
        self.wait_until(lambda: self.doc("v-homebrew")["send"]["auto"]["status"] == "cancelled", "cancelled")
        # The reply marked by hand stays.
        self.assertEqual(self.doc("v-homebrew")["send"]["outcome"], "replied")
        expect(card.locator(".status")).to_have_text("已回复")
        expect(card.locator('[data-act="resume"]')).to_have_text("撤销「已回复」")

    def test_sender_links_open_only_by_a_click(self):
        menu = "window.addEventListener('contextmenu', function (e) { window.__menu = e.defaultPrevented; });"
        page = self.open_links(seed_docs(), settings=SETTINGS_DECK, init=menu)
        self.show("investor", "pending")
        link = self.card("v-homebrew").locator('a[data-link="approve"]')
        expect(link).to_have_text("批准并交给发信助手 ↗")
        # The context menu (open in new tab, copy link) would hand it over with nothing recorded.
        link.click(button="right")
        self.wait_until(lambda: page.evaluate("window.__menu === true"), "context menu blocked")
        self.assertFalse(link.evaluate("a => a.dispatchEvent(new DragEvent('dragstart', {bubbles: true, cancelable: true}))"),
                         "dragging the link to the tab bar is blocked")
        self.assertEqual(link.evaluate("a => getComputedStyle(a).userSelect"), "none")
        self.assertRegex(PAGE.read_text(encoding="utf-8"), r"a\[data-link\] \{[^}]*-webkit-touch-callout: none")
        self.settle()
        self.assertEqual(len(self.ctx.pages), 1)
        self.assertEqual(self.mock.requests, [])
        self.assertEqual(self.writes(), [])
        # Other links keep their menu.
        page.evaluate("window.__menu = null")
        page.locator("#s-dash").click(button="right")
        self.wait_until(lambda: page.evaluate("window.__menu === false"), "dashboard link menu")

    def test_follow_up_without_text_or_day_is_not_handed_over(self):
        docs = seed_docs()
        docs["deepseek"] = approved(dict(docs["deepseek"], followups=[{"day": 4, "text": "  "}, docs["deepseek"]["followups"][1]]))
        docs["v-homebrew"] = dict(docs["v-homebrew"], followups=[INVESTOR_FUS[0], dict(INVESTOR_FUS[1], day=0)])
        self.open_links(docs, settings=SETTINGS_DECK)
        self.show("customer", "todo")
        card = self.card("deepseek")
        expect(card.locator(".review-note.warn")).to_contain_text("还不能交给发信助手：跟进 1 是空的或天数不对")
        self.assertEqual(card.locator("a[data-link]").count(), 0)
        self.show("investor", "pending")
        card = self.card("v-homebrew")
        expect(card.locator(".missing", has_text="批准后不会自动发")).to_have_text("批准后不会自动发：跟进 2 是空的或天数不对")
        expect(card.locator('[data-act="approve"]')).to_have_text("批准")
        self.assertEqual(card.locator("a[data-link]").count(), 0)

    def test_link_mode_on_a_phone(self):
        shots = Path(SHOTS) if SHOTS else None
        if shots:
            shots.mkdir(parents=True, exist_ok=True)
        for scheme in ("light", "dark"):
            docs = seed_docs()
            # Handed over before a settings change: all three links show.
            docs["v-homebrew"] = approved(docs["v-homebrew"], auto={"status": "handed", "via": "link", "at": "2026-10-01T08:00:00Z", "sig": "old", "revision": 1})
            docs["v-01-advisors"] = approved(docs["v-01-advisors"])
            docs["deepseek"] = approved(docs["deepseek"])
            page = self.open_links(docs, settings=SETTINGS_DECK, color_scheme=scheme, width=390, height=844)
            self.show("investor", "all")
            card = self.card("v-homebrew")
            expect(card.locator('a[data-link="rehand"]')).to_be_visible()
            expect(card.locator('a[data-link="cancel"]')).to_be_visible()
            expect(card.locator(".auto-line")).to_contain_text(HANDED)
            expect(self.card("v-01-advisors").locator('[data-act="autosend"]')).to_be_disabled()
            self.assert_fits(390, "cards, " + scheme)
            if shots:
                page.locator(".sender").screenshot(path=str(shots / ("link-settings-%s-phone.png" % scheme)))
                page.locator("#panel").screenshot(path=str(shots / ("link-cards-%s-phone.png" % scheme)))
            self.show("customer", "todo")
            page.click("#auto-all-btn")
            expect(page.locator('#auto-links a[data-link="chunk"]')).to_have_count(1)
            self.assert_fits(390, "batch, " + scheme)
            if shots:
                page.locator("#panel").screenshot(path=str(shots / ("link-batch-%s-phone.png" % scheme)))
            self.assert_db_has_no_secret()
            self.ctx.close()
            self.ctx = None
            self.page = None

    def test_transient_fetch_failure_is_reported_and_retried(self):
        docs = seed_docs()
        docs["v-homebrew"] = approved(docs["v-homebrew"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
        self.mock.rows["v-homebrew"] = {"status": "queued", "msg": {"to": "hunter@homebrew.example", "followups": [{}, {}], "revision": 1}}
        page = self.open(docs, settings=SETTINGS_DECK, clock=True, init=FLAKY_FETCH)
        self.wait_until(lambda: self.mock.calls("status"), "first sync")
        page.evaluate("window.__failFetch = 1")
        page.clock.fast_forward("03:05")
        expect(page.locator("#s-sync")).to_have_text("这次同步没连上发信助手，稍后自动再试。")
        self.assertEqual(len(self.mock.calls("status")), 1)
        # The next interval reads again and picks up the reply.
        self.mock.status_items["v-homebrew"] = {
            "slug": "v-homebrew", "to": "hunter@homebrew.example", "status": "replied", "step": 1, "total": 3,
            "log": [{"step": 0, "at": "2026-10-01T09:12:00Z"}], "nextAt": None, "outcome": "replied",
            "outcomeAt": "2026-10-02T09:00:00Z", "error": None, "revision": 1}
        page.clock.fast_forward("03:05")
        self.wait_until(lambda: (self.doc("v-homebrew")["send"]).get("outcome") == "replied", "reply synced")
        self.assertEqual(len(self.mock.calls("status")), 2)

        # A failed ping says what to check, and a failed handover writes nothing and posts no form.
        page.evaluate("window.__failFetch = 1")
        page.click("#s-ping")
        expect(page.locator("#s-state")).to_have_text(NO_LINK)
        expect(page.locator("#s-conn")).to_have_text("连不上")
        page.evaluate("window.__failFetch = 1")
        self.show("customer", "pending")
        self.card("deepseek").locator('[data-act="approve"]').click()
        expect(page.locator("#toast")).to_contain_text("但没交上：连不上发信助手")
        self.settle()
        self.assertEqual(self.mock.calls(via="form"), [])
        self.assertNotIn("send", self.doc("deepseek"))
        self.show("customer", "todo")
        expect(self.card("deepseek").locator('[data-act="autosend"]')).to_be_enabled()
        page.click("#s-ping")
        expect(page.locator("#s-conn")).to_have_text("已连接")

    def test_sync_reconciles_rows_the_cards_do_not_know(self):
        docs = seed_docs()
        # Handed over, but the send.auto write never landed; the sender has sent the first email.
        docs["v-homebrew"] = approved(docs["v-homebrew"])
        self.mock.status_items["v-homebrew"] = {
            "slug": "v-homebrew", "to": "hunter@homebrew.example", "status": "active", "step": 1, "total": 3,
            "log": [{"step": 0, "at": "2026-10-01T09:12:00Z"}], "nextAt": "2026-10-06T02:00:00Z", "outcome": None,
            "outcomeAt": None, "error": None, "revision": 1}
        # Handed over below, then deleted from the sheet by hand.
        docs["deepseek"] = approved(docs["deepseek"])
        # Handed to another deployment, which may still send it: never marked missing from here.
        docs["v-01-advisors"] = approved(docs["v-01-advisors"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1, "via": "elsewhere"})
        # Cancelled at the sender before anything went out, and not on the card.
        docs["c-dup"] = approved(base_doc(
            slug="c-dup", track="customer", company="Dup Co", category="测试", region="国内", contact="某人", to="dup@example.com",
            order=3300, lang="zh", subject="主题", body="您好，\n\n正文。\n\n[姓名]", followups=[{"day": 4, "text": "跟进。[姓名]"}],
            meta_md="- 类别：测试｜地区：国内（北京）"))
        self.mock.rows["c-dup"] = {"status": "cancelled", "msg": {"to": "dup@example.com", "followups": [{}], "revision": 1}}
        page = self.open(docs, settings=SETTINGS_DECK, clock=True)
        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "untracked row picked up")
        home = self.doc("v-homebrew")["send"]
        self.assertEqual(home["auto"]["status"], "active")
        self.assertEqual(home["log"], [{"step": 0, "at": "2026-10-01T09:12:00Z"}])
        self.assertNotIn("send", self.doc("c-dup"), "a cancelled row with nothing sent is not pushed onto a manual card")
        self.show("investor", "waiting")
        card = self.card("v-homebrew")
        expect(card.locator(".status")).to_have_text("自动跟进")
        self.assertEqual(card.locator('a[href^="https://mail.google.com/mail/?"]').count(), 0)

        self.show("customer", "todo")
        card = self.card("deepseek")
        card.locator('[data-act="autosend"]').click()
        self.wait_until(lambda: (self.doc("deepseek").get("send") or {}).get("auto"), "deepseek queued")
        del self.mock.rows["deepseek"]
        page.clock.fast_forward("03:05")
        self.wait_until(lambda: self.doc("deepseek")["send"]["auto"]["status"] == "missing", "missing row marked")
        self.assertEqual(self.doc("v-01-advisors")["send"]["auto"]["status"], "queued")
        expect(card.locator(".status")).to_have_text("发信助手里没有")
        expect(card.locator(".auto-line")).to_contain_text("不会自动发")
        card.locator('[data-act="resume"]').click()
        expect(card.locator('a[href^="https://mail.google.com/mail/?"]')).to_have_text("在 Gmail 打开第 1 封")

        # Handing over a card the sender already has adopts the sender's record.
        dup = self.card("c-dup")
        dup.locator('[data-act="autosend"]').click()
        self.wait_until(lambda: (self.doc("c-dup").get("send") or {}).get("auto"), "duplicate adopted")
        self.assertEqual(self.doc("c-dup")["send"]["auto"]["status"], "cancelled")
        self.show("customer", "all")
        note = dup.locator(".review-note.warn", has_text="发信助手没收")
        expect(note).to_contain_text("卡片已按它的记录更新")
        self.assertNotIn("手动发", note.inner_text())
        # Taken back by hand, it stays manual through later syncs.
        dup.locator('[data-act="resume"]').click()
        self.wait_until(lambda: self.doc("c-dup")["send"].get("auto", 1) is None, "c-dup back to manual")
        n = len(self.mock.calls("status"))
        page.clock.fast_forward("03:05")
        self.wait_until(lambda: len(self.mock.calls("status")) > n, "next sync")
        self.settle()
        self.assertIsNone(self.doc("c-dup")["send"]["auto"])
        self.assertIsNone(self.doc("deepseek")["send"]["auto"])

    def test_revised_after_approval_needs_review_again(self):
        docs = seed_docs()
        revised = dict(docs["v-homebrew"], revision=2, body=docs["v-homebrew"]["body"].replace("Worth 20 minutes", "REVISED. Worth 20 minutes"))
        docs["v-homebrew"] = approved(revised)
        # Already queued with the approved first version.
        docs["deepseek"] = approved(dict(docs["deepseek"], revision=2), auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
        self.mock.rows["deepseek"] = {"status": "queued", "msg": {"to": "shao@deepseek.example", "followups": [{}, {}], "revision": 1}}
        page = self.open(docs, settings=SETTINGS_DECK)
        self.show("investor", "todo")
        expect(page.locator("#auto-all-btn")).to_be_hidden()
        self.show("investor", "pending")
        card = self.card("v-homebrew")
        expect(card.locator(".status")).to_have_text("待审")
        expect(card.locator(".review-note.warn", has_text="批准的是")).to_have_text("批准的是第 1 版，现在是第 2 版，请重新审。")
        card.locator('[data-act="toggle"]').click()
        self.assertEqual(card.locator('a[href^="https://mail.google.com/mail/?"]').count(), 0)
        card.locator('[data-act="approve"]').click()
        self.wait_until(lambda: self.enqueues(), "enqueue after re-approval")
        m = self.enqueues()[0]["messages"][0]
        self.assertEqual(m["revision"], 2)
        self.assertIn("REVISED.", m["body"])
        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "send.auto")
        self.assertEqual(self.doc("v-homebrew")["review"]["forRevision"], 2)

        # The queued card is back for review; approving replaces the queued copy.
        self.show("customer", "pending")
        card = self.card("deepseek")
        expect(card.locator(".review-note.warn", has_text="批准的是")).to_contain_text("重新批准会换成这一版")
        self.assertEqual(card.locator('[data-act="return"]').count(), 0)
        expect(card.locator('[data-act="autostop"]')).to_be_visible()
        card.locator('[data-act="approve"]').click()
        self.wait_until(lambda: len(self.enqueues()) == 2, "second enqueue")
        expect(page.locator("#toast")).to_contain_text("排队中的内容已更新")
        self.wait_until(lambda: self.doc("deepseek")["send"]["auto"]["revision"] == 2, "queued revision 2")

    def test_handed_over_card_locks_address_and_flags_changed_text(self):
        docs = seed_docs()
        docs["p-abaka-ai"] = approved(dict(docs["p-abaka-ai"], toManual="team@abaka.example"))
        page = self.open(docs, settings=SETTINGS_DECK)
        self.show("partner", "todo")
        card = self.card("p-abaka-ai")
        card.locator('[data-act="autosend"]').click()
        self.wait_until(lambda: (self.doc("p-abaka-ai").get("send") or {}).get("auto"), "send.auto")
        self.show("partner", "waiting")
        # The sender has the address now: no edit box, a pointer to stopping instead.
        self.assertEqual(card.locator("input[data-tomanual]").count(), 0)
        expect(card.locator(".addr-note", has_text="已交给发信助手")).to_contain_text("先点「停止自动发送」")
        self.assertEqual(card.locator('[data-act="autosend"]').count(), 0)

        # A settings change after the handover: the card says so and can replace the queued copy.
        page.fill("#f-name-en", "Charlie")
        self.wait_until(lambda: self.store()["settings/sender"].get("nameEn") == "Charlie", "settings saved")
        expect(card.locator(".review-note.warn", has_text="不一样了")).to_contain_text("点「更新排队内容」")
        card.locator('[data-act="autosend"]', has_text="更新排队内容").click()
        self.wait_until(lambda: len(self.enqueues()) == 2, "re-enqueue")
        m = self.enqueues()[1]["messages"][0]
        self.assertTrue(m["body"].endswith("Charlie"))
        self.assertTrue(all(f["text"].endswith("Charlie") for f in m["followups"]))
        expect(page.locator("#toast")).to_contain_text("排队中的内容已更新")
        expect(card.locator(".review-note.warn", has_text="不一样了")).to_have_count(0)
        self.assertEqual(self.mock.rows["p-abaka-ai"]["msg"]["fromName"], "Charlie")

    def test_handover_waits_for_the_approval_write(self):
        page = self.open(seed_docs(), settings=SETTINGS_DECK, init=FAILING_REVIEW_WRITES)
        page.evaluate("window.__rejectReview = true")
        self.show("investor", "pending")
        card = self.card("v-homebrew")
        card.locator('[data-act="approve"]').click()
        expect(page.locator("#notice")).to_contain_text("没保存上（unavailable）")
        self.settle()
        self.assertEqual(self.enqueues(), [])
        self.assertNotIn("review", self.doc("v-homebrew"))
        expect(card.locator('[data-act="approve"]')).to_have_text("批准并自动发送")
        page.evaluate("window.__rejectReview = false")
        card.locator('[data-act="approve"]').click()
        self.wait_until(lambda: self.enqueues(), "enqueue once saved")
        self.assertEqual(self.doc("v-homebrew")["review"]["status"], "approved")

    def test_not_connected_keeps_the_manual_page(self):
        docs = seed_docs()
        docs["deepseek"] = approved(docs["deepseek"])
        page = self.open(docs, settings=SETTINGS_DECK, connected=False)
        self.show("investor", "pending")
        btn = self.card("v-homebrew").locator('[data-act="approve"]')
        expect(btn).to_have_text("批准")
        # Tabs and filters really hide the other cards.
        expect(self.card("deepseek")).to_be_hidden()
        expect(self.card("p-abaka-ai")).to_be_hidden()
        self.show("customer", "todo")
        card = self.card("deepseek")
        link = card.locator('a[href^="https://mail.google.com/mail/?"]')
        expect(link).to_have_text("在 Gmail 打开第 1 封")
        self.assertIn("btn-primary", link.get_attribute("class"))
        body = parse_qs(urlparse(link.get_attribute("href")).query)["body"][0]
        self.assertEqual(body, finalize(docs["deepseek"]["body"], "zh", SETTINGS_DECK))
        expect(card.locator('[data-act="sent"]')).to_have_text("标记已发送")
        expect(card.locator('[data-act="reopen"]')).to_have_text("撤销批准")
        self.assertEqual(card.locator('[data-act="autosend"]').count(), 0)
        self.assertEqual(card.locator(".auto-line").count(), 0)
        self.assertTrue(page.locator("#auto-all-btn").is_hidden())
        self.assertTrue(page.locator("#auto-hint").is_hidden())
        card.locator('[data-act="sent"]').click()
        self.wait_until(lambda: (self.doc("deepseek").get("send") or {}).get("log"), "manual send logged")
        self.show("investor", "pending")
        self.card("v-homebrew").locator('[data-act="approve"]').click()
        self.wait_until(lambda: (self.doc("v-homebrew").get("review") or {}).get("status") == "approved", "approval")
        self.settle()
        self.assertEqual(self.mock.requests, [])
        self.assertNotIn("send", self.doc("v-homebrew"))

    def test_page_works_when_local_storage_throws(self):
        broken = """
          ["getItem", "setItem", "removeItem"].forEach(function (k) {
            Storage.prototype[k] = function () { throw new DOMException("blocked", "SecurityError"); };
          });"""
        page = self.open(seed_docs(), connected=False, init=broken)
        expect(page.locator("#s-conn")).to_have_text("未连接")
        page.fill("#s-url", self.mock.url)
        page.fill("#s-token", self.token)
        page.click("#s-save")
        expect(page.locator("#s-state")).to_contain_text("已连接 business@simreal.co")
        expect(page.locator("#s-state")).to_contain_text("这个浏览器不让保存")
        self.show("investor", "pending")
        expect(self.card("v-homebrew").locator('[data-act="approve"]')).to_have_text("批准并自动发送")

    @unittest.skipUnless(SHOTS, "set PAGE_TEST_SHOTS to write screenshots")
    def test_screenshots(self):
        out = Path(SHOTS)
        out.mkdir(parents=True, exist_ok=True)
        for scheme in ("light", "dark"):
            for width in (1200, 390):
                tag = "%s-%s" % (scheme, "phone" if width < 600 else "desktop")
                docs = seed_docs()
                docs["v-homebrew"] = approved(docs["v-homebrew"], auto={"status": "queued", "queuedAt": "2026-09-30T08:00:00Z", "revision": 1})
                docs["v-01-advisors"] = approved(docs["v-01-advisors"])
                self.mock.status_items = {"v-homebrew": {
                    "slug": "v-homebrew", "status": "active", "step": 1, "total": 3,
                    "log": [{"step": 1, "at": "2026-10-01T09:12:00Z"}], "nextAt": "2026-10-06T02:00:00Z",
                    "outcome": None, "outcomeAt": None, "error": None, "revision": 1}}
                page = self.open(docs, settings=SETTINGS_DECK, color_scheme=scheme, width=width)
                self.wait_until(lambda: len(self.writes()) >= 1, "sync")
                page.click("#s-ping")
                expect(page.locator("#s-state")).to_contain_text("已连接")
                page.locator(".sender").screenshot(path=str(out / ("settings-%s.png" % tag)))
                self.show("investor", "all")
                page.locator("#panel").screenshot(path=str(out / ("cards-%s.png" % tag)))
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                self.assertLessEqual(overflow, 0, "horizontal scroll at %s" % tag)
                self.ctx.close()
                self.ctx = None
                self.page = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
