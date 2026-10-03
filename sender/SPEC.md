# SimReal 发信助手 — technical spec

The sender turns "approve on the approval page" into "the email goes out from business@simreal.co".
It is a Google Apps Script project that Charles installs under business@simreal.co, a Google Workspace mailbox: MX smtp.google.com, SPF include:_spf.google.com, DKIM selector `google`, no DMARC record yet.
It runs under his own authorization.

Hard rules:
- Nothing is sent that was not approved on the approval page.
- Claude never sends.
- The approval page and the sender only ever send what the page hands over: the finalized subject, body and follow-ups of an approved card.

## Pieces

| Path | What |
|---|---|
| `sender/Code.gs` | The whole Apps Script backend: web app (`doGet`/`doPost`), time-driven `tick()`, `setup()`. V8 runtime, plain JS, no libraries. |
| `sender/appsscript.json` | Manifest: V8, timezone `Asia/Shanghai`, Gmail advanced service v1 (`userSymbol: "Gmail"`), explicit minimal `oauthScopes` (gmail.send, gmail.readonly, spreadsheets, script.scriptapp, userinfo.email, plus anything research proves is needed), `webapp: {executeAs: "USER_DEPLOYING", access: "ANYONE_ANONYMOUS"}`. |
| `sender/test/` | Node test harness: loads `Code.gs` in a `vm` context with in-memory fakes of every Apps Script service used, runs scenario tests. `node sender/test/run.js` must pass. |
| `approval/index.html` | The approval page (claude.ai artifact). Gains a "自动发送" connection in 发件设置 and auto-send buttons and status. |
| `ops/sender-setup.md` | Chinese setup guide for Charles. |

## Web app API (contract between page and backend)

The base URL is the deployment URL (`https://script.google.com/macros/s/<id>/exec`). Every call carries the shared secret `token` that `setup()` generates and stores in Script Properties as `TOKEN`. A wrong or missing token gives `{ok:false, error:"unauthorized"}` and does nothing.

**Request forms.** `doPost` accepts two forms:
1. `fetch` form: the body is a JSON string sent with `Content-Type: text/plain;charset=utf-8`, which avoids a CORS preflight. Shape: `{"token": "...", "action": "...", ...fields}`. The backend reads `e.postData.contents`. The response is `ContentService` JSON.
2. HTML form fallback: a normal `<form method="post" target="_blank">` with one field `payload` holding the same JSON string. The backend reads `e.parameter.payload`. The response is a small Chinese `HtmlService` page that states the result, for example "已加入发送队列 3 封，跳过 1 封（原因）。可以关掉这个标签页。"

**GET requests.**
- `doGet` with `?action=status&token=...` returns the same JSON as POST `status`.
- `?action=dashboard&token=...`, or no action with a valid token, renders a read-only Chinese HTML dashboard. It shows:
  - paused or running;
  - sent today against the cap;
  - counts by status;
  - a table of every row: company, recipient, status, step, last sent, next send, outcome, error;
  - the last 50 log events.
- The dashboard has two POST forms, 暂停全部 and 继续发送. They carry the token in a hidden `payload` and use the form fallback path.

**Response envelope.** Every JSON response is `{ok: true, ...}` or `{ok: false, error: "<code>", message: "<Chinese explanation>"}`. Error codes: `unauthorized`, `bad_request`, `not_set_up`, `busy` (lock timeout), `internal`.

**Actions.**
- `ping` → `{ok, from, paused, dailyCap, sentToday, counts: {queued, active, finished, replied, bounced, cancelled, error}, version}`.
  - `from` is `Session.getEffectiveUser().getEmail()`.
- `enqueue` takes `{messages: [Msg]}` with at most 60 messages per call. It returns `{ok, results: [{slug, result, reason}]}`. `result` is one of:
  - `queued`: a new row;
  - `updated`: the row was still `queued`, never sent, and its content was replaced;
  - `duplicate`: the slug already exists past `queued`; nothing changes;
  - `rejected`: `reason` is one of `invalid_to`, `placeholder:<the token>`, `empty`, `wave_hold`, `suppressed`, `address_in_use:<other slug>`, `too_long`.
- `cancel` takes `{slug}` and returns `{ok, slug, status}`.
  - A row in `queued` or `active` becomes `cancelled`; no further email goes out.
  - Any other status is returned unchanged.
- `pause` and `resume` set the global `PAUSED` property.
  - While paused, `tick` sends nothing but still checks replies.
- `status` takes `{slugs?: [..]}`; without `slugs` it covers all rows. It returns `{ok, paused, sentToday, dailyCap, now, items: [Item]}`, where:
  - `Item = {slug, to, status, step, total, log: [{step, at, messageId, threadId}], nextAt, outcome, outcomeAt, error, revision}`;
  - `step` is the number of emails sent so far;
  - `total` is 1 + the number of follow-ups;
  - `nextAt` is an ISO time or null;
  - `outcome` is `replied`, `bounced`, `cancelled` or null;
  - `at` values are ISO strings.
- `test` takes `{}` and immediately sends one plain-text email from the account to itself.
  - Subject: "SimReal 发信助手测试". The body says setup works and gives the time.
  - It returns `{ok, messageId, threadId}`.
  - It does not count toward the cap and needs no queue row.

**Msg**, built by the page from the finalized text, the same text as the Gmail compose link:
```
{
  slug: "v-conviction",            // unique key, the db doc id
  track: "investor"|"partner"|"customer",
  company: "Conviction", contact: "Sarah Guo",
  to: "sarah@conviction.com",      // exactly one address
  subject: "...",                  // first email subject
  body: "...",                     // first email body, plain text, \n newlines
  followups: [{day: 5, text: "..."}, {day: 12, text: "..."}],  // day = days after the FIRST email
  lang: "en"|"zh", region: "海外（美国）",
  tz: "America/Los_Angeles",       // IANA tz for the send window
  wave: 1|2|3,                     // C=1, B=2, A=3 (investors); 9 = hold, rejected; non-investors send 2
  order: 2610,                     // tie-break inside a wave
  revision: 1,
  fromName: "Charles"              // display name for From; falls back to Script Property FROM_NAME, then none
}
```

**Validation at enqueue, repeated at send time.** Each check is defensive:
- `to` must match a single plain address, `^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]{2,}$`.
- `subject` and `body` must be non-empty after trimming.
- No placeholder may remain in the subject, the body or any follow-up. A placeholder is any `[...]` with up to 80 characters and no line break inside, such as `[Your name]`, `[Deck link]`, `[BP 链接]`, `[姓名]`, `[介绍人]`, `[One line about them...]`, or the bare `[ ]` in `微信/电话：[ ]`. Rejected text gives `placeholder:<the token>`.
- Total size must stay at or under 40,000 characters.
- `wave` 9 is rejected.
- The address is lowercased. It must not be on the suppression list.
- The address must not belong to another slug whose status is `queued`, `active`, `finished` or `replied`. The same person never gets two sequences.

## Storage: one Google Sheet

`setup()` creates the spreadsheet "SimReal 发信助手" in the user's Drive, or reuses it via Script Property `SHEET_ID`. It has three tabs with Chinese headers, so Charles can read them:
- `队列`: one row per slug. Columns, fixed order:
  - slug, 状态, 收件人, 公司, 联系人, 分组, 语言, 时区;
  - 主题, 已发封数, 总封数, 下次发送, 首封时间, 最近发送;
  - threadId, 最近 Message-ID, 结果, 结果时间;
  - 错误, 尝试次数, 入队时间, 修订, 内容JSON, 上次检查.
  - `内容JSON` holds `{subject, body, followups, fromName, track, order, region}`.
  - The 状态 values are English codes: `queued`, `active`, `finished`, `replied`, `bounced`, `cancelled`, `error`. The dashboard and `status` use them.
  - Charles may set a row's 状态 to `cancelled` by hand. `tick` respects it.
- `记录`: an append-only log with columns 时间, slug, 收件人, 步骤, 事件, 主题, messageId, threadId, 说明.
  - 事件 is one of `sent`, `replied`, `bounced`, `auto_reply`, `error`, `cancelled`, `queued`, `updated`, `test`.
- `屏蔽`: columns 邮箱, 原因, 时间. Bounced addresses are added automatically. Charles can add more.

**Concurrency.** `doPost` and `tick` both take `LockService.getScriptLock()`:
- `doPost` uses `waitLock(20000)` and returns `busy` on timeout.
- `tick` uses `tryLock(1000)` and skips the run if the lock is held.

Read the whole `队列` range once per run and write back only the changed rows.

**Script Properties.** All of these are created by `setup()` with defaults, and all can be changed in the editor:
- `TOKEN`: 32+ random characters from `Utilities.getUuid()` twice, without dashes.
- `SHEET_ID`
- `PAUSED`: `false`
- `DAILY_CAP`: 30. This counts first emails and follow-ups, per day in the script timezone.
- `PER_TICK`: 1. The maximum number of emails one tick sends.
- `MIN_GAP_MINUTES`: 4. The minimum gap between any two sends.
- `WINDOW_START`: 8. `WINDOW_END`: 18. Local hours in the recipient's tz, Monday–Friday only.
- `DOMAIN_GAP_HOURS`: 24. No two first emails to the same recipient domain within this many hours. Free-mail domains (gmail.com, outlook.com, hotmail.com, yahoo.com, icloud.com, qq.com, 163.com, 126.com, foxmail.com) are exempt.
- `FROM_NAME`: empty.
- `MAX_ATTEMPTS`: 3.
- `CHECKS_PER_TICK`: 40.

## tick(): runs every 5 minutes, installed by setup()

`setup()` installs a time-based trigger on `tick`, every 5 minutes. It first deletes any existing `tick` triggers, so it is idempotent.

1. Take the lock. Load the rows. Load `now` from `now_()`, a single function that tests can override.
2. **Check replies and bounces.**
   - Scope: `active` rows, plus `finished` rows whose last send was within 14 days. Take up to `CHECKS_PER_TICK` of them, ordered by oldest 上次检查 first.
   - Call `Gmail.Users.Threads.get('me', threadId, {format: 'metadata', metadataHeaders: ['From','Subject','Auto-Submitted','X-Autoreply','X-Autorespond','Precedence']})`.
   - Consider only messages with an `internalDate` after our first send. Ignore messages whose From address is ours: the effective user's email and its send-as aliases. Get the aliases from `Gmail.Users.Settings.SendAs.list('me')` and cache them per run. Do not use `GmailApp`: it pulls in the full `https://mail.google.com/` scope.
   - A From of mailer-daemon@ or postmaster@ means **bounced**: stop the row and add the address to `屏蔽`.
   - An auto-reply means: `Auto-Submitted` present and not `no`; or `X-Autoreply` or `X-Autorespond` present; or `Precedence: auto_reply`; or a subject matching `/out of office|automatic reply|auto(matic)?[- ]?reply|autoreply|自动回复|休假|不在办公室/i`. Log `auto_reply` and keep the sequence.
   - Any other message means **replied**. Set 结果 = replied and 结果时间 = that message's time, and stop the sequence.
   - Also run `Gmail.Users.Messages.list('me', {q: 'from:(mailer-daemon OR postmaster) newer_than:3d', maxResults: 20})`. For each hit, get the snippet with metadata. Mark as bounced any active or finished row whose address appears in the snippet or in a `X-Failed-Recipients` header.
   - Update 上次检查 on every row this step checks.
3. **If paused, stop here.**
4. **Pick at most `PER_TICK` sends.**
   - Stop if the daily cap is reached. sentToday counts the 记录 `sent` events dated today in the script tz.
   - Stop if the last send was less than `MIN_GAP_MINUTES` ago.
   - The recipient must be inside the send window: the weekday from `Utilities.formatDate(now, tz, 'u')` must be 1–5, and the hour (`'H'`) must be ≥ `WINDOW_START` and < `WINDOW_END`.
   - Due follow-ups go first. For an `active` row, step k (1-based) is due when now ≥ 首封时间 + `followups[k-1].day` days. Do not send two emails of the same sequence within 20 hours of each other, even if several are overdue. That situation arises after a pause.
   - Then first emails from `queued` rows. Order: wave ascending (1, 2, 3), then order ascending, then 入队时间. Skip a row while its domain gap is not clear. Skip any row whose 状态 is no longer `queued`.
4b. **Before a follow-up**, run the step-2 reply and bounce check on that row's thread in the same tick, whatever its 上次检查. Send only if the row is still `active` and has no reply. A reply that arrived since the last round-robin check must never get a follow-up.
5. **Send** with `Gmail.Users.Messages.send({raw, threadId?}, 'me')`. The raw message:
   - ASCII-only MIME with CRLF line endings. `From: <encoded fromName> <me>`.
   - `To`. `Subject` RFC 2047-encoded (`=?UTF-8?B?...?=`) when it is not pure ASCII.
   - `MIME-Version: 1.0`, `Content-Type: text/plain; charset=UTF-8`, `Content-Transfer-Encoding: base64`.
   - The body is UTF-8 with its `\n` normalized to CRLF, base64-encoded and wrapped at 76 characters.
   - `raw` is the web-safe base64 of those bytes.
   - A follow-up also sets `threadId`, `In-Reply-To` and `References`, both being the Message-ID of our previous message, and `Subject: Re: <first subject>`. Its body is the follow-up text.
   - After the send, call `Gmail.Users.Messages.get('me', id, {format: 'metadata', metadataHeaders: ['Message-ID']})`, matching the header name case-insensitively. Store the threadId and Message-ID.
   - Update the row: 已发封数 + 1, 最近发送, 首封时间 on the first email, 状态 `active`, or `finished` after the last step. Then append a `sent` row to 记录.
   - **On failure**, increment 尝试次数 and record 错误.
     - An error whose message mentions `Invalid To header`, `Invalid recipient` or `invalid address`, or reaching `MAX_ATTEMPTS`, sets 状态 `error`.
     - Otherwise the row stays and is retried on a later tick.
     - Never retry inside the same tick.
6. **Re-validate before every send** with the validation above. On failure, set 状态 `error` and record the reason. This catches edits made by hand in the sheet.
7. Write back the changed rows, release the lock, and log a one-line summary with `console.log`.

`setup()` does the following, and is safe to run again:
- creates or reuses the sheet;
- creates any missing properties (it never overwrites existing values except that a missing TOKEN is generated);
- installs the trigger;
- logs the sheet URL, the token, and the next steps in Chinese: deploy as a web app, then paste the URL and token into the approval page.

## Approval page integration (`approval/index.html`)

**Connection.**
- The URL and token live in `localStorage` key `simreal.sender` as `{url, token}`. Every access is wrapped in try/catch.
- They are never stored in the db; the db is shared state.
- The db `settings/sender` doc may only gain a non-secret boolean `autoSend` flag, so Claude can see that it is in use.

**发件设置.** Add a block "自动发送（发信助手）" with:
- 地址 input; 口令 input (`type=password`); 保存 button.
- 测试连接 button. It calls `ping` and shows "已连接 business@simreal.co · 今天已发 3/30 · 排队 5 封 · 运行中/已暂停", or a Chinese error.
- 试发一封给自己 button. It calls `test`, on click only.
- 打开发信助手 link. It goes to the dashboard: url + `?action=dashboard&token=` + token, with `target=_blank` and `rel=noopener`.
- 断开 button.
- One line of help pointing to `ops/sender-setup.md`.

**Transport.** `senderCall(action, data)`:
- First it tries `fetch(url, {method: 'POST', headers: {'Content-Type': 'text/plain;charset=utf-8'}, body: JSON.stringify({token, action, ...data}), redirect: 'follow'})` and parses the JSON.
- If `fetch` itself throws (a CSP block or a network error), the page sets `state.senderTransport = 'form'`.
  - For mutating actions (`enqueue`, `cancel`, `pause`, `resume`, `test`), it submits a hidden `<form method="post" action=url target="_blank">` with a single `payload` field, in a fresh tab.
  - In that mode the page cannot read results. It writes optimistic state and tells the user that status is shown on the 发信助手 page.
  - `status` and `ping` have no form fallback. Show "此浏览器里审批页无法直接读取发信助手状态，请点'打开发信助手'查看。"

**Building a Msg from a card.**
- `subject` is `doc.subject`.
- `body` is `bodyOf(doc, 0)`.
- `followups[i]` is `{day: doc.followups[i].day, text: bodyOf(doc, i+1)}`.
- `to` is `toOf(doc)`.
- `tz` comes from the region:
  - Parse 地区 from `doc.meta_md` (`地区：海外（美国，纽约）`), falling back to `doc.region`.
  - 国内 → Asia/Shanghai. 香港 → Asia/Hong_Kong. 新加坡 → Asia/Singapore. 英国 → Europe/London. 荷兰 or 欧洲 → Europe/Amsterdam. 以色列 → Asia/Jerusalem. 韩国 → Asia/Seoul. 日本 → Asia/Tokyo. 加拿大 → America/Toronto.
  - Within the US: 纽约, 康涅狄格 and 费城 → America/New_York; 芝加哥 → America/Chicago; anything else in the US (美国, 西雅图, 湾区 and so on) → America/Los_Angeles.
  - Any other 海外 → America/Los_Angeles.
- `fromName` is `settings.nameEn` for `en` and `settings.nameZh` for `zh`.
- `wave` is `doc.wave`, or 2 for non-investor tracks.
- The page refuses to enqueue in these cases and says why on the card:
  - `missingIn()` finds a placeholder in the subject, body or any follow-up;
  - `to` is empty;
  - `wave === 9`.

**Card flow when connected.** "Connected" means a url and token are saved.
- The approve button reads "批准并自动发送". Clicking it does two things:
  - writes the review as approved, exactly as today;
  - enqueues that one card.
- On `queued` or `updated`, the page writes `send.auto = {status: 'queued', queuedAt, revision}` into the doc. The existing `send.log` and `send.outcome` stay untouched.
- On a rejection, it writes nothing to `send.auto` and shows the reason on the card.
- Already-approved cards in stage `tosend` get a button "交给发信助手".
- The toolbar in the 待发送 filter gets "全部交给发信助手（N 封）". It enqueues every eligible `tosend` card in the current tab, 50 per request, and shows a summary.
- A card with `send.auto` shows its auto status instead of the manual buttons:
  - 排队中（预计按分组顺序在工作时间发出）;
  - 已发首封 MM-DD HH:mm，第 2 封约 MM-DD;
  - 已回复, 退信, 已取消 or 发送失败：<error>.
- It also gets a "停止自动发送" button, which calls `cancel`.
- The manual buttons (open Gmail, 标记已发送, and so on) stay for cards without `send.auto`, and whenever the sender is not connected.

**Status sync.** The page runs a sync once after the db snapshot arrives and then every 3 minutes while `document.visibilityState === 'visible'`. Only the fetch transport syncs. Each sync:
- calls `status` with the slugs that have `send.auto`;
- maps each item onto the doc, writing only when something changed:
  - `send.log` becomes the item's log, as `{step, at}` entries;
  - `send.outcome` becomes `replied` when the item is replied; `stopped` when it is cancelled, bounced or error; otherwise it keeps the current value;
  - `send.auto` becomes `{status, step, total, nextAt, error, outcome, syncedAt}`, with `queuedAt` and `revision` preserved.

Because `send.log` is kept in sync, the existing stage machine keeps working. Two new stages render for auto rows:
- `autoqueued`: "排队中（自动）";
- `bounced`: "退信".

Add both to STAGE and to the filters where sensible. An auto row in the waiting state shows "自动跟进" wording, not "跟进到期". The page must not offer manual-send buttons for steps the sender owns.

Everything else on the page works exactly as before when no sender is connected.
