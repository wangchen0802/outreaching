"use strict";
// Scenario tests for sender/Code.gs. Loads it into a vm context with the fakes from fakes.js and drives
// doPost / doGet / tick / setup on a test clock. No npm dependencies.
// Run: node sender/test/run.js   (VERBOSE=1 prints the script's console output; pass a name filter to run some)

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");
const { makeFakes, parseRaw, decodeWords, headerOf } = require("./fakes");

const CODE = fs.readFileSync(path.join(__dirname, "..", "Code.gs"), "utf8");
const ME = "business@simreal.co";
const MIN = 60000;
const HOUR = 60 * MIN;
const DAY = 24 * HOUR;
// Monday 2026-10-05 10:00 in Shanghai (the script timezone and most test recipients).
const MON10 = "2026-10-05T02:00:00Z";
const QUEUE_HEADERS = ["slug", "状态", "收件人", "公司", "联系人", "分组", "语言", "时区", "主题", "已发封数", "总封数", "下次发送", "首封时间",
  "最近发送", "threadId", "最近 Message-ID", "结果", "结果时间", "错误", "尝试次数", "入队时间", "修订", "内容JSON", "上次检查"];
const LOG_HEADERS = ["时间", "slug", "收件人", "步骤", "事件", "主题", "messageId", "threadId", "说明"];

// After loading Code.gs: route now_() through the test clock, and make any other time read throw.
const GUARD = `
now_ = function () { return new Date(__clockMs()); };
Date = (function (RealDate) {
  return new Proxy(RealDate, {
    construct: function (target, args, newTarget) {
      if (!args.length) throw new Error("Code.gs read the time outside now_()");
      return Reflect.construct(target, args, newTarget);
    },
    apply: function () { throw new Error("Code.gs called Date() as a function"); },
    get: function (target, key) {
      if (key === "now") return function () { throw new Error("Code.gs called Date.now() outside now_()"); };
      return target[key];
    }
  });
})(Date);
`;

function makeEnv(opts = {}) {
  const context = vm.createContext({});
  const CtxDate = vm.runInContext("Date", context);
  const clock = { ms: Date.parse(opts.at || MON10) };
  const fakes = makeFakes({ Date: CtxDate, clock, me: ME });
  Object.assign(context, fakes.globals);
  vm.runInContext(CODE, context, { filename: "Code.gs" });
  context.__clockMs = () => clock.ms;
  vm.runInContext(GUARD, context);
  const s = fakes.state;
  const env = Object.assign({ context, clock }, s);

  function lockFree() {
    assert.ok(s.lock.holder === null || s.lock.holder === s.lock.other, "the script lock was left held");
  }
  env.setup = () => context.setup();
  env.token = () => s.props.getProperty("TOKEN");
  env.prop = (key, value) => s.props.setProperty(key, String(value));
  env.at = (iso) => { clock.ms = typeof iso === "number" ? iso : Date.parse(iso); };
  env.advance = (minutes) => { clock.ms += minutes * MIN; };
  env.post = (body) => {
    const contents = typeof body === "string" ? body : JSON.stringify(body);
    const out = context.doPost({
      postData: { contents, type: "text/plain", length: contents.length, name: "postData" },
      parameter: {}, parameters: {}, queryString: "", contextPath: "", contentLength: contents.length
    });
    lockFree();
    assert.strictEqual(out.getMimeType(), "JSON", "fetch form answers with ContentService JSON");
    return JSON.parse(out.getContent());
  };
  env.call = (action, data) => env.post(Object.assign({ token: env.token(), action }, data || {}));
  env.enqueue = (messages) => env.call("enqueue", { messages });
  env.postForm = (body) => {
    const payload = typeof body === "string" ? body : JSON.stringify(body);
    const out = context.doPost({
      parameter: { payload }, parameters: { payload: [payload] }, queryString: "", contextPath: "",
      postData: { contents: "payload=" + encodeURIComponent(payload), type: "application/x-www-form-urlencoded", length: payload.length, name: "postData" },
      contentLength: payload.length
    });
    lockFree();
    assert.strictEqual(typeof out.getTitle, "function", "form fallback answers with an HtmlService page");
    return out.getContent();
  };
  env.get = (params) => {
    const parameters = {};
    Object.keys(params).forEach((k) => { parameters[k] = [params[k]]; });
    return context.doGet({ parameter: params, parameters, queryString: new URLSearchParams(params).toString(), contextPath: "", contentLength: -1 });
  };
  env.tick = () => {
    const before = s.mail.sent.length;
    context.tick();
    lockFree();
    return s.mail.sent.slice(before);
  };
  env.book = () => s.books.get(s.props.getProperty("SHEET_ID"));
  env.sheet = (name) => env.book().getSheetByName(name);
  env.table = (name) => {
    const sheet = env.sheet(name);
    const last = sheet.getLastRow();
    if (last < 1) return [];
    const values = sheet.getRange(1, 1, last, sheet.getLastColumn()).getValues();
    return values.slice(1).map((v) => {
      const o = {};
      values[0].forEach((h, i) => { o[h] = v[i]; });
      return o;
    });
  };
  env.rows = () => env.table("队列");
  env.row = (slug) => env.rows().find((r) => r.slug === slug);
  env.logs = (event) => env.table("记录").filter((e) => !event || e["事件"] === event);
  env.setCell = (slug, header, value) => {
    const sheet = env.sheet("队列");
    const r = env.rows().findIndex((x) => x.slug === slug) + 2;
    sheet.getRange(r, QUEUE_HEADERS.indexOf(header) + 1).setValues([[value]]);
  };
  env.content = (slug) => JSON.parse(env.row(slug)["内容JSON"]);
  env.editContent = (slug, fn) => {
    const c = env.content(slug);
    fn(c);
    env.setCell(slug, "内容JSON", JSON.stringify(c));
  };
  env.sentTo = (sent) => sent.map((m) => headerOf(m.parsed.headers, "To"));
  env.attemptsTo = (addr) => s.mail.sendAttempts.filter((x) => headerOf(parseRaw(x.resource.raw).headers, "To") === addr).length;
  env.threadOf = (slug) => env.row(slug).threadId;
  env.reply = (slug, over = {}) => s.mail.deliver(Object.assign({
    threadId: env.threadOf(slug), from: "Sam Lee <" + env.row(slug)["收件人"] + ">", subject: "Re: hello"
  }, over));
  if (opts.setup !== false) env.setup();
  envs.push(env);
  return env;
}

// Every environment a test made must end with clean MIME and no script errors.
let envs = [];
function checkEnvs() {
  envs.forEach((env) => {
    assert.deepStrictEqual(env.mail.problems, [], "MIME problems");
    assert.deepStrictEqual(env.output.error, [], "console.error from Code.gs");
  });
}

// A finalized Msg the way the approval page builds it.
function msg(slug, over = {}) {
  return Object.assign({
    slug, track: "investor", company: "Co " + slug, contact: "Sam Lee", to: slug + "@" + slug + "-co.com",
    subject: "SimReal x " + slug, body: "Hi Sam,\n\nA short note from SimReal.\n\nBest,\nCharles",
    followups: [{ day: 2, text: "Hi Sam, following up.\n\nCharles" }, { day: 3, text: "Last note.\n\nCharles" }],
    lang: "en", region: "国内", tz: "Asia/Shanghai", wave: 2, order: 1, revision: 1, fromName: "Charles"
  }, over);
}

function at(base, plusMs) {
  return new Date(Date.parse(base) + plusMs).toISOString();
}

function crlf(s) {
  return s.replace(/\r\n|\r|\n/g, "\r\n");
}

function results(r) {
  assert.strictEqual(r.ok, true, JSON.stringify(r));
  return r.results.map((x) => x.result === "rejected" ? "rejected:" + x.reason : x.result);
}

const tests = [];
function test(name, fn) {
  tests.push({ name, fn });
}

// ---------------------------------------------------------------------------------------------------

test("unauthorized token", () => {
  const env = makeEnv();
  [{ action: "ping" }, { token: "wrong", action: "ping" }, { token: env.token() + "x", action: "ping" }, { token: 123, action: "ping" }].forEach((body) => {
    const r = env.post(body);
    assert.deepStrictEqual([r.ok, r.error], [false, "unauthorized"]);
    assert.match(r.message, /口令/);
  });
  const r = env.post({ token: "wrong", action: "enqueue", messages: [msg("a")] });
  assert.strictEqual(r.error, "unauthorized");
  assert.strictEqual(env.rows().length, 0);
  assert.strictEqual(env.logs().length, 0);
  const status = env.get({ action: "status", token: "wrong" });
  assert.strictEqual(status.getMimeType(), "JSON");
  assert.strictEqual(JSON.parse(status.getContent()).error, "unauthorized");
  for (const params of [{ action: "dashboard", token: "wrong" }, {}]) {
    const page = env.get(params).getContent();
    assert.match(page, /口令/);
    assert.doesNotMatch(page, /<table/);
  }
  assert.strictEqual(JSON.parse(env.get({ action: "nope", token: env.token() }).getContent()).error, "bad_request");
  assert.strictEqual(env.post("{not json").error, "bad_request");
  assert.strictEqual(env.call("dance").error, "bad_request");

  const fresh = makeEnv({ setup: false });
  assert.strictEqual(fresh.post({ token: "x", action: "ping" }).error, "not_set_up");
  fresh.tick();
  assert.match(fresh.output.log.join("\n"), /setup/);
});

test("ping", () => {
  const env = makeEnv();
  const r = env.call("ping");
  assert.deepStrictEqual(Object.keys(r).sort(), ["counts", "dailyCap", "from", "ok", "paused", "sentToday", "version"]);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.from, ME);
  assert.strictEqual(r.paused, false);
  assert.strictEqual(r.dailyCap, 30);
  assert.strictEqual(r.sentToday, 0);
  assert.strictEqual(typeof r.version, "string");
  assert.deepStrictEqual(r.counts, { queued: 0, active: 0, finished: 0, replied: 0, bounced: 0, cancelled: 0, error: 0 });
  env.enqueue([msg("a"), msg("b")]);
  env.tick();
  const r2 = env.call("ping");
  assert.deepStrictEqual([r2.counts.queued, r2.counts.active, r2.sentToday], [1, 1, 1]);
});

test("enqueue validation: every reject reason", () => {
  const env = makeEnv();
  // The suppression list is read case-insensitively.
  env.sheet("屏蔽").getRange(2, 1, 1, 3).setValues([["Blocked@Block-co.com", "手动", ""]]);
  // Start from a sheet that is exactly full, so appending must grow it.
  const queue = env.sheet("队列");
  queue.maxRows = 1;
  const long = "x".repeat(40001);
  const r = env.enqueue([
    msg("ok1"),
    msg("bad-to", { to: "not-an-email" }),
    msg("two-to", { to: "a@x.com, b@y.com" }),
    msg("named-to", { to: "Sam <sam@x.com>" }),
    msg("no-subject", { subject: "   " }),
    msg("no-body", { body: " \n " }),
    msg("fu-empty", { followups: [{ day: 4, text: " " }] }),
    msg("fu-day", { followups: [{ day: 0, text: "hi" }] }),
    msg("deck", { body: "Deck: [Deck link]\nThanks" }),
    msg("bare", { body: "微信/电话：[ ]" }),
    msg("subj-ph", { subject: "[姓名] 你好" }),
    msg("fu-ph", { followups: [{ day: 4, text: "Thanks,\n[Your name]" }] }),
    msg("bp", { body: "BP：[BP 链接]" }),
    msg("long", { body: long }),
    msg("hold", { wave: 9 }),
    msg("supp", { to: "blocked@block-co.com" }),
    msg("dup-addr", { to: "OK1@ok1-co.com" }),
    msg("edge-81", { body: "see [" + "a".repeat(81) + "] ok" }),
    msg("multi-line", { body: "a [b\nc] d" }),
    msg("exact-40000", { subject: "S", body: "y".repeat(39999), followups: [] })
  ]);
  assert.deepStrictEqual(results(r), [
    "queued", "rejected:invalid_to", "rejected:invalid_to", "rejected:invalid_to", "rejected:empty", "rejected:empty",
    "rejected:empty", "rejected:empty", "rejected:placeholder:[Deck link]", "rejected:placeholder:[ ]",
    "rejected:placeholder:[姓名]", "rejected:placeholder:[Your name]", "rejected:placeholder:[BP 链接]", "rejected:too_long",
    "rejected:wave_hold", "rejected:suppressed", "rejected:address_in_use:ok1", "queued", "queued", "queued"
  ]);
  assert.strictEqual(r.results[0].slug, "ok1");
  assert.strictEqual(r.results[0].reason, null);
  assert.deepStrictEqual(results(env.enqueue([msg("ph80", { body: "[" + "a".repeat(80) + "]" })])), ["rejected:placeholder:[" + "a".repeat(80) + "]"]);

  const rows = env.rows();
  assert.deepStrictEqual(rows.map((x) => x.slug), ["ok1", "edge-81", "multi-line", "exact-40000"]);
  assert.deepStrictEqual(env.sheet("队列").getRange(1, 1, 1, 24).getValues()[0], QUEUE_HEADERS);
  const ok1 = env.row("ok1");
  assert.strictEqual(ok1["状态"], "queued");
  assert.strictEqual(ok1["收件人"], "ok1@ok1-co.com");
  assert.strictEqual(ok1["已发封数"], 0);
  assert.strictEqual(ok1["总封数"], 3);
  assert.strictEqual(ok1["分组"], 2);
  assert.strictEqual(ok1["时区"], "Asia/Shanghai");
  assert.strictEqual(ok1["修订"], 1);
  assert.strictEqual(ok1["入队时间"].getTime(), Date.parse(MON10), "times are stored as dates");
  const c = env.content("ok1");
  assert.deepStrictEqual(Object.keys(c).sort(), ["body", "followups", "fromName", "order", "region", "subject", "track"]);
  assert.strictEqual(c.body, msg("ok1").body);
  assert.deepStrictEqual(c.followups, msg("ok1").followups);
  // Rows added past the old end were given plain-text format, so ids stay text.
  assert.strictEqual(queue._format(2, QUEUE_HEADERS.indexOf("threadId") + 1), "@");
  assert.deepStrictEqual(env.logs("queued").map((e) => e.slug), ["ok1", "edge-81", "multi-line", "exact-40000"]);

  assert.strictEqual(env.enqueue(Array.from({ length: 61 }, (_, i) => msg("m" + i))).error, "bad_request");
  assert.strictEqual(env.enqueue([msg("")]).error, "bad_request");
  assert.strictEqual(env.call("enqueue", { messages: "nope" }).error, "bad_request");
  assert.strictEqual(env.rows().length, 4);
});

test("enqueue: updated while queued, duplicate once sent or cancelled", () => {
  const env = makeEnv();
  assert.deepStrictEqual(results(env.enqueue([msg("a"), msg("b", { order: 2 })])), ["queued", "queued"]);
  assert.deepStrictEqual(results(env.enqueue([msg("a", { subject: "New subject", revision: 2 })])), ["updated"]);
  assert.strictEqual(env.row("a")["主题"], "New subject");
  assert.strictEqual(env.row("a")["修订"], 2);
  assert.strictEqual(env.content("a").subject, "New subject");
  // An update that fails validation changes nothing.
  assert.deepStrictEqual(results(env.enqueue([msg("a", { subject: "[Deck link]", revision: 3 })])), ["rejected:placeholder:[Deck link]"]);
  assert.strictEqual(env.row("a")["修订"], 2);
  assert.deepStrictEqual(env.logs().map((e) => e["事件"]), ["queued", "queued", "updated"]);
  assert.strictEqual(env.rows().length, 2);

  const sent = env.tick();
  assert.strictEqual(decodeWords(headerOf(sent[0].parsed.headers, "Subject")), "New subject");
  assert.deepStrictEqual(results(env.enqueue([msg("a", { subject: "Third", revision: 4 })])), ["duplicate"]);
  assert.strictEqual(env.row("a")["主题"], "New subject");
  assert.strictEqual(env.row("a")["状态"], "active");

  env.call("cancel", { slug: "b" });
  assert.deepStrictEqual(results(env.enqueue([msg("b", { revision: 2 })])), ["duplicate"]);
  assert.strictEqual(env.row("b")["状态"], "cancelled");
  // Two messages for one slug in one call: the second replaces the first.
  assert.deepStrictEqual(results(env.enqueue([msg("c"), msg("c", { revision: 2 })])), ["queued", "updated"]);
  assert.strictEqual(env.rows().filter((x) => x.slug === "c").length, 1);
});

test("form fallback: payload field, HTML answers", () => {
  const env = makeEnv();
  const token = env.token();
  let html = env.postForm({ token, action: "enqueue", messages: [msg("a"), msg("b<x>", { to: "b@b-co.com", body: "[Deck link]" })] });
  assert.match(html, /已加入发送队列 1 封，跳过 1 封（b&lt;x&gt;：还有占位符 \[Deck link\]）。可以关掉这个标签页。/);
  assert.doesNotMatch(html, /b<x>/);
  assert.strictEqual(env.row("a")["状态"], "queued");

  html = env.postForm({ token: "bad", action: "pause" });
  assert.match(html, /没有完成/);
  assert.match(html, /口令/);
  assert.strictEqual(env.props.getProperty("PAUSED"), "false");

  assert.match(env.postForm({ token, action: "pause" }), /已暂停全部自动发送/);
  assert.strictEqual(env.props.getProperty("PAUSED"), "true");
  assert.match(env.postForm({ token, action: "resume" }), /已继续自动发送/);
  assert.strictEqual(env.props.getProperty("PAUSED"), "false");
  assert.match(env.postForm({ token, action: "cancel", slug: "a" }), /已停止 a 的自动发送/);
  assert.match(env.postForm({ token, action: "cancel", slug: "a" }), /已停止 a 的自动发送/, "cancelling twice is harmless");
  assert.match(env.postForm({ token, action: "cancel", slug: "zzz" }), /没有完成：队列里没有 zzz/);
  assert.match(env.postForm({ token, action: "test" }), /测试邮件已发出/);
  assert.match(env.postForm("not json"), /没有完成/);
});

test("status shape", () => {
  const env = makeEnv();
  env.enqueue([msg("a"), msg("b", { order: 2 })]);
  env.tick();
  const r = env.call("status");
  assert.deepStrictEqual(Object.keys(r).sort(), ["dailyCap", "items", "now", "ok", "paused", "sentToday"]);
  assert.deepStrictEqual([r.ok, r.paused, r.sentToday, r.dailyCap, r.now], [true, false, 1, 30, MON10.replace("Z", ".000Z")]);
  const a = r.items.find((x) => x.slug === "a");
  const b = r.items.find((x) => x.slug === "b");
  assert.deepStrictEqual(Object.keys(a).sort(), ["error", "log", "nextAt", "outcome", "outcomeAt", "revision", "slug", "status", "step", "to", "total"]);
  const first = env.mail.sent[0];
  assert.deepStrictEqual(a, {
    slug: "a", to: "a@a-co.com", status: "active", step: 1, total: 3,
    log: [{ step: 0, at: "2026-10-05T02:00:00.000Z", messageId: first.id, threadId: first.threadId }],
    nextAt: "2026-10-07T02:00:00.000Z", outcome: null, outcomeAt: null, error: null, revision: 1
  });
  assert.deepStrictEqual([b.status, b.step, b.total, b.log, b.nextAt, b.outcome], ["queued", 0, 3, [], null, null]);
  const only = env.call("status", { slugs: ["b"] });
  assert.deepStrictEqual(only.items.map((x) => x.slug), ["b"]);
  const viaGet = JSON.parse(env.get({ action: "status", token: env.token() }).getContent());
  assert.deepStrictEqual(viaGet.items, r.items);
  assert.deepStrictEqual(JSON.parse(env.get({ action: "status", token: env.token(), slugs: "a" }).getContent()).items, [a]);
});

test("tick sends first emails only inside the recipient's window", () => {
  const env = makeEnv({ at: "2026-10-10T17:00:00Z" }); // Sat 10:00 Los Angeles, Sun 01:00 Shanghai
  env.enqueue([msg("la", { tz: "America/Los_Angeles" }), msg("sh", { order: 2 })]);
  assert.strictEqual(env.tick().length, 0, "weekend");
  env.at("2026-10-12T02:00:00Z"); // Mon 10:00 Shanghai, Sun 19:00 Los Angeles
  assert.deepStrictEqual(env.sentTo(env.tick()), ["sh@sh-co.com"]);
  env.at("2026-10-12T14:30:00Z"); // Mon 07:30 Los Angeles
  assert.strictEqual(env.tick().length, 0, "before 08:00 local");
  env.at("2026-10-12T15:00:00Z"); // Mon 08:00 Los Angeles
  assert.deepStrictEqual(env.sentTo(env.tick()), ["la@la-co.com"]);

  const late = makeEnv({ at: "2026-10-13T00:59:00Z" }); // Mon 17:59 Los Angeles
  late.enqueue([msg("la", { tz: "America/Los_Angeles" })]);
  assert.strictEqual(late.tick().length, 1);
  const closed = makeEnv({ at: "2026-10-13T01:00:00Z" }); // Mon 18:00 Los Angeles
  closed.enqueue([msg("la", { tz: "America/Los_Angeles" })]);
  assert.strictEqual(closed.tick().length, 0, "18:00 is outside");
  closed.prop("WINDOW_END", 20);
  assert.strictEqual(closed.tick().length, 1, "WINDOW_END is read from Script Properties");
});

test("wave and order: C before B before A", () => {
  const env = makeEnv();
  env.enqueue([
    msg("a1", { wave: 3, order: 1 }), msg("b2", { wave: 2, order: 5 }), msg("c1", { wave: 1, order: 9 }),
    msg("b1", { wave: 2, order: 2 }), msg("c0", { wave: 1, order: 3 })
  ]);
  env.advance(1);
  env.enqueue([msg("x", { wave: 2, order: 2 })]); // ties with b1, queued later
  const order = [];
  for (let i = 0; i < 7; i++) {
    env.advance(5);
    env.tick().forEach((m) => order.push(headerOf(m.parsed.headers, "To").split("@")[0]));
  }
  assert.deepStrictEqual(order, ["c0", "c1", "b1", "x", "b2", "a1"]);
});

test("PER_TICK and MIN_GAP_MINUTES", () => {
  const env = makeEnv();
  env.enqueue(["a", "b", "c", "d", "e", "f"].map((s, i) => msg(s, { order: i })));
  assert.strictEqual(env.tick().length, 1);
  env.advance(2);
  assert.strictEqual(env.tick().length, 0, "2 minutes after the last send");
  env.advance(2);
  assert.strictEqual(env.tick().length, 1, "4 minutes after the last send");
  env.prop("PER_TICK", 3);
  env.advance(5);
  assert.strictEqual(env.tick().length, 1, "the gap also holds between sends of one tick");
  env.prop("MIN_GAP_MINUTES", 0);
  env.advance(5);
  assert.strictEqual(env.tick().length, 3);
  assert.strictEqual(env.rows().filter((x) => x["状态"] === "queued").length, 0);
});

test("DAILY_CAP counts first emails and follow-ups per script-timezone day", () => {
  const env = makeEnv();
  env.prop("DAILY_CAP", 2);
  env.prop("MIN_GAP_MINUTES", 0);
  env.prop("PER_TICK", 5);
  const fus = [{ day: 1, text: "Following up." }, { day: 5, text: "Last one." }];
  env.enqueue(["r1", "r2", "r3", "r4"].map((s, i) => msg(s, { order: i, followups: fus })));
  assert.deepStrictEqual(env.sentTo(env.tick()), ["r1@r1-co.com", "r2@r2-co.com"]);
  env.advance(60);
  assert.strictEqual(env.tick().length, 0);
  assert.match(env.output.log.slice(-1)[0], /每日上限/);
  assert.strictEqual(env.call("test").ok, true);
  assert.strictEqual(env.call("ping").sentToday, 2, "the test email does not count");
  env.at(at(MON10, DAY)); // Tuesday: the two follow-ups are due and go first
  const tue = env.tick();
  assert.deepStrictEqual(env.sentTo(tue), ["r1@r1-co.com", "r2@r2-co.com"]);
  assert.ok(tue.every((m) => /^Re: /.test(headerOf(m.parsed.headers, "Subject"))));
  env.at(at(MON10, 2 * DAY));
  assert.deepStrictEqual(env.sentTo(env.tick()), ["r3@r3-co.com", "r4@r4-co.com"]);
});

test("domain gap, with the free-mail exemption", () => {
  const env = makeEnv();
  env.enqueue([
    msg("a1", { to: "a1@acme.com", order: 1 }), msg("a2", { to: "a2@acme.com", order: 2 }), msg("b1", { to: "b1@beta.com", order: 3 }),
    msg("g1", { to: "g1@gmail.com", order: 4 }), msg("g2", { to: "g2@gmail.com", order: 5 })
  ]);
  const order = [];
  for (let i = 0; i < 5; i++) {
    env.tick().forEach((m) => order.push(headerOf(m.parsed.headers, "To")));
    env.advance(5);
  }
  assert.deepStrictEqual(order, ["a1@acme.com", "b1@beta.com", "g1@gmail.com", "g2@gmail.com"]);
  env.at(at(MON10, DAY - MIN));
  assert.strictEqual(env.tick().length, 0, "23h59m after the first acme email");
  env.at(at(MON10, DAY));
  assert.deepStrictEqual(env.sentTo(env.tick()), ["a2@acme.com"]);
});

test("follow-ups thread: Re: subject, In-Reply-To/References, threadId", () => {
  const env = makeEnv();
  env.mail.nextIds.push("9234567890123457"); // an all-digit id that a number cell would round
  env.enqueue([msg("a", { subject: "Intro: SimReal", followups: [{ day: 2, text: "FU one\nline 2" }, { day: 3, text: "FU two" }] })]);
  const [first] = env.tick();
  assert.strictEqual(first.threadId, "9234567890123457");
  assert.strictEqual(env.row("a").threadId, "9234567890123457");
  assert.strictEqual(first.resource.threadId, undefined);
  assert.strictEqual(headerOf(first.parsed.headers, "In-Reply-To"), "");
  const firstId = headerOf(first.headers, "Message-Id");
  assert.strictEqual(env.row("a")["最近 Message-ID"], firstId);

  env.at(at(MON10, DAY));
  assert.strictEqual(env.tick().length, 0);
  env.at(at(MON10, 2 * DAY - MIN));
  assert.strictEqual(env.tick().length, 0, "one minute before day 2");
  env.at(at(MON10, 2 * DAY));
  const [second] = env.tick();
  assert.ok(second, "follow-up 1 on day 2");
  assert.strictEqual(second.resource.threadId, "9234567890123457");
  assert.strictEqual(second.threadId, "9234567890123457", "Gmail filed it in the same thread");
  assert.strictEqual(headerOf(second.parsed.headers, "Subject"), "Re: Intro: SimReal");
  assert.strictEqual(headerOf(second.parsed.headers, "In-Reply-To"), firstId);
  assert.strictEqual(headerOf(second.parsed.headers, "References"), firstId);
  assert.strictEqual(second.parsed.body, "FU one\r\nline 2");
  assert.deepStrictEqual([env.row("a")["已发封数"], env.row("a")["状态"]], [2, "active"]);

  env.at(at(MON10, 3 * DAY));
  const [third] = env.tick();
  assert.strictEqual(headerOf(third.parsed.headers, "In-Reply-To"), headerOf(second.headers, "Message-Id"));
  assert.strictEqual(third.threadId, "9234567890123457");
  assert.strictEqual(env.mail.threads.get("9234567890123457").length, 3);
  assert.deepStrictEqual([env.row("a")["已发封数"], env.row("a")["状态"], env.row("a")["下次发送"]], [3, "finished", ""]);
  assert.deepStrictEqual(env.call("status").items[0].log.map((e) => e.step), [0, 1, 2]);
  env.at(at(MON10, 4 * DAY));
  assert.strictEqual(env.tick().length, 0);
});

test("a failed Message-ID lookup neither resends nor breaks threading", () => {
  const env = makeEnv();
  env.enqueue([msg("a")]);
  env.mail.failGetOnce = 1;
  assert.strictEqual(env.tick().length, 1);
  assert.deepStrictEqual([env.row("a")["状态"], env.row("a")["最近 Message-ID"]], ["active", ""]);
  env.advance(5);
  assert.strictEqual(env.tick().length, 0, "no second first email");
  env.at(at(MON10, 2 * DAY));
  const [fu] = env.tick();
  assert.strictEqual(headerOf(fu.parsed.headers, "In-Reply-To"), headerOf(env.mail.sent[0].headers, "Message-Id"));
  assert.strictEqual(fu.threadId, env.mail.sent[0].threadId);
});

test("no follow-up after a reply (round-robin check)", () => {
  const env = makeEnv();
  env.enqueue([msg("a")]);
  env.tick();
  env.at(at(MON10, DAY + 2 * HOUR));
  const replyAt = env.clock.ms - 30 * MIN;
  env.reply("a", { at: replyAt });
  env.tick();
  const row = env.row("a");
  assert.deepStrictEqual([row["状态"], row["结果"], row["结果时间"].getTime()], ["replied", "replied", replyAt]);
  assert.strictEqual(env.logs("replied").length, 1);
  env.at(at(MON10, 2 * DAY));
  assert.strictEqual(env.tick().length, 0);
  env.at(at(MON10, 3 * DAY));
  assert.strictEqual(env.tick().length, 0);
  const item = env.call("status").items[0];
  assert.deepStrictEqual([item.outcome, item.outcomeAt], ["replied", new Date(replyAt).toISOString()]);
});

test("4b: a reply just before the follow-up is due stops it", () => {
  const env = makeEnv();
  env.prop("CHECKS_PER_TICK", 0); // no round-robin: only the pre-follow-up check can see the reply
  env.enqueue([msg("a"), msg("b", { order: 2 })]);
  env.tick();
  env.advance(5);
  env.tick();
  env.at(at(MON10, DAY));
  env.tick();
  assert.strictEqual(env.mail.calls.threadsGet, 0);
  env.at(at(MON10, 2 * DAY - 2 * MIN));
  env.reply("a");
  env.at(at(MON10, 2 * DAY));
  assert.strictEqual(env.tick().length, 0, "a's follow-up is held back");
  assert.strictEqual(env.row("a")["状态"], "replied");
  env.advance(5);
  assert.deepStrictEqual(env.sentTo(env.tick()), ["b@b-co.com"], "b had no reply and gets its follow-up");
});

test("auto-replies and our own messages do not stop the sequence", () => {
  const env = makeEnv();
  env.prop("PER_TICK", 10);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue(["a", "b", "c", "d", "e", "f"].map((s, i) => msg(s, { order: i })));
  assert.strictEqual(env.tick().length, 6);
  env.at(at(MON10, DAY + HOUR));
  env.reply("a", { subject: "Out of Office: Sam", headers: { "Auto-Submitted": "auto-replied" } });
  env.reply("b", { subject: "自动回复：休假中" });
  env.reply("c", { subject: "Re: hi", headers: { "x-autoreply": "yes" } });
  env.reply("d", { subject: "Re: hi", headers: { Precedence: "auto_reply" } });
  env.reply("e", { subject: "Re: SimReal", headers: { "Auto-Submitted": "no" } }); // a person
  env.reply("f", { from: "Charles <charles@simreal.co>", subject: "Re: SimReal" }); // our alias
  env.reply("f", { from: ME, subject: "Re: SimReal" });
  env.tick();
  assert.deepStrictEqual(["a", "b", "c", "d", "e", "f"].map((s) => env.row(s)["状态"]), ["active", "active", "active", "active", "replied", "active"]);
  assert.deepStrictEqual(env.logs("auto_reply").map((e) => e.slug), ["a", "b", "c", "d"]);
  env.advance(5);
  env.tick();
  assert.strictEqual(env.logs("auto_reply").length, 4, "each auto-reply is logged once");
  env.at(at(MON10, 2 * DAY));
  assert.deepStrictEqual(env.sentTo(env.tick()).sort(), ["a@a-co.com", "b@b-co.com", "c@c-co.com", "d@d-co.com", "f@f-co.com"]);
});

test("a bounce stops the sequence and suppresses the address", () => {
  const env = makeEnv();
  env.prop("PER_TICK", 10);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue(["a", "b", "c", "d"].map((s, i) => msg(s, { order: i })));
  assert.strictEqual(env.tick().length, 4);
  env.advance(20);
  // a: Gmail files the bounce in our thread.
  env.reply("a", { from: "Mail Delivery Subsystem <mailer-daemon@googlemail.com>", subject: "Delivery Status Notification (Failure)", headers: { "X-Failed-Recipients": "a@a-co.com" } });
  // b, c: bounces in threads of their own, found by the search.
  env.mail.deliver({ from: "postmaster@b-co.com", subject: "Undeliverable: SimReal x b", headers: { "X-Failed-Recipients": "B@b-co.com" } });
  env.mail.deliver({ from: "MAILER-DAEMON@relay.example.net", subject: "Returned mail", snippet: "Your message to c@c-co.com couldn't be delivered." });
  // Not d: another address that contains d's, and an old bounce from before the first send.
  env.mail.deliver({ from: "mailer-daemon@googlemail.com", subject: "Failure", snippet: "wasn't delivered to xd@d-co.com" });
  env.mail.deliver({ from: "mailer-daemon@googlemail.com", subject: "Failure", snippet: "wasn't delivered to d@d-co.com", at: Date.parse(MON10) - HOUR });
  env.tick();
  assert.deepStrictEqual(["a", "b", "c", "d"].map((s) => env.row(s)["状态"]), ["bounced", "bounced", "bounced", "active"]);
  assert.deepStrictEqual(env.table("屏蔽").map((x) => x["邮箱"]), ["a@a-co.com", "b@b-co.com", "c@c-co.com"]);
  assert.strictEqual(env.logs("bounced").length, 3);
  assert.strictEqual(env.row("a")["结果"], "bounced");
  env.advance(5);
  env.tick();
  assert.strictEqual(env.table("屏蔽").length, 3, "no duplicate suppression rows");
  env.at(at(MON10, 2 * DAY));
  assert.deepStrictEqual(env.sentTo(env.tick()), ["d@d-co.com"]);
  assert.deepStrictEqual(results(env.enqueue([msg("a2", { to: "a@a-co.com" })])), ["rejected:suppressed"]);
});

test("cancel stops a queued or active row; other statuses are returned unchanged", () => {
  const env = makeEnv();
  env.enqueue([msg("a"), msg("b", { order: 2 }), msg("c", { order: 3, followups: [] })]);
  assert.deepStrictEqual(env.call("cancel", { slug: "a" }), { ok: true, slug: "a", status: "cancelled" });
  assert.deepStrictEqual(env.sentTo(env.tick()), ["b@b-co.com"]);
  assert.deepStrictEqual(env.call("cancel", { slug: "b" }), { ok: true, slug: "b", status: "cancelled" });
  env.advance(5);
  assert.deepStrictEqual(env.sentTo(env.tick()), ["c@c-co.com"]);
  assert.strictEqual(env.call("cancel", { slug: "c" }).status, "finished");
  assert.strictEqual(env.call("cancel", { slug: "a" }).status, "cancelled");
  assert.strictEqual(env.call("cancel", { slug: "nope" }).error, "bad_request");
  env.at(at(MON10, 2 * DAY));
  assert.strictEqual(env.tick().length, 0);
  env.at(at(MON10, 3 * DAY));
  assert.strictEqual(env.tick().length, 0);
  assert.strictEqual(env.logs("cancelled").length, 2);
  const b = env.call("status", { slugs: ["b"] }).items[0];
  assert.deepStrictEqual([b.status, b.outcome, b.step], ["cancelled", "cancelled", 1]);
});

test("pause stops sends but still detects replies", () => {
  const env = makeEnv();
  env.enqueue([msg("a"), msg("b", { order: 2 })]);
  env.tick();
  assert.deepStrictEqual(env.call("pause"), { ok: true, paused: true });
  assert.strictEqual(env.call("ping").paused, true);
  env.at(at(MON10, DAY));
  env.reply("a");
  assert.strictEqual(env.tick().length, 0);
  assert.strictEqual(env.row("a")["状态"], "replied");
  assert.strictEqual(env.row("b")["状态"], "queued");
  assert.deepStrictEqual(env.call("resume"), { ok: true, paused: false });
  assert.deepStrictEqual(env.sentTo(env.tick()), ["b@b-co.com"]);
});

test("overdue follow-ups after a pause go out at least 20 hours apart", () => {
  const env = makeEnv();
  env.prop("WINDOW_START", 0);
  env.prop("WINDOW_END", 24);
  env.enqueue([msg("a", { followups: [{ day: 1, text: "one" }, { day: 2, text: "two" }] })]);
  env.tick();
  env.call("pause");
  env.at(at(MON10, 3 * DAY)); // Thursday: both follow-ups are overdue
  env.call("resume");
  assert.strictEqual(env.tick()[0].parsed.body, "one");
  assert.strictEqual(env.call("status").items[0].nextAt, at(MON10, 3 * DAY + 20 * HOUR));
  env.at(at(MON10, 3 * DAY + 20 * HOUR - MIN));
  assert.strictEqual(env.tick().length, 0);
  env.at(at(MON10, 3 * DAY + 20 * HOUR));
  assert.strictEqual(env.tick()[0].parsed.body, "two");
});

test("a 状态 set to cancelled by hand is respected", () => {
  const env = makeEnv();
  env.prop("PER_TICK", 5);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue([msg("a"), msg("b", { order: 2 })]);
  env.setCell("a", "状态", "cancelled");
  assert.deepStrictEqual(env.sentTo(env.tick()), ["b@b-co.com"]);
  env.setCell("b", "状态", "Cancelled");
  env.at(at(MON10, 2 * DAY));
  assert.strictEqual(env.tick().length, 0);
  assert.strictEqual(env.row("a")["状态"], "cancelled");
  assert.strictEqual(env.call("ping").counts.cancelled, 2);
});

test("send failures: retried on later ticks, error after MAX_ATTEMPTS; invalid address stops at once", () => {
  const env = makeEnv();
  env.enqueue([msg("a")]);
  env.mail.failNext.push("Backend Error", "Backend Error", "Backend Error");
  for (let i = 1; i <= 3; i++) {
    assert.strictEqual(env.tick().length, 0);
    assert.strictEqual(env.mail.sendAttempts.length, i, "one attempt per tick");
    assert.strictEqual(env.row("a")["尝试次数"], i);
    assert.match(env.row("a")["错误"], /Backend Error/);
    assert.strictEqual(env.row("a")["状态"], i < 3 ? "queued" : "error");
    env.advance(5);
  }
  env.tick();
  assert.strictEqual(env.mail.sendAttempts.length, 3, "no attempt after error");
  assert.strictEqual(env.logs("error").length, 3);

  // A failed attempt uses one of the tick's PER_TICK slots; the next row still goes, and the failed row waits a tick.
  env.prop("PER_TICK", 3);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue([msg("b"), msg("c", { order: 2 })]);
  env.mail.failNext.push("Backend Error");
  assert.deepStrictEqual(env.sentTo(env.tick()), ["c@c-co.com"]);
  assert.strictEqual(env.attemptsTo("b@b-co.com"), 1);
  assert.strictEqual(env.row("b")["尝试次数"], 1);
  env.advance(5);
  assert.deepStrictEqual(env.sentTo(env.tick()), ["b@b-co.com"]);
  assert.deepStrictEqual([env.row("b")["状态"], env.row("b")["尝试次数"], env.row("b")["错误"]], ["active", 0, ""]);

  env.enqueue([msg("d")]);
  env.mail.failNext.push("Invalid To header");
  env.advance(5);
  env.tick();
  assert.deepStrictEqual([env.row("d")["状态"], env.row("d")["尝试次数"]], ["error", 1]);
  // Gmail's own rejection of an address that passed our pattern.
  env.enqueue([msg("e", { to: "e..x@e-co.com" })]);
  env.advance(5);
  env.tick();
  assert.deepStrictEqual([env.row("e")["状态"], env.row("e")["尝试次数"]], ["error", 1]);
  assert.match(env.row("e")["错误"], /Invalid To header/);
});

test("re-validation at send time catches edits made in the sheet", () => {
  const env = makeEnv();
  env.prop("PER_TICK", 10);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue(["a", "b", "c", "d", "e"].map((s, i) => msg(s, { order: i })));
  env.editContent("a", (c) => { c.body += "\nDeck: [Deck link]"; });
  env.setCell("b", "收件人", "not-an-address");
  env.setCell("d", "内容JSON", "{broken");
  env.sheet("屏蔽").getRange(2, 1, 1, 3).setValues([["e@e-co.com", "手动", ""]]);
  assert.deepStrictEqual(env.sentTo(env.tick()), ["c@c-co.com"]);
  assert.deepStrictEqual(["a", "b", "d", "e"].map((s) => env.row(s)["状态"]), ["error", "error", "error", "error"]);
  assert.strictEqual(env.row("a")["错误"], "发送前检查不通过：placeholder:[Deck link]");
  assert.strictEqual(env.row("b")["错误"], "发送前检查不通过：invalid_to");
  assert.match(env.row("d")["错误"], /内容JSON 无法解析/);
  assert.strictEqual(env.row("e")["错误"], "发送前检查不通过：suppressed");
  env.editContent("c", (c) => { c.followups[0].text = "微信/电话：[ ]"; });
  env.at(at(MON10, 2 * DAY));
  assert.strictEqual(env.tick().length, 0);
  assert.deepStrictEqual([env.row("c")["状态"], env.row("c")["错误"]], ["error", "发送前检查不通过：placeholder:[ ]"]);
});

test("changed rows are written back by slug, even if the tab was sorted during the run", () => {
  const env = makeEnv();
  env.prop("PER_TICK", 5);
  env.prop("MIN_GAP_MINUTES", 0);
  env.enqueue([msg("a"), msg("b", { order: 2 }), msg("c", { order: 3 })]);
  const queue = env.sheet("队列");
  let calls = 0;
  const setValues = Object.getPrototypeOf(queue.getRange(1, 1)).setValues;
  // Charles sorts the tab (c, b, a) while the tick is sending.
  env.mail.onSend = () => {
    env.mail.onSend = null;
    const body = queue.cells.slice(1).reverse();
    queue.cells.splice(1, body.length, ...body);
  };
  queue.getRange = function (row, col, numRows, numCols) {
    const range = Object.getPrototypeOf(this).getRange.apply(this, arguments);
    range.setValues = function (values) { calls++; return setValues.call(this, values); };
    return range;
  };
  assert.strictEqual(env.tick().length, 3);
  assert.deepStrictEqual(env.rows().map((r) => r.slug), ["c", "b", "a"]);
  assert.deepStrictEqual(env.rows().map((r) => [r["收件人"], r["状态"], r["已发封数"]]), [
    ["c@c-co.com", "active", 1], ["b@b-co.com", "active", 1], ["a@a-co.com", "active", 1]
  ]);
  assert.strictEqual(calls, 1, "three neighbouring rows in one setValues");
});

test("finished after the last step; replies are watched for 14 days", () => {
  const env = makeEnv();
  env.enqueue([msg("a", { followups: [] }), msg("b", { followups: [], order: 2 })]);
  env.tick();
  assert.deepStrictEqual([env.row("a")["状态"], env.row("a")["总封数"], env.row("a")["下次发送"]], ["finished", 1, ""]);
  env.advance(5);
  env.tick();
  env.at(at(MON10, DAY));
  env.reply("a");
  assert.strictEqual(env.tick().length, 0);
  assert.strictEqual(env.row("a")["状态"], "replied");
  env.at(at(MON10, 15 * DAY));
  env.reply("b");
  env.tick();
  assert.strictEqual(env.row("b")["状态"], "finished", "not checked after 14 days");
});

test("Chinese subject and body: RFC 2047 subject and base64 body round-trip exactly", () => {
  const env = makeEnv();
  const subject = "关于 SimReal 的合作：专家数据与 RL 环境——想和您约 20 分钟聊聊 🚀 这个主题故意写得很长，用来测试编码词拆分";
  const body = "张总您好：\n\n我是 SimReal 的 Charles。😀 emoji 和中文混排……\n第二段 with English，以及“引号”和——破折号。\n" + "长".repeat(300) + "\n";
  env.enqueue([msg("zh", { subject, body, fromName: "张三（SimReal）", lang: "zh" }), msg("en", { order: 2, fromName: "Zhang, Charles" })]);
  const [m] = env.tick();
  const h = m.parsed.headers;
  assert.match(headerOf(h, "Subject"), /^=\?UTF-8\?B\?/);
  assert.ok(m.parsed.mime.split("\r\n").filter((l) => /^ =\?UTF-8/.test(l)).length >= 2, "long subject is folded into several words");
  assert.strictEqual(decodeWords(headerOf(h, "Subject")), subject);
  assert.strictEqual(decodeWords(headerOf(h, "From")), "张三（SimReal） <business@simreal.co>");
  assert.strictEqual(headerOf(h, "To"), "zh@zh-co.com");
  assert.strictEqual(headerOf(h, "MIME-Version"), "1.0");
  assert.strictEqual(headerOf(h, "Content-Type"), "text/plain; charset=UTF-8");
  assert.strictEqual(headerOf(h, "Content-Transfer-Encoding"), "base64");
  assert.strictEqual(m.parsed.body, crlf(body));
  assert.ok(m.parsed.bodyRaw.split("\r\n").filter(Boolean).every((l) => l.length <= 76));
  assert.strictEqual(m.parsed.bodyRaw.split("\r\n")[0].length, 76);
  env.advance(5);
  const [en] = env.tick();
  assert.strictEqual(headerOf(en.parsed.headers, "Subject"), "SimReal x en", "ASCII subjects stay as they are");
  assert.strictEqual(headerOf(en.parsed.headers, "From"), '"Zhang, Charles" <business@simreal.co>');
  env.prop("FROM_NAME", "Charles");
  env.enqueue([msg("nn", { fromName: "" })]);
  env.advance(5);
  assert.strictEqual(headerOf(env.tick()[0].parsed.headers, "From"), "Charles <business@simreal.co>", "falls back to FROM_NAME");
});

test("CRLF normalization", () => {
  const env = makeEnv();
  env.enqueue([msg("a", { body: "line1\r\nline2\nline3\rline4\n\nend", followups: [{ day: 1, text: "x\ny\r\n" }] })]);
  const [m] = env.tick();
  assert.strictEqual(m.parsed.body, "line1\r\nline2\r\nline3\r\nline4\r\n\r\nend");
  assert.ok(!/(^|[^\r])\n/.test(m.parsed.mime) && !/\r(?!\n)/.test(m.parsed.mime));
  env.at(at(MON10, DAY));
  assert.strictEqual(env.tick()[0].parsed.body, "x\r\ny\r\n");
});

test("setup() is idempotent: one trigger, same TOKEN and sheet", () => {
  const env = makeEnv();
  const token = env.token();
  const sheetId = env.props.getProperty("SHEET_ID");
  assert.match(token, /^[0-9a-f]{64}$/);
  assert.deepStrictEqual(env.triggers.map((t) => [t.getHandlerFunction(), t.spec.everyMinutes]), [["tick", 5]]);
  assert.deepStrictEqual(env.props.getProperties(), {
    SHEET_ID: sheetId, TOKEN: token, PAUSED: "false", DAILY_CAP: "30", PER_TICK: "1", MIN_GAP_MINUTES: "4", WINDOW_START: "8",
    WINDOW_END: "18", DOMAIN_GAP_HOURS: "24", FROM_NAME: "", MAX_ATTEMPTS: "3", CHECKS_PER_TICK: "40"
  });
  const book = env.book();
  assert.strictEqual(book.getName(), "SimReal 发信助手");
  assert.strictEqual(book.getSpreadsheetTimeZone(), "Asia/Shanghai");
  assert.deepStrictEqual(book.getSheets().map((s) => s.getName()), ["队列", "记录", "屏蔽"]);
  assert.deepStrictEqual(env.sheet("记录").getRange(1, 1, 1, 9).getValues()[0], LOG_HEADERS);
  assert.deepStrictEqual(env.sheet("屏蔽").getRange(1, 1, 1, 3).getValues()[0], ["邮箱", "原因", "时间"]);
  assert.strictEqual(env.sheet("队列").getFrozenRows(), 1);
  const log = env.output.log.join("\n");
  assert.ok(log.includes(book.getUrl()) && log.includes(token));
  assert.match(log, /部署/);
  assert.match(log, /ops\/sender-setup\.md/);

  env.context.ScriptApp.newTrigger("other").timeBased().everyMinutes(10).create();
  env.prop("DAILY_CAP", 50);
  env.enqueue([msg("a")]);
  env.setup();
  env.setup();
  assert.deepStrictEqual(env.triggers.map((t) => t.getHandlerFunction()).sort(), ["other", "tick"]);
  assert.strictEqual(env.token(), token);
  assert.strictEqual(env.props.getProperty("SHEET_ID"), sheetId);
  assert.strictEqual(env.props.getProperty("DAILY_CAP"), "50");
  assert.strictEqual(env.books.size, 1);
  assert.deepStrictEqual(env.rows().map((r) => r.slug), ["a"]);

  env.props.deleteProperty("TOKEN");
  env.props.deleteProperty("PER_TICK");
  env.setup();
  assert.match(env.token(), /^[0-9a-f]{64}$/);
  assert.notStrictEqual(env.token(), token);
  assert.strictEqual(env.props.getProperty("PER_TICK"), "1");
  assert.strictEqual(env.props.getProperty("DAILY_CAP"), "50");
});

test("lock busy: doPost answers busy, tick skips", () => {
  const env = makeEnv();
  env.enqueue([msg("a")]);
  env.lock.holder = env.lock.other;
  const r = env.call("ping");
  assert.deepStrictEqual([r.ok, r.error], [false, "busy"]);
  assert.match(r.message, /稍后|过一会儿/);
  assert.strictEqual(env.call("enqueue", { messages: [msg("b")] }).error, "busy");
  assert.strictEqual(env.post({ token: "wrong", action: "ping" }).error, "unauthorized", "the token is checked before the lock");
  assert.match(env.postForm({ token: env.token(), action: "pause" }), /没有完成/);
  assert.strictEqual(env.tick().length, 0);
  assert.match(env.output.log.slice(-1)[0], /跳过/);
  env.lock.holder = null;
  assert.strictEqual(env.tick().length, 1);
  assert.strictEqual(env.rows().length, 1);
});

test("test action: one plain email to ourselves", () => {
  const env = makeEnv();
  const r = env.call("test");
  assert.deepStrictEqual(Object.keys(r).sort(), ["messageId", "ok", "threadId"]);
  const m = env.mail.sent[0];
  assert.deepStrictEqual([r.messageId, r.threadId], [m.id, m.threadId]);
  assert.strictEqual(headerOf(m.parsed.headers, "To"), ME);
  assert.strictEqual(decodeWords(headerOf(m.parsed.headers, "Subject")), "SimReal 发信助手测试");
  assert.match(m.parsed.body, /设置好/);
  assert.match(m.parsed.body, /2026-10-05 10:00:00/);
  assert.strictEqual(env.logs("test").length, 1);
  assert.strictEqual(env.rows().length, 0);
  assert.strictEqual(env.call("ping").sentToday, 0);
});

test("dashboard: read-only, escaped, with pause and resume forms", () => {
  const env = makeEnv();
  env.enqueue([msg("x", { company: "<img src=x onerror=alert(1)>" }), msg("y", { order: 2 })]);
  env.tick();
  env.mail.failNext.push("<script>alert(1)</script>");
  env.advance(5);
  env.tick();
  const out = env.get({ action: "dashboard", token: env.token() });
  assert.strictEqual(out.getTitle(), "SimReal 发信助手");
  const html = out.getContent();
  assert.ok(html.includes("&lt;img src=x onerror=alert(1)&gt;"));
  assert.ok(!html.includes("<img") && !html.includes("<script>"));
  assert.match(html, /运行中/);
  assert.match(html, /今天已发 1\/30/);
  assert.match(html, /发送中 1 · 序列结束 0/);
  ["公司", "收件人", "状态", "最近发送", "下次发送", "结果", "错误", "暂停全部", "继续发送", "最近 50 条记录"].forEach((t) => assert.ok(html.includes(t), t));
  const forms = html.match(/<form method="post" action="([^"]*)" target="_blank"><input type="hidden" name="payload" value="([^"]*)">/g);
  assert.strictEqual(forms.length, 2);
  assert.ok(html.includes('action="' + env.serviceUrl + '"'));
  assert.ok(html.includes("&quot;token&quot;:&quot;" + env.token() + "&quot;,&quot;action&quot;:&quot;pause&quot;"));
  assert.strictEqual(env.get({ token: env.token() }).getContent().replace(/更新于 [^（]+/, ""), html.replace(/更新于 [^（]+/, ""));
});

// ---------------------------------------------------------------------------------------------------

const filter = process.argv[2];
let failed = 0;
let ran = 0;
for (const t of tests) {
  if (filter && !t.name.includes(filter)) continue;
  ran++;
  envs = [];
  try {
    t.fn();
    checkEnvs();
    console.log("PASS  " + t.name);
  } catch (err) {
    failed++;
    console.log("FAIL  " + t.name);
    console.log("      " + String(err && err.stack ? err.stack : err).split("\n").slice(0, 6).join("\n      "));
  }
}
console.log(`\n${ran - failed}/${ran} passed`);
process.exit(failed ? 1 : 0);
