"""Approval page <-> 发信助手 integration test (SPEC.md, "Approval page integration").

Serves approval/index.html locally, gives it a fake claude.ai runtime (page_fake_claude.js) and a
mock sender (page_mock_sender.py), and drives it in headless Chromium. Nothing is sent anywhere.

    python sender/test/page_test.py              # needs the playwright package
    PAGE_TEST_SHOTS=/some/dir python sender/test/page_test.py   # also writes screenshots

PAGE_TEST_CHROMIUM points at a Chromium binary; without it Playwright's own is used.
"""

import json
import os
import re
import secrets
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import expect, sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from page_mock_sender import MockSender  # noqa: E402

ROOT = HERE.parents[1]
PAGE = ROOT / "approval" / "index.html"
FAKE_JS = HERE / "page_fake_claude.js"
CHROME = os.environ.get("PAGE_TEST_CHROMIUM", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
SHOTS = os.environ.get("PAGE_TEST_SHOTS")
NO_READ = "此浏览器里审批页无法直接读取发信助手状态，请点「打开发信助手」查看。"

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
    """Serves approval/index.html at / inside the skeleton the Artifact tool publishes it in."""

    def __init__(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                if urlparse(self.path).path != "/":
                    self.send_response(404)
                    self.end_headers()
                    return
                html = ('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
                        "</head><body>" + PAGE.read_text(encoding="utf-8") + "</body></html>").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
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
             init=None, clock=False, extra_docs=None):
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
        self.page.goto(self.site.origin + "/")
        self.page.wait_for_selector("article.card")
        return self.page

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

        page.fill("#s-url", self.mock.url)
        page.fill("#s-token", "wrong-token")
        page.click("#s-save")
        expect(page.locator("#s-state")).to_contain_text("口令不对")

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
        self.assertEqual(sorted(self.mock.calls("status")[0]["data"]["slugs"]), sorted(docs))
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
        self.show("partner", "closed")
        card = self.card("p-abaka-ai")
        expect(card.locator(".auto-line")).to_contain_text("发送失败：Invalid To header")
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

    def test_form_fallback_when_fetch_throws(self):
        page = self.open(seed_docs(), settings=SETTINGS_DECK)
        page.evaluate("""url => {
          const real = window.fetch;
          window.fetch = function (u) {
            if (String(u).indexOf(url) === 0) return Promise.reject(new TypeError("Failed to fetch"));
            return real.apply(this, arguments);
          };
        }""", self.mock.url)
        page.click("#s-ping")
        expect(page.locator("#s-state")).to_have_text(NO_READ)

        self.show("investor", "pending")
        with page.expect_popup() as pop:
            self.card("v-homebrew").locator('[data-act="approve"]').click()
        popup = pop.value
        popup.wait_for_load_state()
        forms = self.wait_until(lambda: self.mock.calls(via="form"), "form post")
        self.assertEqual(len(forms), 1)
        self.assertTrue(forms[0]["content_type"].startswith("application/x-www-form-urlencoded"))
        self.assertEqual(list(parse_qs(forms[0]["raw"])), ["payload"])
        payload = json.loads(parse_qs(forms[0]["raw"])["payload"][0])
        self.assertEqual(payload["token"], self.token)
        self.assertEqual(payload["action"], "enqueue")
        self.assertEqual([m["slug"] for m in payload["messages"]], ["v-homebrew"])
        self.assertEqual(payload["messages"][0]["tz"], "America/Los_Angeles")
        self.assertIn(DECK, payload["messages"][0]["body"])
        self.assertEqual(self.mock.calls(via="fetch"), [])
        self.assertIn("已加入发送队列 1 封", popup.content())

        self.wait_until(lambda: (self.doc("v-homebrew").get("send") or {}).get("auto"), "optimistic send.auto")
        doc = self.doc("v-homebrew")
        self.assertEqual(doc["review"]["status"], "approved")
        self.assertEqual(doc["send"]["auto"]["status"], "queued")
        expect(page.locator("#toast")).to_contain_text(NO_READ)
        self.show("investor", "waiting")
        expect(self.card("v-homebrew").locator(".auto-line")).to_contain_text("状态以发信助手页面为准")

    def test_not_connected_keeps_the_manual_page(self):
        docs = seed_docs()
        docs["deepseek"] = approved(docs["deepseek"])
        page = self.open(docs, settings=SETTINGS_DECK, connected=False)
        self.show("investor", "pending")
        btn = self.card("v-homebrew").locator('[data-act="approve"]')
        expect(btn).to_have_text("批准")
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
