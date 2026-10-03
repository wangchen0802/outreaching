/**
 * SimReal 发信助手 — the Apps Script backend. The contract is sender/SPEC.md.
 *
 * The approval page hands approved cards to this web app (doPost: enqueue, cancel, pause, status ...), or,
 * where it can neither fetch nor post (claude.ai), as links the user clicks (doGet: enqueue, cancel, ping,
 * test), each answered with a page in a new tab. A time-driven tick() sends them from the account that deployed it (business@simreal.co) inside each
 * recipient's working hours, threads the follow-ups, and stops a sequence on a reply, a bounce or a cancel.
 * Queue, log and suppression list live in the Google Sheet "SimReal 发信助手".
 *
 * Install (step by step in Chinese: ops/sender-setup.md): new Apps Script project under
 * business@simreal.co, paste this file and appsscript.json, run setup() once, deploy as a web app
 * (execute as me, access: anyone), then paste the /exec URL and the token from the log into the
 * approval page. Tests: node sender/test/run.js
 */

var VERSION = "1.1.0";
var BOOK_NAME = "SimReal 发信助手";
var TAB_QUEUE = "队列";
var TAB_LOG = "记录";
var TAB_SUPPRESS = "屏蔽";

// 队列 columns in sheet order: [key used in the code, Chinese header].
var QUEUE_COLS = [
  ["slug", "slug"], ["status", "状态"], ["to", "收件人"], ["company", "公司"], ["contact", "联系人"],
  ["wave", "分组"], ["lang", "语言"], ["tz", "时区"],
  ["subject", "主题"], ["sent", "已发封数"], ["total", "总封数"], ["nextAt", "下次发送"], ["firstAt", "首封时间"],
  ["lastAt", "最近发送"],
  ["threadId", "threadId"], ["messageId", "最近 Message-ID"], ["outcome", "结果"], ["outcomeAt", "结果时间"],
  ["error", "错误"], ["attempts", "尝试次数"], ["queuedAt", "入队时间"], ["revision", "修订"], ["content", "内容JSON"],
  ["checkedAt", "上次检查"]
];
var TIME_COLS = { nextAt: 1, firstAt: 1, lastAt: 1, outcomeAt: 1, queuedAt: 1, checkedAt: 1 };
var NUMBER_COLS = { wave: 1, sent: 1, total: 1, attempts: 1, revision: 1 };
var LOG_HEADERS = ["时间", "slug", "收件人", "步骤", "事件", "主题", "messageId", "threadId", "说明"];
var SUPPRESS_HEADERS = ["邮箱", "原因", "时间"];
// Text cells are formatted as plain text so Sheets never turns an id into a number or a date.
var TEXT_FORMAT = "@";
var TIME_FORMAT = "yyyy-mm-dd hh:mm";

// Script Properties that setup() creates when missing. TOKEN and SHEET_ID are handled separately.
var DEFAULTS = {
  PAUSED: "false", DAILY_CAP: "10", PER_TICK: "1", MIN_GAP_MINUTES: "4", WINDOW_START: "8", WINDOW_END: "18",
  DOMAIN_GAP_HOURS: "24", FROM_NAME: "", MAX_ATTEMPTS: "3", CHECKS_PER_TICK: "40"
};

var STATUSES = ["queued", "active", "finished", "replied", "bounced", "cancelled", "error"];
var STATUS_LABEL = {
  queued: "排队中", active: "发送中", finished: "序列结束", replied: "已回复", bounced: "退信", cancelled: "已取消",
  error: "发送失败"
};
var EVENT_LABEL = {
  sent: "已发送", replied: "对方回复", bounced: "退信", auto_reply: "自动回复", error: "出错", cancelled: "已取消",
  queued: "入队", updated: "内容更新", test: "测试邮件"
};
var OUTCOMES = ["replied", "bounced", "cancelled"];
var FREE_MAIL = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "icloud.com", "qq.com", "163.com", "126.com", "foxmail.com"];

var MAX_PER_CALL = 60;
var MAX_CHARS = 40000;
var MAX_CELL = 49000; // a Sheets cell holds 50,000 characters; 内容JSON must fit in one
var MINUTE = 60000;
var HOUR = 60 * MINUTE;
var DAY = 24 * HOUR;
var SEQUENCE_GAP = 20 * HOUR; // two emails of one sequence never go out closer than this
var RECHECK_DAYS = 14;

var TO_RE = /^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]{2,}$/;
var PLACEHOLDER_RE = /\[[^\[\]\r\n]{0,80}\]/;
var AUTO_SUBJECT_RE = /out of office|automatic reply|auto(matic)?[- ]?reply|autoreply|自动回复|休假|不在办公室/i;
var BOUNCE_FROM_RE = /^(mailer-daemon|postmaster)@/i;
// A delivery notice about a delay (Gmail keeps trying) is not a bounce; one that reports a failure is.
var DELAY_RE = /\(delay\)|delayed|delivery incomplete|not delivered yet|will retry|will keep trying|temporary problem|延迟|暂未送达|尚未送达|暂时/i;
var FAILURE_RE = /fail|undeliverable|returned|无法送达|退信/i;
var HARD_FAIL_RE = /Invalid To header|Invalid recipient|invalid address/i;
// Send errors that blame the account, not the row (a permission left unticked, a quota, a rate limit).
var ACCOUNT_FAIL_RE = /insufficient|permission|not sufficient|authori[sz]|rate ?limit|quota|exceeded|too many|denied|disabled|not enabled|not configured|has not been used/i;
var CHECK_HEADERS = ["From", "Subject", "Auto-Submitted", "X-Autoreply", "X-Autorespond", "Precedence", "X-Failed-Recipients"];
var BOUNCE_QUERY = "from:(mailer-daemon OR postmaster) newer_than:3d";

var MSG = {
  unauthorized: "口令不对或缺失。请在审批页「发件设置 → 自动发送」里重新粘贴口令。",
  not_set_up: "发信助手还没有初始化。请在 Apps Script 编辑器里运行一次 setup()。",
  busy: "发信助手正在处理另一个任务，请过一会儿再试。"
};

// The one clock. Tests replace it.
function now_() {
  return new Date();
}

// ---- Web app ----

function doPost(e) {
  var form = !!(e && e.parameter && typeof e.parameter.payload === "string");
  var req = null;
  try {
    req = JSON.parse(form ? e.parameter.payload : text_(e && e.postData && e.postData.contents));
  } catch (err) {
    req = null;
  }
  var res = req && typeof req === "object" && !Array.isArray(req) ? post_(req) : fail_("bad_request", "请求内容不是有效的 JSON。");
  return form ? resultPage_(req && req.action, res) : json_(res);
}

// `view(ctx, req, res)`, when given, reshapes the result inside the same run (sender links, linkView_).
function post_(req, view) {
  var denied = authorize_(req.token);
  if (denied) return denied;
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
  } catch (err) {
    return fail_("busy", MSG.busy);
  }
  try {
    return run_(req, view);
  } catch (err) {
    return failFrom_(err);
  } finally {
    lock.releaseLock();
  }
}

var ACTIONS = { ping: ping_, enqueue: enqueue_, cancel: cancel_, pause: pause_, resume: resume_, status: status_, test: test_ };

function run_(req, view) {
  var action = text_(req.action);
  if (!Object.prototype.hasOwnProperty.call(ACTIONS, action)) throw problem_("bad_request", "不认识的操作：" + action);
  var ctx = open_();
  try {
    var res = ACTIONS[action](ctx, req);
    return view ? view(ctx, req, res) : res;
  } finally {
    save_(ctx);
  }
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  var action = text_(p.action) || "dashboard";
  var denied = authorize_(p.token);
  if (action === "status") {
    if (denied) return json_(denied);
    try {
      return json_(status_(open_(), { slugs: p.slugs ? String(p.slugs).split(",") : null }));
    } catch (err) {
      return json_(failFrom_(err));
    }
  }
  if (LINK_ACTIONS.indexOf(action) !== -1) return link_(action, p, denied);
  if (action !== "dashboard") return json_(fail_("bad_request", "不认识的操作：" + action));
  if (denied) return page_("<h1>" + esc_(BOOK_NAME) + "</h1><p>" + esc_(denied.message) + "</p>");
  try {
    return dashboard_(open_(), String(p.token));
  } catch (err) {
    return page_("<h1>" + esc_(BOOK_NAME) + "</h1><p>" + esc_(failFrom_(err).message) + "</p>");
  }
}

function authorize_(token) {
  var expected = PropertiesService.getScriptProperties().getProperty("TOKEN");
  if (!expected) return fail_("not_set_up", MSG.not_set_up);
  if (typeof token !== "string" || !sameText_(token, expected)) return fail_("unauthorized", MSG.unauthorized);
  return null;
}

function sameText_(a, b) {
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function fail_(code, message) {
  return { ok: false, error: code, message: message };
}

// An error that carries one of the envelope codes.
function problem_(code, message) {
  var err = new Error(message);
  err.code = code;
  return err;
}

function failFrom_(err) {
  if (err && err.code) return fail_(err.code, err.message);
  console.error(err && err.stack ? err.stack : errText_(err));
  return fail_("internal", "发信助手内部出错：" + errText_(err));
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// ---- Sender links: GET enqueue, cancel, ping, test ----
// In claude.ai the approval page can neither fetch nor post to this web app, so there each action is a
// link the user clicks. It runs exactly as the POST does (same token check, lock, validation and results)
// and answers with a page in the new tab. Opening a link again is safe: enqueue gives `updated` while the
// row is still queued, and `duplicate` once it has been sent or a newer revision has replaced it.

var LINK_ACTIONS = ["enqueue", "cancel", "ping", "test"];
var LINK_UNREADABLE = "链接里的邮件内容读不出来，可能链接不完整。请回到审批页重新点一次链接。";

function link_(action, p, denied) {
  if (denied) return resultPage_(action, denied);
  var req = { token: p.token, action: action };
  if (action === "cancel") req.slug = p.slug;
  if (action === "enqueue") {
    var data = linkData_(p);
    if (!data) return resultPage_(action, fail_("bad_request", LINK_UNREADABLE), dashboardLink_(p.token));
    req.messages = data.messages;
  }
  var res = post_(req, linkView_);
  return resultPage_(action, res, linkDetails_(action, res) + dashboardLink_(p.token));
}

// The {messages} a link carries: `z` is base64url of gzip(UTF-8 JSON), `j` base64url of the JSON itself.
// Null when it does not decode; nothing has changed then.
function linkData_(p) {
  try {
    var json;
    if (p.z) json = Utilities.ungzip(Utilities.newBlob(base64Url_(p.z), "application/x-gzip")).getDataAsString("UTF-8");
    else if (p.j) json = Utilities.newBlob(base64Url_(p.j)).getDataAsString("UTF-8");
    else return null;
    var data = JSON.parse(json);
    return data && typeof data === "object" && !Array.isArray(data) ? data : null;
  } catch (err) {
    console.warn("发信链接里的内容解不开：" + errText_(err));
    return null;
  }
}

// Bytes of a base64url value with or without its "=" padding: the page sends it, but a link can lose it
// on the way, and the decoder is not documented to do without it.
function base64Url_(s) {
  var t = text_(s).trim().replace(/=+$/, "");
  while (t.length % 4) t += "=";
  return Utilities.base64DecodeWebSafe(t);
}

// What a link's page shows besides the result, read in the same run: the sending rules, each card's
// company and contact, and where a card that was not taken stands now.
function linkView_(ctx, req, res) {
  var out = Object.assign({ conf: ctx.conf }, res);
  if (req.action === "enqueue") {
    out.cards = res.results.map(function (r, i) {
      var m = normalize_(req.messages[i]), row = find_(ctx, r.slug);
      return {
        slug: r.slug, company: m.company, contact: m.contact, result: r.result, reason: r.reason,
        status: row ? row.status : "", sent: row ? row.sent : 0, total: row ? row.total : 0,
        revision: m.revision, held: row ? row.revision : 0
      };
    });
  }
  if (req.action === "cancel") {
    var target = find_(ctx, res.slug);
    out.company = target.company;
    out.contact = target.contact;
  }
  return out;
}

// ---- Actions ----

function ping_(ctx) {
  return {
    ok: true, from: me_(), paused: ctx.conf.paused, dailyCap: ctx.conf.dailyCap, sentToday: sentToday_(ctx),
    counts: counts_(ctx), version: VERSION
  };
}

function enqueue_(ctx, req) {
  var list = req.messages;
  if (!Array.isArray(list)) throw problem_("bad_request", "messages 必须是数组。");
  if (list.length > MAX_PER_CALL) {
    throw problem_("bad_request", "一次最多交 " + MAX_PER_CALL + " 封，这次有 " + list.length + " 封。");
  }
  var msgs = list.map(normalize_);
  msgs.forEach(function (m) {
    if (!m.slug) throw problem_("bad_request", "每封邮件都要有 slug。");
  });
  return { ok: true, results: msgs.map(function (m) { return enqueueOne_(ctx, m); }) };
}

// A row that holds a newer revision is never replaced by an older one: a link is a GET, and the browser
// reloads an old tab by itself (a restored session, a phone reloading a discarded tab).
function enqueueOne_(ctx, m) {
  var row = find_(ctx, m.slug);
  if (row && (row.status !== "queued" || row.sent > 0 || m.revision < row.revision)) {
    return { slug: m.slug, result: "duplicate", reason: null };
  }
  var reason = problemOf_(m) || addressProblem_(ctx, m.slug, m.to, ["queued", "active", "finished", "replied"]);
  if (reason) return { slug: m.slug, result: "rejected", reason: reason };
  var result = row ? "updated" : "queued";
  if (!row) {
    row = blankRow_(m.slug, ctx.now);
    ctx.rows.push(row);
    ctx.added.push(row);
  }
  fill_(row, m);
  log_(ctx, result, row, { subject: m.subject, note: "修订 " + m.revision });
  return { slug: m.slug, result: result, reason: null };
}

function cancel_(ctx, req) {
  var slug = text_(req.slug).trim();
  if (!slug) throw problem_("bad_request", "缺少 slug。");
  var row = find_(ctx, slug);
  if (!row) throw problem_("bad_request", "队列里没有 " + slug + "。");
  if (row.status === "queued" || row.status === "active") {
    stop_(row, "cancelled", ctx.now);
    log_(ctx, "cancelled", row, { note: "停止自动发送" });
  }
  return { ok: true, slug: slug, status: row.status };
}

function pause_(ctx) {
  return setPaused_(ctx, true);
}

function resume_(ctx) {
  return setPaused_(ctx, false);
}

function setPaused_(ctx, paused) {
  ctx.props.setProperty("PAUSED", paused ? "true" : "false");
  ctx.conf.paused = paused;
  return { ok: true, paused: paused };
}

function status_(ctx, req) {
  var want = Array.isArray(req.slugs) ? req.slugs.map(function (s) { return text_(s).trim(); }) : null;
  var sent = sentLogs_(ctx);
  var items = ctx.rows.filter(function (row) {
    return !want || want.indexOf(row.slug) !== -1;
  }).map(function (row) {
    return item_(row, sent[row.slug] || []);
  });
  return {
    ok: true, paused: ctx.conf.paused, sentToday: sentToday_(ctx), dailyCap: ctx.conf.dailyCap, now: iso_(ctx.now),
    items: items
  };
}

// Log steps are 0-based like the approval page's send.log: 0 = first email, k = follow-up k.
function item_(row, sent) {
  return {
    slug: row.slug, to: row.to, status: row.status, step: row.sent, total: row.total,
    log: sent.map(function (e) {
      return { step: Number(e.step), at: iso_(e.at), messageId: e.messageId, threadId: e.threadId };
    }),
    nextAt: iso_(row.nextAt), outcome: outcomeOf_(row), outcomeAt: iso_(row.outcomeAt), error: row.error || null,
    revision: row.revision
  };
}

function outcomeOf_(row) {
  if (OUTCOMES.indexOf(row.status) !== -1) return row.status;
  return OUTCOMES.indexOf(row.outcome) !== -1 ? row.outcome : null;
}

function test_(ctx) {
  var me = me_(), tz = Session.getScriptTimeZone();
  var subject = "SimReal 发信助手测试";
  var body = "这是一封测试邮件。\n\n能收到它，说明发信助手已经设置好，可以从 " + me + " 发出审批通过的邮件。\n\n发送时间：" +
    Utilities.formatDate(new Date(ctx.now), tz, "yyyy-MM-dd HH:mm:ss") + "（" + tz + "）\n";
  var res;
  try {
    res = Gmail.Users.Messages.send({ raw: raw_({ fromName: ctx.conf.fromName, from: me, to: me, subject: subject, body: body }) }, "me");
  } catch (err) {
    throw problem_("internal", "测试邮件没有发出：" + errText_(err));
  }
  log_(ctx, "test", null, {
    to: me, subject: subject, messageId: res.id, threadId: res.threadId, note: "测试邮件，不计入每日上限"
  });
  return { ok: true, messageId: res.id, threadId: res.threadId };
}

// ---- Validation (at enqueue, and again before every send) ----

function normalize_(raw) {
  var m = raw && typeof raw === "object" ? raw : {};
  var wave = Number(m.wave), order = Number(m.order);
  return {
    slug: text_(m.slug).trim(),
    track: text_(m.track).trim(),
    company: oneLine_(m.company).trim(),
    contact: oneLine_(m.contact).trim(),
    to: text_(m.to).trim().toLowerCase(),
    subject: oneLine_(m.subject).trim(),
    body: text_(m.body),
    followups: (Array.isArray(m.followups) ? m.followups : []).map(function (f) {
      f = f && typeof f === "object" ? f : {};
      return { day: Number(f.day), text: text_(f.text) };
    }),
    lang: text_(m.lang).trim(),
    region: text_(m.region).trim(),
    tz: text_(m.tz).trim(),
    wave: m.wave == null || m.wave === "" || !isFinite(wave) ? 2 : wave,
    order: m.order == null || m.order === "" || !isFinite(order) ? 0 : order,
    revision: Number(m.revision) || 0,
    fromName: oneLine_(m.fromName).trim()
  };
}

// The checks that need no sheet. A follow-up without text or without a positive day counts as "empty".
function problemOf_(m) {
  if (!TO_RE.test(m.to)) return "invalid_to";
  if (!m.subject.trim() || !m.body.trim()) return "empty";
  for (var i = 0; i < m.followups.length; i++) {
    if (!m.followups[i].text.trim() || !(m.followups[i].day > 0)) return "empty";
  }
  var texts = [m.subject, m.body].concat(m.followups.map(function (f) { return f.text; }));
  for (var j = 0; j < texts.length; j++) {
    var ph = PLACEHOLDER_RE.exec(texts[j]);
    if (ph) return "placeholder:" + ph[0];
  }
  var size = texts.reduce(function (n, t) { return n + t.length; }, 0);
  if (size > MAX_CHARS || JSON.stringify(contentOf_(m)).length > MAX_CELL) return "too_long";
  if (m.wave === 9) return "wave_hold";
  return "";
}

// Suppression list, then: the same person never gets two sequences. A row that already sent an email
// counts whatever its status (a cancelled or failed sequence still reached them).
function addressProblem_(ctx, slug, to, statuses) {
  if (Object.prototype.hasOwnProperty.call(ctx.suppressed, to)) return "suppressed";
  for (var i = 0; i < ctx.rows.length; i++) {
    var r = ctx.rows[i];
    if (r.slug !== slug && r.to === to && (statuses.indexOf(r.status) !== -1 || r.sent > 0)) return "address_in_use:" + r.slug;
  }
  return "";
}

function contentOf_(m) {
  return {
    subject: m.subject, body: m.body, followups: m.followups, fromName: m.fromName, track: m.track, order: m.order,
    region: m.region
  };
}

function content_(row) {
  try {
    var c = JSON.parse(row.content);
    return c && typeof c === "object" ? c : null;
  } catch (err) {
    return null;
  }
}

// What is sent comes from 内容JSON plus the 收件人 and 分组 cells; 主题 is a copy for reading.
function msgOf_(row) {
  var c = content_(row);
  if (!c) return null;
  var m = normalize_(c);
  m.slug = row.slug;
  m.to = text_(row.to).trim().toLowerCase();
  m.wave = row.wave;
  return m;
}

function revalidate_(ctx, row) {
  var m = msgOf_(row);
  if (!m) return "内容JSON 无法解析";
  if (row.sent > 0 && !m.followups[row.sent - 1]) return "内容JSON 里没有跟进 " + row.sent;
  return problemOf_(m) || addressProblem_(ctx, row.slug, m.to, ["active", "finished", "replied"]);
}

// ---- tick: every 5 minutes ----

function tick() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) {
    console.log("tick：另一个任务正在运行，这一轮跳过。");
    return;
  }
  try {
    console.log(runTick_());
  } catch (err) {
    if (err && err.code === "not_set_up") console.log("tick：" + err.message);
    else throw err;
  } finally {
    lock.releaseLock();
  }
}

function runTick_() {
  var ctx = open_();
  try {
    checkReplies_(ctx);
    checkBounceMail_(ctx);
    if (ctx.conf.paused) ctx.stats.held = "已暂停，只检查回复";
    else sendDue_(ctx);
  } finally {
    save_(ctx);
  }
  return summary_(ctx);
}

function summary_(ctx) {
  var s = ctx.stats;
  return "tick " + Utilities.formatDate(new Date(ctx.now), Session.getScriptTimeZone(), "MM-dd HH:mm") +
    "：检查 " + s.checked + " 个会话，发出 " + s.sent + " 封，回复 " + s.replied + "，退信 " + s.bounced +
    "，自动回复 " + s.autoReplies + "，失败 " + s.failed + (s.held ? "；" + s.held : "");
}

// Step 2: round-robin over live threads, least recently checked first.
function checkReplies_(ctx) {
  var since = ctx.now - RECHECK_DAYS * DAY;
  var live = ctx.rows.filter(function (row) {
    if (!row.threadId) return false;
    return row.status === "active" || (row.status === "finished" && row.lastAt != null && row.lastAt >= since);
  });
  live.sort(function (a, b) { return (a.checkedAt || 0) - (b.checkedAt || 0); });
  live.slice(0, Math.max(0, ctx.conf.checksPerTick)).forEach(function (row) {
    checkRow_(ctx, row);
  });
}

// Reads one row's threads and applies what it finds, then looks for mail from the recipient that Gmail
// filed elsewhere. Returns false when Gmail could not be read.
function checkRow_(ctx, row) {
  var previous = row.checkedAt, msgs = [];
  row.checkedAt = ctx.now;
  row._dirty = true;
  try {
    threadIds_(row).forEach(function (id) {
      var thread = Gmail.Users.Threads.get("me", id, { format: "metadata", metadataHeaders: CHECK_HEADERS });
      msgs = msgs.concat(thread.messages || []);
    });
  } catch (err) {
    console.warn("读不到 " + row.slug + " 的邮件线程：" + errText_(err));
    return false;
  }
  ctx.stats.checked++;
  msgs.sort(function (a, b) {
    return Number(a.internalDate) - Number(b.internalDate);
  });
  for (var i = 0; i < msgs.length; i++) {
    var msg = msgs[i], at = Number(msgs[i].internalDate);
    if (!(at > (row.firstAt || 0))) continue;
    var from = addressOf_(header_(msg, "From"));
    if (!from || isOwn_(ctx, from)) continue;
    var subject = header_(msg, "Subject");
    if (BOUNCE_FROM_RE.test(from)) {
      if (isDelayNotice_(msg)) continue; // Gmail is still trying to deliver it
      bounce_(ctx, row, at, subject);
      return true;
    }
    if (isAutoReply_(msg)) {
      if (previous == null || at > previous) {
        ctx.stats.autoReplies++;
        log_(ctx, "auto_reply", row, { subject: subject, messageId: msg.id, note: "来自 " + from + "，序列继续" });
      }
      continue;
    }
    stop_(row, "replied", at);
    ctx.stats.replied++;
    log_(ctx, "replied", row, { subject: subject, messageId: msg.id, note: "来自 " + from });
    return true;
  }
  return replyElsewhere_(ctx, row);
}

// Mail from the recipient outside our threads also stops the sequence: Gmail splits off a reply whose
// subject starts "AW:" or "SV:", and people write fresh emails. An auto-reply there does not count.
function replyElsewhere_(ctx, row) {
  if (isOwn_(ctx, row.to)) return true;
  try {
    var hits = Gmail.Users.Messages.list("me", {
      q: "from:" + row.to + " after:" + Math.floor((row.firstAt || 0) / 1000), maxResults: 5
    }).messages || [];
    for (var i = 0; i < hits.length; i++) {
      var msg = Gmail.Users.Messages.get("me", hits[i].id, { format: "metadata", metadataHeaders: CHECK_HEADERS });
      var at = Number(msg.internalDate);
      if (!(at > (row.firstAt || 0)) || isAutoReply_(msg)) continue;
      stop_(row, "replied", at);
      ctx.stats.replied++;
      log_(ctx, "replied", row, { subject: header_(msg, "Subject"), messageId: msg.id, note: "来自 " + row.to + "（另一个会话）" });
      return true;
    }
  } catch (err) {
    console.warn("搜索 " + row.to + " 的来信失败：" + errText_(err));
    return false;
  }
  return true;
}

// A row's threads: the first email's, then any a follow-up landed in instead (space-separated).
function threadIds_(row) {
  return text_(row.threadId).split(/\s+/).filter(Boolean);
}

// No X-Failed-Recipients, no failure in the subject, and it speaks of a delay or a retry.
function isDelayNotice_(msg) {
  var subject = header_(msg, "Subject");
  if (header_(msg, "X-Failed-Recipients") || FAILURE_RE.test(subject)) return false;
  return DELAY_RE.test(subject) || DELAY_RE.test(text_(msg.snippet));
}

function isAutoReply_(msg) {
  var submitted = findHeader_(msg, "Auto-Submitted");
  if (submitted && text_(submitted.value).trim().toLowerCase() !== "no") return true;
  if (findHeader_(msg, "X-Autoreply") || findHeader_(msg, "X-Autorespond")) return true;
  if (header_(msg, "Precedence").trim().toLowerCase() === "auto_reply") return true;
  return AUTO_SUBJECT_RE.test(header_(msg, "Subject"));
}

function bounce_(ctx, row, at, subject) {
  stop_(row, "bounced", at);
  suppress_(ctx, row.to, "退信（" + row.slug + "）");
  ctx.stats.bounced++;
  log_(ctx, "bounced", row, { subject: subject, note: "退信，地址已加入屏蔽" });
}

// Bounces that Gmail did not file in our thread.
function checkBounceMail_(ctx) {
  var live = ctx.rows.filter(function (row) {
    return (row.status === "active" || row.status === "finished") && row.firstAt != null;
  });
  if (!live.length) return;
  var list;
  try {
    list = Gmail.Users.Messages.list("me", { q: BOUNCE_QUERY, maxResults: 20 });
  } catch (err) {
    console.warn("搜索退信失败：" + errText_(err));
    return;
  }
  (list.messages || []).forEach(function (hit) {
    var msg;
    try {
      msg = Gmail.Users.Messages.get("me", hit.id, { format: "metadata", metadataHeaders: ["From", "Subject", "X-Failed-Recipients"] });
    } catch (err) {
      console.warn("读不到退信 " + hit.id + "：" + errText_(err));
      return;
    }
    if (isDelayNotice_(msg)) return;
    var at = Number(msg.internalDate), snippet = text_(msg.snippet).toLowerCase();
    var failed = header_(msg, "X-Failed-Recipients").toLowerCase().split(/[\s,;]+/);
    live.forEach(function (row) {
      if (row.status !== "active" && row.status !== "finished") return;
      if (!(at > row.firstAt)) return;
      if (failed.indexOf(row.to) === -1 && !mentions_(snippet, row.to)) return;
      bounce_(ctx, row, at, header_(msg, "Subject"));
    });
  });
}

// Whole-address match: "a@b.co" is not found inside "xa@b.com".
function mentions_(text, addr) {
  var i = text.indexOf(addr);
  while (i !== -1) {
    var before = i ? text.charAt(i - 1) : "", after = text.substr(i + addr.length, 2);
    if (!/[a-z0-9._%+\-]/.test(before) && !/^([a-z0-9_\-]|\.[a-z0-9])/.test(after)) return true;
    i = text.indexOf(addr, i + 1);
  }
  return false;
}

// Steps 4–6: due follow-ups first, then first emails by wave and order.
function sendDue_(ctx) {
  var list = dueFollowups_(ctx).concat(queuedInOrder_(ctx));
  var done = 0, held = list.length ? held_(ctx) : "";
  for (var i = 0; i < list.length && done < ctx.conf.perTick; i++) {
    if (held) {
      ctx.stats.held = held;
      return;
    }
    var row = list[i];
    if (!inWindow_(ctx, row.tz)) continue;
    if (row.sent === 0) {
      if (row.status !== "queued" || !domainClear_(ctx, row)) continue;
    } else if (!checkRow_(ctx, row) || row.status !== "active") {
      continue; // 4b: a reply that came in since the last round-robin check stops the follow-up
    }
    if (liveStatus_(ctx, row) !== row.status) continue; // cancelled or deleted by hand during this run
    var bad = revalidate_(ctx, row);
    if (bad) {
      stop_(row, "error", ctx.now);
      row.error = "发送前检查不通过：" + bad;
      log_(ctx, "error", row, { step: row.sent, note: row.error });
      continue;
    }
    if (sentAlready_(ctx, row)) {
      held = held_(ctx);
      continue;
    }
    if (row.sent > 0 && !previousMessageId_(ctx, row)) {
      // Without In-Reply-To Gmail opens a new thread, where a reply would go unseen.
      row.error = "读不到上一封的 Message-ID，这封跟进下一轮再发";
      row._dirty = true;
      console.warn(row.slug + "：" + row.error);
      continue;
    }
    sendStep_(ctx, row);
    done++;
    held = ctx.stats.held || held_(ctx);
  }
}

// 状态 as the sheet has it now ("" when the row is gone): Charles may have cancelled or deleted the row
// by hand while this run was reading Gmail.
function liveStatus_(ctx, row) {
  var last = ctx.queue.getLastRow();
  var cells = last < 2 ? [] : ctx.queue.getRange(2, 1, last - 1, 2).getValues();
  for (var i = 0; i < cells.length; i++) {
    if (text_(cells[i][0]).trim() === row.slug) return text_(cells[i][1]).trim().toLowerCase();
  }
  return "";
}

// Whether this step already went out, recording it if so: 记录 has it (a run that stopped before it
// wrote the row), or, after a failed attempt, Sent has it (Gmail took it although the call threw).
// Also true when Sent cannot be searched: the row waits a tick rather than risk a second copy.
function sentAlready_(ctx, row) {
  var logged = (sentLogs_(ctx)[row.slug] || []).filter(function (e) {
    return e.step !== "" && Number(e.step) === row.sent;
  })[0];
  if (logged) {
    markSent_(ctx, row, { id: logged.messageId, threadId: logged.threadId, at: logged.at });
    return true;
  }
  if (!(row.attempts > 0)) return false;
  var subject = subjectOf_(msgOf_(row), row.sent), found;
  try {
    found = findSent_(ctx, row, subject);
  } catch (err) {
    console.warn("查不到 " + row.slug + " 上次报错的那封是否已发出，这一轮先不发：" + errText_(err));
    return true;
  }
  if (found) recordSent_(ctx, row, found, subject, "上次发送报错，但这封已在「已发送」里");
  return !!found;
}

// A message in Sent to this recipient with this step's subject that 记录 does not know yet. Throws
// when Gmail cannot be searched.
function findSent_(ctx, row, subject) {
  var since = row.sent ? row.lastAt : row.queuedAt, known = {};
  (sentLogs_(ctx)[row.slug] || []).forEach(function (e) { known[e.messageId] = true; });
  var q = "in:sent to:" + row.to + (since ? " after:" + Math.floor(since / 1000) : "");
  var hits = Gmail.Users.Messages.list("me", { q: q, maxResults: 10 }).messages || [];
  for (var i = 0; i < hits.length; i++) {
    if (known[hits[i].id]) continue;
    var msg = Gmail.Users.Messages.get("me", hits[i].id, { format: "metadata", metadataHeaders: ["To", "Subject"] });
    if (mentions_(header_(msg, "To").toLowerCase(), row.to) && sameSubject_(header_(msg, "Subject"), subject)) {
      return { id: msg.id, threadId: msg.threadId, at: Number(msg.internalDate) };
    }
  }
  return null;
}

// Gmail may hand a header back decoded or still RFC 2047-encoded.
function sameSubject_(got, want) {
  function norm(s) {
    return text_(s).replace(/\s+/g, " ").trim();
  }
  return norm(got) === norm(want) || norm(got) === norm(headerText_(want));
}

function subjectOf_(m, step) {
  return step ? "Re: " + m.subject : m.subject;
}

function held_(ctx) {
  var conf = ctx.conf, today = sentToday_(ctx);
  if (today >= conf.dailyCap) return "今天已发 " + today + " 封，到每日上限 " + conf.dailyCap;
  var last = lastSend_(ctx);
  if (last != null && ctx.now - last < conf.minGap * MINUTE) return "距上一封不到 " + conf.minGap + " 分钟";
  return "";
}

function dueFollowups_(ctx) {
  var due = [];
  ctx.rows.forEach(function (row) {
    if (row.status !== "active" || !(row.sent >= 1) || row.firstAt == null) return;
    var c = content_(row);
    if (c && row.sent >= 1 + (Array.isArray(c.followups) ? c.followups.length : 0)) {
      row.status = "finished"; // follow-ups removed by hand: nothing left to send
      row.nextAt = null;
      row._dirty = true;
      return;
    }
    var at = followupDue_(row, c);
    if (at <= ctx.now) due.push({ row: row, at: at });
  });
  due.sort(function (a, b) { return a.at - b.at; });
  return due.map(function (d) { return d.row; });
}

// When the next follow-up of an active row may go out. Unreadable content or a bad day counts as
// due at once, so that the re-validation turns the row into an error.
function followupDue_(row, c) {
  var day = c ? Number(c.followups[row.sent - 1] && c.followups[row.sent - 1].day) : NaN;
  if (!(day > 0)) return row.firstAt;
  return Math.max(row.firstAt + day * DAY, (row.lastAt || 0) + SEQUENCE_GAP);
}

function queuedInOrder_(ctx) {
  var list = ctx.rows.filter(function (row) { return row.status === "queued" && row.sent === 0; });
  var order = {};
  list.forEach(function (row) {
    var c = content_(row);
    order[row.slug] = c && isFinite(Number(c.order)) ? Number(c.order) : 0;
  });
  return list.sort(function (a, b) {
    return (a.wave - b.wave) || (order[a.slug] - order[b.slug]) || ((a.queuedAt || 0) - (b.queuedAt || 0));
  });
}

// Monday–Friday, WINDOW_START <= hour < WINDOW_END, in the recipient's timezone. Cached per zone.
function inWindow_(ctx, tz) {
  var zone = tz || Session.getScriptTimeZone();
  if (!Object.prototype.hasOwnProperty.call(ctx.windows, zone)) {
    var at = new Date(ctx.now);
    var day = weekday_(at, zone), hour = Number(Utilities.formatDate(at, zone, "H"));
    ctx.windows[zone] = day >= 1 && day <= 5 && hour >= ctx.conf.windowStart && hour < ctx.conf.windowEnd;
  }
  return ctx.windows[zone];
}

// The weekday in that zone, 1 = Monday … 7 = Sunday, worked out from the local calendar date. The
// pattern letter "u" is not relied on: date formatters disagree on it (in ICU it is the year).
function weekday_(date, tz) {
  var ymd = Utilities.formatDate(date, tz, "yyyy-MM-dd").split("-");
  var day = new Date(Date.UTC(Number(ymd[0]), Number(ymd[1]) - 1, Number(ymd[2]))).getUTCDay();
  return day === 0 ? 7 : day;
}

function domainClear_(ctx, row) {
  var domain = domainOf_(row.to);
  if (FREE_MAIL.indexOf(domain) !== -1) return true;
  var since = ctx.now - ctx.conf.domainGap * HOUR;
  return !ctx.rows.some(function (r) {
    return r !== row && r.firstAt != null && r.firstAt > since && domainOf_(r.to) === domain;
  });
}

function lastSend_(ctx) {
  var last = null;
  ctx.rows.forEach(function (row) {
    if (row.lastAt != null && (last == null || row.lastAt > last)) last = row.lastAt;
  });
  return last;
}

// Step 5: one email of one sequence. Returns true when Gmail accepted it.
function sendStep_(ctx, row) {
  var m = msgOf_(row), step = row.sent, first = step === 0, threads = threadIds_(row);
  var subject = subjectOf_(m, step);
  var resource = {
    raw: raw_({
      fromName: m.fromName || ctx.conf.fromName, from: me_(), to: m.to, subject: subject,
      body: first ? m.body : m.followups[step - 1].text, inReplyTo: first ? "" : previousMessageId_(ctx, row)
    })
  };
  if (!first && threads.length) resource.threadId = threads[threads.length - 1];
  var res;
  try {
    res = Gmail.Users.Messages.send(resource, "me");
  } catch (err) {
    return sendFailed_(ctx, row, step, subject, err);
  }
  recordSent_(ctx, row, { id: res.id, threadId: res.threadId, at: ctx.now }, subject, first ? "第 1 封" : "跟进 " + step);
  ctx.stats.sent++;
  return true;
}

// The email is out: Script Properties hold it before anything else can fail (see remember_), then the
// row and 记录 take it.
function recordSent_(ctx, row, sent, subject, note) {
  var step = row.sent;
  remember_(ctx, { slug: row.slug, step: step, id: sent.id, threadId: sent.threadId, at: sent.at, subject: subject });
  sent.messageId = messageIdOf_(sent.id);
  markSent_(ctx, row, sent);
  log_(ctx, "sent", row, { at: sent.at, step: step, subject: subject, messageId: sent.id, threadId: sent.threadId, note: note });
}

// Moves the row past the step that went out as Gmail message `sent` ({id, threadId, at, messageId}).
// An empty messageId is looked up again before the next follow-up (previousMessageId_).
function markSent_(ctx, row, sent) {
  var m = msgOf_(row), first = row.sent === 0, threads = threadIds_(row);
  row.sent++;
  if (m) row.total = 1 + m.followups.length;
  row.lastAt = sent.at;
  if (first) {
    row.firstAt = sent.at;
    row.threadId = text_(sent.threadId);
  } else if (sent.threadId && threads.indexOf(sent.threadId) === -1) {
    row.threadId = threads.concat(sent.threadId).join(" ");
    console.warn(row.slug + " 的跟进进了新的会话 " + sent.threadId + "，以后两个会话都检查回复。");
  }
  row.messageId = text_(sent.messageId);
  if (row.status === "queued" || row.status === "active") row.status = row.sent >= row.total ? "finished" : "active";
  row.error = "";
  row.attempts = 0;
  row.nextAt = m ? nextAt_(row, m) : null;
  row._dirty = true;
}

// Sends the sheet does not show yet live in Script Properties, which do not depend on the sheet, until
// save_ has written them. A run that dies or cannot write the sheet is replayed by the next (replay_),
// so the row never sends that email again.
function remember_(ctx, entry) {
  ctx.inflight.push(entry);
  try {
    ctx.props.setProperty("INFLIGHT", JSON.stringify(ctx.inflight));
  } catch (err) {
    console.warn("暂存刚发出的邮件失败，只能靠表格记下它：" + errText_(err));
  }
}

// Replays the sends a failed run left in Script Properties: rows and 记录 catch up, nothing is sent.
function replay_(ctx) {
  var list;
  try {
    list = JSON.parse(ctx.props.getProperty("INFLIGHT") || "[]");
  } catch (err) {
    list = [];
  }
  if (!Array.isArray(list) || !list.length) return;
  var logged = sentLogs_(ctx);
  list.forEach(function (e) {
    var row = find_(ctx, e.slug);
    if (!row) {
      console.warn("队列里找不到 " + e.slug + "，它已发出的第 " + (e.step + 1) + " 封没能补记。");
      return;
    }
    if (row.sent === e.step) markSent_(ctx, row, e);
    var known = (logged[e.slug] || []).some(function (x) { return x.messageId === e.id; });
    if (!known) {
      log_(ctx, "sent", row, {
        at: e.at, step: e.step, subject: e.subject, messageId: e.id, threadId: e.threadId, note: "补记：发出后上一轮没能写进表格"
      });
    }
  });
  ctx.inflight = list;
}

function nextAt_(row, m) {
  if (row.status !== "active") return null;
  var f = m.followups[row.sent - 1];
  return f ? Math.max(row.firstAt + f.day * DAY, row.lastAt + SEQUENCE_GAP) : null;
}

function sendFailed_(ctx, row, step, subject, err) {
  var text = errText_(err), hard = HARD_FAIL_RE.test(text);
  if (!hard && ACCOUNT_FAIL_RE.test(text)) {
    // Not this row's fault: count no attempt, send nothing more this tick, try again next tick.
    if (row.error !== text) log_(ctx, "error", row, { step: step, note: "发信账号出错，暂停到下一轮：" + text });
    row.error = text;
    row._dirty = true;
    ctx.stats.failed++;
    ctx.stats.held = "发信账号出错：" + text;
    return false;
  }
  if (!hard) {
    // "Empty response" or a timeout can come after Gmail took the message.
    var found = null;
    try {
      found = findSent_(ctx, row, subject);
    } catch (e) {
      console.warn("查不到 " + row.slug + " 这封是否已发出：" + errText_(e));
    }
    if (found) {
      recordSent_(ctx, row, found, subject, "发送时报错（" + text + "），但这封已在「已发送」里");
      ctx.stats.sent++;
      return true;
    }
  }
  row.attempts = (row.attempts || 0) + 1;
  row.error = text;
  var final = hard || row.attempts >= ctx.conf.maxAttempts;
  if (final) stop_(row, "error", ctx.now);
  row._dirty = true;
  ctx.stats.failed++;
  log_(ctx, "error", row, {
    step: step, note: "第 " + row.attempts + " 次发送失败：" + text + (final ? "（已停止）" : "（下一轮重试）")
  });
  return false;
}

// The Message-ID of our previous email in this sequence. It is stored after each send; when that
// lookup failed, ask Gmail again by the message id kept in 记录.
function previousMessageId_(ctx, row) {
  if (row.messageId) return row.messageId;
  var sent = sentLogs_(ctx)[row.slug] || [];
  var id = sent.length ? messageIdOf_(sent[sent.length - 1].messageId) : "";
  if (id) {
    row.messageId = id;
    row._dirty = true;
  }
  return id;
}

function messageIdOf_(id) {
  try {
    var msg = Gmail.Users.Messages.get("me", id, { format: "metadata", metadataHeaders: ["Message-ID"] });
    return header_(msg, "Message-ID").trim();
  } catch (err) {
    console.warn("读不到刚发出邮件的 Message-ID：" + errText_(err));
    return "";
  }
}

function stop_(row, status, at) {
  row.status = status;
  if (OUTCOMES.indexOf(status) !== -1) {
    row.outcome = status;
    row.outcomeAt = at;
  }
  row.nextAt = null;
  row._dirty = true;
}

// ---- MIME ----

function raw_(m) {
  return Utilities.base64EncodeWebSafe(mime_(m), Utilities.Charset.UTF_8);
}

// ASCII-only MIME with CRLF line endings; the UTF-8 body travels as base64.
function mime_(m) {
  var from = m.fromName ? phrase_(m.fromName) : "";
  var fromLine = "From: " + (from ? from + " <" + m.from + ">" : m.from);
  if (fromLine.length > 76 && from) fromLine = "From: " + from + "\r\n <" + m.from + ">";
  var head = [
    fromLine,
    "To: " + m.to,
    "Subject: " + headerText_(m.subject),
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64"
  ];
  var ref = msgIdRef_(m.inReplyTo);
  if (ref) head.push("In-Reply-To: " + ref, "References: " + ref);
  var body = Utilities.base64Encode(crlf_(m.body), Utilities.Charset.UTF_8).replace(/.{76}(?=.)/g, "$&\r\n");
  return head.join("\r\n") + "\r\n\r\n" + body + "\r\n";
}

function crlf_(s) {
  return text_(s).replace(/\r\n|\r|\n/g, "\r\n");
}

function headerText_(text) {
  text = oneLine_(text).trim();
  if (/^[\x20-\x7e]*$/.test(text) && text.indexOf("=?") === -1 && text.length <= 900) return text;
  return encodedWords_(text);
}

// A display name: bare when it is plain ASCII words, quoted when it has specials, else RFC 2047.
function phrase_(name) {
  name = oneLine_(name).trim();
  if (!/^[\x20-\x7e]*$/.test(name) || name.indexOf("=?") !== -1) return encodedWords_(name);
  if (/^[A-Za-z0-9!#$%&'*+\/=?^_`{|}~ -]+$/.test(name)) return name;
  return '"' + name.replace(/(["\\])/g, "\\$1") + '"';
}

// RFC 2047 B-encoding in words of at most 39 UTF-8 bytes, so every header line stays within 76
// characters and no character is split between two words.
function encodedWords_(text) {
  var words = [], chunk = "", bytes = 0;
  Array.from(text).forEach(function (ch) {
    var n = utf8Length_(ch);
    if (bytes + n > 39 && chunk) {
      words.push(chunk);
      chunk = "";
      bytes = 0;
    }
    chunk += ch;
    bytes += n;
  });
  if (chunk) words.push(chunk);
  return words.map(function (w) {
    return "=?UTF-8?B?" + Utilities.base64Encode(w, Utilities.Charset.UTF_8) + "?=";
  }).join("\r\n ");
}

function utf8Length_(ch) {
  var c = ch.codePointAt(0);
  return c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
}

function msgIdRef_(id) {
  var s = oneLine_(id).trim();
  if (!s) return "";
  return s.charAt(0) === "<" ? s : "<" + s + ">";
}

// ---- Gmail helpers ----

function me_() {
  return Session.getEffectiveUser().getEmail();
}

function isOwn_(ctx, addr) {
  return Object.prototype.hasOwnProperty.call(own_(ctx), addr);
}

// Our own addresses: the effective user and its send-as aliases, read once per run.
function own_(ctx) {
  if (ctx.own) return ctx.own;
  var own = {};
  own[text_(me_()).toLowerCase()] = true;
  try {
    (Gmail.Users.Settings.SendAs.list("me").sendAs || []).forEach(function (s) {
      if (s.sendAsEmail) own[String(s.sendAsEmail).toLowerCase()] = true;
    });
  } catch (err) {
    console.warn("读不到发件别名：" + errText_(err));
  }
  ctx.own = own;
  return own;
}

function findHeader_(msg, name) {
  var list = (msg && msg.payload && msg.payload.headers) || [], want = name.toLowerCase();
  for (var i = 0; i < list.length; i++) {
    if (String(list[i].name).toLowerCase() === want) return list[i];
  }
  return null;
}

function header_(msg, name) {
  var h = findHeader_(msg, name);
  return h ? text_(h.value) : "";
}

function addressOf_(from) {
  var s = text_(from), angle = /<([^<>]*)>/.exec(s);
  if (angle) return angle[1].trim().toLowerCase();
  var bare = /[^\s<>"(),;:]+@[^\s<>"(),;:]+/.exec(s);
  return (bare ? bare[0] : s.trim()).toLowerCase();
}

function domainOf_(addr) {
  return text_(addr).split("@").pop().toLowerCase();
}

// ---- Storage: the sheet ----

function open_() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty("SHEET_ID");
  if (!id) throw problem_("not_set_up", MSG.not_set_up);
  var book;
  try {
    book = SpreadsheetApp.openById(id);
  } catch (err) {
    throw problem_("not_set_up", "打不开发信助手表格（" + errText_(err) + "）。请重新运行一次 setup()。");
  }
  var ctx = {
    props: props, conf: conf_(props), now: now_().getTime(), book: book,
    queue: tab_(book, TAB_QUEUE), logTab: tab_(book, TAB_LOG), blockTab: tab_(book, TAB_SUPPRESS),
    rows: [], added: [], logs: null, newLogs: [], newBlocks: [], suppressed: {}, own: null, windows: {}, inflight: [],
    stats: { checked: 0, sent: 0, replied: 0, bounced: 0, autoReplies: 0, failed: 0, held: "" }
  };
  ctx.rows = loadQueue_(ctx.queue);
  ctx.suppressed = loadSuppressed_(ctx.blockTab);
  replay_(ctx);
  return ctx;
}

function tab_(book, name) {
  var sheet = book.getSheetByName(name);
  if (!sheet) throw problem_("not_set_up", "表格里缺少「" + name + "」页。请重新运行一次 setup()。");
  return sheet;
}

function conf_(props) {
  var all = props.getProperties();
  function num(key) {
    var v = text_(all[key]).trim(), n = Number(v);
    return v !== "" && isFinite(n) ? n : Number(DEFAULTS[key]);
  }
  return {
    paused: text_(all.PAUSED).trim().toLowerCase() === "true",
    dailyCap: num("DAILY_CAP"), perTick: num("PER_TICK"), minGap: num("MIN_GAP_MINUTES"),
    windowStart: num("WINDOW_START"), windowEnd: num("WINDOW_END"), domainGap: num("DOMAIN_GAP_HOURS"),
    fromName: text_(all.FROM_NAME).trim(), maxAttempts: num("MAX_ATTEMPTS"), checksPerTick: num("CHECKS_PER_TICK")
  };
}

// The whole 队列 range, read once per run.
function loadQueue_(sheet) {
  var last = sheet.getLastRow();
  if (last < 2) return [];
  var rows = [];
  sheet.getRange(2, 1, last - 1, QUEUE_COLS.length).getValues().forEach(function (v, i) {
    if (text_(v[0]).trim()) rows.push(settle_({}, v, i + 2));
  });
  return rows;
}

// Makes the row match these sheet values and remembers them, to tell this run's changes from edits
// Charles makes in the sheet meanwhile (merge_).
function settle_(row, values, r) {
  Object.assign(row, rowOf_(values, r));
  row._orig = valuesOf_(row).map(cellKey_);
  return row;
}

// A cell value in comparable form: a date by its time.
function cellKey_(v) {
  return Object.prototype.toString.call(v) === "[object Date]" ? "@" + v.getTime() : String(v);
}

function rowOf_(values, r) {
  var row = { _r: r, _dirty: false };
  QUEUE_COLS.forEach(function (col, i) {
    var key = col[0], v = values[i];
    if (TIME_COLS[key]) row[key] = ms_(v);
    else if (NUMBER_COLS[key]) row[key] = Number(v) || 0;
    else row[key] = text_(v).trim();
  });
  row.status = row.status.toLowerCase();
  row.to = row.to.toLowerCase();
  return row;
}

function blankRow_(slug, now) {
  var row = { _r: 0, _dirty: true };
  QUEUE_COLS.forEach(function (col) {
    var key = col[0];
    row[key] = TIME_COLS[key] ? null : NUMBER_COLS[key] ? 0 : "";
  });
  row.slug = slug;
  row.status = "queued";
  row.queuedAt = now;
  return row;
}

function fill_(row, m) {
  row.to = m.to;
  row.company = m.company;
  row.contact = m.contact;
  row.wave = m.wave;
  row.lang = m.lang;
  row.tz = m.tz;
  row.subject = m.subject;
  row.total = 1 + m.followups.length;
  row.revision = m.revision;
  row.content = JSON.stringify(contentOf_(m));
  row.nextAt = null;
  row._dirty = true; // 错误 and 尝试次数 stay: a failed attempt may still have gone out (sentAlready_)
}

function valuesOf_(row) {
  return QUEUE_COLS.map(function (col) {
    var v = row[col[0]];
    if (TIME_COLS[col[0]]) return v == null ? "" : new Date(v);
    return v == null ? "" : v;
  });
}

function find_(ctx, slug) {
  for (var i = 0; i < ctx.rows.length; i++) if (ctx.rows[i].slug === slug) return ctx.rows[i];
  return null;
}

function counts_(ctx) {
  var counts = {};
  STATUSES.forEach(function (s) { counts[s] = 0; });
  ctx.rows.forEach(function (row) {
    if (Object.prototype.hasOwnProperty.call(counts, row.status)) counts[row.status]++;
  });
  return counts;
}

function loadSuppressed_(sheet) {
  var set = {}, last = sheet.getLastRow();
  if (last < 2) return set;
  sheet.getRange(2, 1, last - 1, 1).getValues().forEach(function (v) {
    var addr = text_(v[0]).trim().toLowerCase();
    if (addr) set[addr] = true;
  });
  return set;
}

function suppress_(ctx, addr, reason) {
  if (Object.prototype.hasOwnProperty.call(ctx.suppressed, addr)) return;
  ctx.suppressed[addr] = true;
  ctx.newBlocks.push([addr, reason, new Date(ctx.now)]);
}

function log_(ctx, event, row, more) {
  more = more || {};
  var e = {
    at: more.at == null ? ctx.now : more.at, slug: row ? row.slug : "", to: row ? row.to : text_(more.to),
    step: more.step == null ? "" : more.step,
    event: event, subject: text_(more.subject), messageId: text_(more.messageId),
    threadId: text_(more.threadId || (row && row.threadId)), note: text_(more.note)
  };
  ctx.newLogs.push(e);
  if (ctx.logs) ctx.logs.push(e);
}

// The whole 记录 tab plus what this run added, read at most once per run.
function logs_(ctx) {
  if (ctx.logs) return ctx.logs;
  var list = [], last = ctx.logTab.getLastRow();
  if (last >= 2) {
    ctx.logTab.getRange(2, 1, last - 1, LOG_HEADERS.length).getValues().forEach(function (v) {
      list.push({
        at: ms_(v[0]), slug: text_(v[1]), to: text_(v[2]), step: v[3], event: text_(v[4]), subject: text_(v[5]),
        messageId: text_(v[6]), threadId: text_(v[7]), note: text_(v[8])
      });
    });
  }
  ctx.logs = list.concat(ctx.newLogs);
  return ctx.logs;
}

function sentLogs_(ctx) {
  var by = {};
  logs_(ctx).forEach(function (e) {
    if (e.event !== "sent") return;
    (by[e.slug] = by[e.slug] || []).push(e);
  });
  return by;
}

// 记录 `sent` events dated today in the script timezone.
function sentToday_(ctx) {
  var today = day_(ctx.now);
  return logs_(ctx).filter(function (e) {
    return e.event === "sent" && e.at != null && Math.abs(ctx.now - e.at) < 2 * DAY && day_(e.at) === today;
  }).length;
}

function day_(ms) {
  return Utilities.formatDate(new Date(ms), Session.getScriptTimeZone(), "yyyy-MM-dd");
}

function logValues_(e) {
  return [new Date(e.at), e.slug, e.to, e.step, e.event, e.subject, e.messageId, e.threadId, e.note];
}

// Appends the new log events first (a `sent` event there is never sent again, see sentAlready_), then
// writes back the changed rows and appends new queue rows and suppressed addresses. Once all of it is
// in the sheet, the sends kept in Script Properties are no longer needed (remember_).
function save_(ctx) {
  if (ctx.newLogs.length) {
    append_(ctx.logTab, TAB_LOG, ctx.newLogs.map(logValues_));
    ctx.newLogs = [];
  }
  var dirty = ctx.rows.filter(function (row) { return row._dirty && row._r; });
  if (dirty.length) writeRows_(ctx, dirty);
  if (ctx.added.length) {
    var start = append_(ctx.queue, TAB_QUEUE, ctx.added.map(valuesOf_));
    ctx.added.forEach(function (row, i) {
      settle_(row, valuesOf_(row), start + i);
    });
    ctx.added = [];
  }
  if (ctx.newBlocks.length) {
    append_(ctx.blockTab, TAB_SUPPRESS, ctx.newBlocks);
    ctx.newBlocks = [];
  }
  if (ctx.inflight.length) {
    ctx.props.deleteProperty("INFLIGHT");
    ctx.inflight = [];
  }
}

// Each changed row goes to wherever its slug is now (Charles may have sorted the tab meanwhile), merged
// with what the sheet holds now (merge_); neighbouring rows go out in one call.
function writeRows_(ctx, rows) {
  var last = ctx.queue.getLastRow();
  var current = last < 2 ? [] : ctx.queue.getRange(2, 1, last - 1, QUEUE_COLS.length).getValues();
  var slugs = current.map(function (v) { return text_(v[0]).trim(); });
  var placed = [];
  rows.forEach(function (row) {
    var i = slugs[row._r - 2] === row.slug ? row._r - 2 : slugs.indexOf(row.slug);
    if (i === -1) console.warn("队列里找不到 " + row.slug + "（可能被手动删除了），这一行的改动没有写回。");
    else placed.push({ r: i + 2, row: row, values: merge_(row, current[i]) });
  });
  placed.sort(function (a, b) { return a.r - b.r; });
  for (var i = 0; i < placed.length;) {
    var j = i;
    while (j + 1 < placed.length && placed[j + 1].r === placed[j].r + 1) j++;
    var run = placed.slice(i, j + 1);
    ctx.queue.getRange(run[0].r, 1, run.length, QUEUE_COLS.length).setValues(run.map(function (p) { return p.values; }));
    run.forEach(function (p) {
      settle_(p.row, p.values, p.r);
    });
    i = j + 1;
  }
}

// Only the cells this run changed are written; an edit Charles made in the sheet meanwhile stays. His
// 状态 wins even over a change of ours, so a cancel typed while a tick runs holds.
function merge_(row, current) {
  var theirs = valuesOf_(rowOf_(current, 0)).map(cellKey_);
  return valuesOf_(row).map(function (v, c) {
    var ours = cellKey_(v) !== row._orig[c], hand = theirs[c] !== row._orig[c];
    return ours && !(hand && QUEUE_COLS[c][0] === "status") ? v : current[c];
  });
}

function append_(sheet, name, values) {
  var start = sheet.getLastRow() + 1, end = start + values.length - 1, max = sheet.getMaxRows();
  if (end > max) {
    sheet.insertRowsAfter(max, end - max);
    format_(sheet, name, max + 1, end - max);
  }
  sheet.getRange(start, 1, values.length, values[0].length).setValues(values);
  return start;
}

// Per column: "text", "time", or "" (numbers keep the default format).
function kinds_(name) {
  if (name === TAB_QUEUE) {
    return QUEUE_COLS.map(function (col) { return TIME_COLS[col[0]] ? "time" : NUMBER_COLS[col[0]] ? "" : "text"; });
  }
  if (name === TAB_LOG) return ["time", "text", "text", "", "text", "text", "text", "text", "text"];
  return ["text", "text", "time"];
}

function format_(sheet, name, fromRow, numRows) {
  var kinds = kinds_(name), i = 0;
  while (i < kinds.length) {
    var j = i;
    while (j + 1 < kinds.length && kinds[j + 1] === kinds[i]) j++;
    if (kinds[i]) sheet.getRange(fromRow, i + 1, numRows, j - i + 1).setNumberFormat(kinds[i] === "text" ? TEXT_FORMAT : TIME_FORMAT);
    i = j + 1;
  }
}

// ---- Dashboard and result pages ----

var PAGE_CSS = [
  ":root{color-scheme:light dark;--bg:#fff;--fg:#1d1d1f;--muted:#6e6e73;--line:#e5e5ea;--accent:#0a66c2}",
  "@media (prefers-color-scheme:dark){:root{--bg:#1c1c1e;--fg:#f2f2f7;--muted:#a1a1a6;--line:#3a3a3c;--accent:#4ea1ff}}",
  "body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,'PingFang SC','Microsoft YaHei',sans-serif}",
  "h1{font-size:20px;margin:0 0 8px}h2{font-size:16px;margin:24px 0 8px}p{margin:4px 0}.muted{color:var(--muted)}",
  ".actions{display:flex;gap:8px;margin:12px 0}.actions form{margin:0}",
  "button{font:inherit;padding:6px 14px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--accent);cursor:pointer}",
  ".scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}",
  "th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;white-space:nowrap}",
  "td.wrap{white-space:normal;min-width:160px}th{color:var(--muted);font-weight:500}a{color:var(--accent)}"
].join("\n");

function page_(body) {
  var html = '<!doctype html><html><head><meta charset="utf-8"><style>' + PAGE_CSS + "</style></head><body>" + body + "</body></html>";
  return HtmlService.createHtmlOutput(html).setTitle(BOOK_NAME).addMetaTag("viewport", "width=device-width, initial-scale=1");
}

function dashboard_(ctx, token) {
  var conf = ctx.conf, counts = counts_(ctx);
  var url = serviceUrl_();
  var h = ["<h1>" + esc_(BOOK_NAME) + "</h1>"];
  h.push("<p><b>" + (conf.paused ? "已暂停" : "运行中") + "</b> · 今天已发 " + sentToday_(ctx) + "/" + conf.dailyCap +
    " · 发件账号 " + esc_(me_()) + '</p><p class="muted">更新于 ' + esc_(time_(ctx.now)) + "（" +
    esc_(Session.getScriptTimeZone()) + "），只读页面，刷新可看最新状态。</p>");
  h.push('<div class="actions">' + formButton_(url, token, "pause", "暂停全部") + formButton_(url, token, "resume", "继续发送") + "</div>");
  h.push("<h2>各状态数量</h2><p>" + STATUSES.map(function (s) {
    return esc_(STATUS_LABEL[s]) + " " + counts[s];
  }).join(" · ") + "</p>");
  h.push("<h2>队列（" + ctx.rows.length + "）</h2>" + table_(
    ["公司", "收件人", "状态", "已发", "最近发送", "下次发送", "结果", "错误"],
    dashboardRows_(ctx).map(function (row) {
      var outcome = outcomeOf_(row);
      return [
        esc_(row.company || row.slug), esc_(row.to), esc_(STATUS_LABEL[row.status] || row.status),
        row.sent + "/" + row.total, esc_(time_(row.lastAt)), esc_(time_(row.nextAt)),
        outcome ? esc_(STATUS_LABEL[outcome] + " " + time_(row.outcomeAt)) : "", { wrap: esc_(row.error) }
      ];
    })));
  h.push("<h2>最近 50 条记录</h2>" + table_(
    ["时间", "事件", "slug", "收件人", "说明"],
    logs_(ctx).slice(-50).reverse().map(function (e) {
      return [esc_(time_(e.at)), esc_(EVENT_LABEL[e.event] || e.event), esc_(e.slug), esc_(e.to), { wrap: esc_(e.note) }];
    })));
  return page_(h.join(""));
}

function dashboardRows_(ctx) {
  var rank = { active: 0, queued: 1, error: 2, finished: 3, replied: 4, bounced: 5, cancelled: 6 };
  return ctx.rows.slice().sort(function (a, b) {
    var ra = rank[a.status] == null ? 7 : rank[a.status], rb = rank[b.status] == null ? 7 : rank[b.status];
    return (ra - rb) || ((b.lastAt || 0) - (a.lastAt || 0)) || (a.wave - b.wave);
  });
}

function serviceUrl_() {
  try {
    return ScriptApp.getService().getUrl() || "";
  } catch (err) {
    return "";
  }
}

// Cells are already-escaped HTML; {wrap: html} marks a cell that may wrap.
function table_(headers, rows) {
  if (!rows.length) return '<p class="muted">暂无。</p>';
  return '<div class="scroll"><table><tr>' + headers.map(function (t) { return "<th>" + esc_(t) + "</th>"; }).join("") + "</tr>" +
    rows.map(function (cells) {
      return "<tr>" + cells.map(function (c) {
        return c && typeof c === "object" ? '<td class="wrap">' + c.wrap + "</td>" : "<td>" + c + "</td>";
      }).join("") + "</tr>";
    }).join("") + "</table></div>";
}

// The dashboard's buttons use the form fallback: a POST in a new tab with the token in `payload`.
function formButton_(url, token, action, label) {
  return '<form method="post" action="' + esc_(url) + '" target="_blank">' +
    '<input type="hidden" name="payload" value="' + esc_(JSON.stringify({ token: token, action: action })) + '">' +
    "<button type=\"submit\">" + esc_(label) + "</button></form>";
}

// The small page a form post or a sender link answers with. `more` is HTML that follows the result.
function resultPage_(action, res, more) {
  return page_("<h1>" + esc_(BOOK_NAME) + "</h1><p>" + esc_(resultText_(action, res)) + "</p>" + (more || ""));
}

function resultText_(action, res) {
  var close = "可以关掉这个标签页。";
  if (!res.ok) return "没有完成：" + res.message;
  if (action === "enqueue") {
    var joined = 0, skipped = [];
    res.results.forEach(function (r) {
      if (r.result === "queued" || r.result === "updated") joined++;
      else skipped.push(r.slug + "：" + reasonText_(r.result === "duplicate" ? "duplicate" : r.reason));
    });
    var head = "已加入发送队列 " + joined + " 封" + (skipped.length ? "，跳过 " + skipped.length + " 封" : "");
    if (res.cards) return head + "。"; // a link's page lists every card below
    return head + (skipped.length ? "（" + skipped.join("；") + "）" : "") + "。" + close;
  }
  if (action === "cancel") {
    var who = res.company ? res.company + (res.contact ? "（" + res.contact + "）" : "") : res.slug;
    var gap = /）$/.test(who) ? "" : " ";
    return (res.status === "cancelled" ? "已停止 " + who + gap + "的自动发送。" :
      who + gap + "现在是「" + (STATUS_LABEL[res.status] || res.status) + "」，没有改动。") + close;
  }
  if (action === "pause") return "已暂停全部自动发送，回复检查照常进行。" + close;
  if (action === "resume") return "已继续自动发送。" + close;
  if (action === "test") return "测试邮件已发出，请到收件箱查看。" + close;
  if (action === "ping") {
    return "已连接 " + res.from + " · 今天已发 " + res.sentToday + "/" + res.dailyCap + " · 排队 " + res.counts.queued + " 封 · " +
      (res.paused ? "已暂停" : "运行中");
  }
  return "共 " + res.items.length + " 行。";
}

// Below a sender link's result: for enqueue one line per card and the sending rules, for ping the counts
// and the version.
function linkDetails_(action, res) {
  if (!res.ok) return "";
  if (action === "enqueue") {
    var h = [table_(["公司", "联系人", "结果"], res.cards.map(function (c) {
      return [esc_(c.company || c.slug), esc_(c.contact), { wrap: esc_(cardText_(c)) }];
    }))];
    h.push("<p>" + esc_(rulesText_(res.conf)) + "</p>");
    if (res.conf.paused) h.push("<p><b>" + esc_("发信助手现在是暂停状态，在发信助手页面点「继续发送」后才会发出。") + "</b></p>");
    return h.join("");
  }
  if (action === "ping") {
    return "<p>" + esc_(STATUSES.map(function (s) { return STATUS_LABEL[s] + " " + res.counts[s]; }).join(" · ")) +
      '</p><p class="muted">版本 ' + esc_(res.version) + "</p>";
  }
  return "";
}

function cardText_(c) {
  if (c.result === "queued") return "已加入发送队列";
  if (c.result === "updated") return "已更新（还没发出，内容换成了这一版）";
  if (c.result === "rejected") return "跳过：" + reasonText_(c.reason);
  var label = STATUS_LABEL[c.status] || c.status;
  if (c.sent > 0) return "跳过：已发出 " + c.sent + "/" + c.total + " 封（" + label + "），不会重复发";
  if (c.status === "queued" && c.revision < c.held) {
    return "跳过：发信助手里已是第 " + c.held + " 版，这个链接是旧的第 " + c.revision + " 版，没有改动";
  }
  return "跳过：这一封已是「" + label + "」，没有改动";
}

function rulesText_(conf) {
  return "会在对方当地工作日 " + conf.windowStart + "–" + conf.windowEnd + " 点按分组顺序发出，每封间隔至少 " + conf.minGap +
    " 分钟；对方回复后自动停止跟进。";
}

// HtmlService shows a page inside a frame, so the link opens the dashboard in the whole tab.
function dashboardLink_(token) {
  var url = serviceUrl_();
  if (!url) return "";
  return '<p><a href="' + esc_(url + "?action=dashboard&token=" + encodeURIComponent(text_(token))) + '" target="_top">打开发信助手</a></p>';
}

function reasonText_(reason) {
  var r = text_(reason);
  if (r.indexOf("placeholder:") === 0) return "还有占位符 " + r.slice(12);
  if (r.indexOf("address_in_use:") === 0) return "同一地址已在 " + r.slice(15) + " 的序列里";
  return {
    invalid_to: "收件人地址无效", empty: "主题、正文或跟进为空", wave_hold: "暂缓组，不发送", suppressed: "地址在屏蔽名单里",
    too_long: "内容超过 40,000 字", duplicate: "已经发出过，没有改动"
  }[r] || r;
}

function time_(ms) {
  return ms == null ? "" : Utilities.formatDate(new Date(ms), Session.getScriptTimeZone(), "MM-dd HH:mm");
}

// ---- setup(): run once from the editor; safe to run again ----

function setup() {
  // The consent screen lets Charles untick single permissions; this asks again until all are granted.
  ScriptApp.requireAllScopes(ScriptApp.AuthMode.FULL);
  var props = PropertiesService.getScriptProperties();
  var have = props.getProperties();
  var book = setupBook_(props, have.SHEET_ID);
  var missing = {};
  Object.keys(DEFAULTS).forEach(function (key) {
    if (have[key] == null) missing[key] = DEFAULTS[key];
  });
  if (!have.TOKEN) missing.TOKEN = Utilities.getUuid().replace(/-/g, "") + Utilities.getUuid().replace(/-/g, "");
  props.setProperties(missing);
  installTrigger_();
  var token = props.getProperty("TOKEN");
  console.log([
    "SimReal 发信助手已就绪。",
    "发件账号：" + me_(),
    "表格：" + book.getUrl(),
    "口令（TOKEN）：" + token,
    "定时任务：每 5 分钟运行一次 tick。",
    "下一步：",
    "1. 点右上角「部署 → 新建部署」，类型选「Web 应用」，执行身份选「我」，谁有权访问选「任何人」，部署后复制以 /exec 结尾的网址。",
    "2. 打开审批页「发件设置 → 自动发送（发信助手）」，粘贴网址和上面的口令，点「保存」，再点「测试连接」。",
    "3. 详细说明见 ops/sender-setup.md。网址和口令不要外传。"
  ].join("\n"));
  return { sheetUrl: book.getUrl(), token: token };
}

function setupBook_(props, id) {
  var book;
  if (id) {
    try {
      book = SpreadsheetApp.openById(id);
    } catch (err) {
      throw new Error("打不开 SHEET_ID 指向的表格（" + errText_(err) + "）。如果表格已删除，请在「项目设置 → 脚本属性」里删掉 SHEET_ID，再运行 setup()。");
    }
  } else {
    book = SpreadsheetApp.create(BOOK_NAME);
    book.getSheets()[0].setName(TAB_QUEUE);
    props.setProperty("SHEET_ID", book.getId());
  }
  book.setSpreadsheetTimeZone(Session.getScriptTimeZone());
  ensureTab_(book, TAB_QUEUE, QUEUE_COLS.map(function (col) { return col[1]; }));
  ensureTab_(book, TAB_LOG, LOG_HEADERS);
  ensureTab_(book, TAB_SUPPRESS, SUPPRESS_HEADERS);
  return book;
}

function ensureTab_(book, name, headers) {
  var sheet = book.getSheetByName(name) || book.insertSheet(name);
  if (sheet.getLastRow() === 0) {
    format_(sheet, name, 1, sheet.getMaxRows());
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight("bold");
    sheet.setFrozenRows(1);
    return;
  }
  var have = sheet.getRange(1, 1, 1, headers.length).getValues()[0].map(text_);
  if (have.join("|") !== headers.join("|")) console.warn("「" + name + "」页的表头和预期不一致，请检查：" + headers.join("，"));
}

function installTrigger_() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === "tick") ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger("tick").timeBased().everyMinutes(5).create();
}

// ---- Small helpers ----

function text_(v) {
  return v == null ? "" : String(v);
}

function oneLine_(v) {
  return text_(v).replace(/[\r\n]+/g, " ");
}

function esc_(s) {
  return text_(s).replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
  });
}

function errText_(err) {
  return text_(err && err.message ? err.message : err);
}

function ms_(v) {
  if (v === "" || v == null) return null;
  if (Object.prototype.toString.call(v) === "[object Date]") return isNaN(v.getTime()) ? null : v.getTime();
  var t = typeof v === "number" ? v : Date.parse(String(v));
  return isFinite(t) ? t : null;
}

function iso_(ms) {
  return ms == null ? null : new Date(ms).toISOString();
}
