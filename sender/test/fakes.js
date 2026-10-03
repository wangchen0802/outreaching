"use strict";
// In-memory fakes of the Apps Script services sender/Code.gs uses, with the real call signatures:
// SpreadsheetApp, PropertiesService, LockService, Utilities, Session, ContentService, HtmlService,
// ScriptApp, the Gmail advanced service, and console. Each one models only what Code.gs needs, and
// throws where the real service would (range sizes, sheet bounds, unknown date-pattern letters,
// missing threads), so a call Code.gs gets wrong fails here instead of in Charles's account.

const crypto = require("crypto");
const util = require("util");

const DAY = 86400000;

function isDate(v) {
  return Object.prototype.toString.call(v) === "[object Date]";
}

// ---- MIME helpers shared with the tests ----

function headerOf(headers, name) {
  const want = name.toLowerCase();
  const h = headers.find((x) => x.name.toLowerCase() === want);
  return h ? h.value : "";
}

// RFC 2047: whitespace between adjacent encoded-words is dropped, and each word must decode on its own.
function decodeWords(s) {
  return String(s).replace(/\?=\s+=\?/g, "?==?").replace(/=\?([^?]+)\?([BbQq])\?([^?]*)\?=/g, (m, cs, enc, data) => {
    if (enc.toUpperCase() !== "B") throw new Error("fake: only B-encoded words are modelled");
    if (cs.toUpperCase() !== "UTF-8") throw new Error("fake: only UTF-8 encoded words are modelled");
    const text = Buffer.from(data, "base64").toString("utf8");
    if (text.includes("�")) throw new Error("fake: an encoded-word splits a character: " + m);
    return text;
  });
}

function addressOf(from) {
  const angle = /<([^<>]*)>/.exec(from);
  return (angle ? angle[1] : String(from)).trim().toLowerCase();
}

// Decodes a Gmail `raw` value and notes everything that breaks the SPEC's MIME rules.
function parseRaw(raw) {
  const problems = [];
  if (/[^A-Za-z0-9\-_=]/.test(raw)) problems.push("raw is not web-safe base64");
  const buf = Buffer.from(raw.replace(/-/g, "+").replace(/_/g, "/"), "base64");
  if (buf.some((b) => b > 127)) problems.push("MIME has non-ASCII bytes");
  const text = buf.toString("latin1");
  if (/(^|[^\r])\n/.test(text)) problems.push("MIME has a bare LF");
  if (/\r(?!\n)/.test(text)) problems.push("MIME has a bare CR");
  const split = text.indexOf("\r\n\r\n");
  if (split === -1) problems.push("MIME has no blank line after the headers");
  const head = split === -1 ? text : text.slice(0, split);
  const bodyRaw = split === -1 ? "" : text.slice(split + 4);
  head.split("\r\n").forEach((line) => {
    if (line.includes("=?") && line.length > 76) problems.push("encoded-word header line over 76 characters: " + line);
    if (line.length > 998) problems.push("header line over 998 characters");
  });
  const headers = head.replace(/\r\n(?=[ \t])/g, "").split("\r\n").map((line) => {
    const i = line.indexOf(":");
    if (i < 1) problems.push("malformed header line: " + line);
    return { name: line.slice(0, i), value: line.slice(i + 1).replace(/^[ \t]+/, "") };
  });
  let body = bodyRaw;
  if (headerOf(headers, "Content-Transfer-Encoding").toLowerCase() === "base64") {
    bodyRaw.split("\r\n").forEach((line) => {
      if (line.length > 76) problems.push("base64 body line over 76 characters");
    });
    body = Buffer.from(bodyRaw.replace(/\s+/g, ""), "base64").toString("utf8");
  }
  return { headers, body, bodyRaw, problems, mime: text };
}

function baseSubject(s) {
  let t = decodeWords(s).trim();
  while (/^(re|fwd?)\s*:\s*/i.test(t)) t = t.replace(/^(re|fwd?)\s*:\s*/i, "");
  return t;
}

// ---- Factory ----

function makeFakes(opts) {
  const CtxDate = opts.Date; // dates handed to the script are built in its own realm
  const clock = opts.clock; // { ms }
  const me = opts.me;
  const scriptTz = opts.timeZone || "Asia/Shanghai";
  const serviceUrl = "https://script.google.com/macros/s/FAKE_DEPLOYMENT/exec";
  const output = { log: [], warn: [], error: [] };

  // ---- SpreadsheetApp ----

  const books = new Map();

  function toCell(v, format) {
    if (v === null || v === undefined) return "";
    if (isDate(v)) return { date: v.getTime() };
    if (typeof v === "number" || typeof v === "boolean") return v;
    if (typeof v !== "string") throw new Error("fake Sheets: cannot store a " + typeof v + " in a cell");
    if (v.length > 50000) throw new Error("Your input contains more than the maximum of 50000 characters in a single cell.");
    if (format === "@") return v;
    // Without plain-text format, Sheets parses what looks like a number or a formula.
    if (/^\s*[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?\s*$/.test(v)) return Number(v);
    if (/^=/.test(v)) throw new Error("fake Sheets: " + JSON.stringify(v.slice(0, 40)) + " would become a formula");
    return v;
  }

  function fromCell(c) {
    if (c === undefined) return "";
    if (c && typeof c === "object") return new CtxDate(c.date);
    return c;
  }

  class Range {
    constructor(sheet, row, col, numRows, numCols) {
      Object.assign(this, { sheet, row, col, numRows, numCols });
    }
    getRow() { return this.row; }
    getColumn() { return this.col; }
    getNumRows() { return this.numRows; }
    getNumColumns() { return this.numCols; }
    getValues() {
      const out = [];
      for (let r = 0; r < this.numRows; r++) {
        const line = [];
        for (let c = 0; c < this.numCols; c++) line.push(fromCell((this.sheet.cells[this.row - 1 + r] || [])[this.col - 1 + c]));
        out.push(line);
      }
      return out;
    }
    setValues(values) {
      if (!Array.isArray(values) || values.some((r) => !Array.isArray(r))) throw new Error("fake Sheets: setValues needs Object[][]");
      if (values.length !== this.numRows) {
        throw new Error(`The number of rows in the data does not match the number of rows in the range. The data has ${values.length} but the range has ${this.numRows}.`);
      }
      values.forEach((line) => {
        if (line.length !== this.numCols) {
          throw new Error(`The number of columns in the data does not match the number of columns in the range. The data has ${line.length} but the range has ${this.numCols}.`);
        }
      });
      const s = this.sheet;
      values.forEach((line, r) => {
        const rr = this.row - 1 + r;
        s.cells[rr] = s.cells[rr] || [];
        line.forEach((v, c) => {
          const cc = this.col - 1 + c;
          s.cells[rr][cc] = toCell(v, (s.formats[rr] || [])[cc]);
        });
      });
      return this;
    }
    setNumberFormat(format) {
      const s = this.sheet;
      for (let r = 0; r < this.numRows; r++) {
        const rr = this.row - 1 + r;
        s.formats[rr] = s.formats[rr] || [];
        for (let c = 0; c < this.numCols; c++) s.formats[rr][this.col - 1 + c] = format;
      }
      return this;
    }
    setFontWeight() { return this; }
  }

  class Sheet {
    constructor(book, name) {
      Object.assign(this, { book, name, cells: [], formats: [], maxRows: 1000, maxCols: 26, frozenRows: 0 });
    }
    getName() { return this.name; }
    setName(name) {
      if (this.book.sheets.some((s) => s !== this && s.name === name)) throw new Error(`A sheet with the name "${name}" already exists. Please enter another name.`);
      this.name = name;
      return this;
    }
    getParent() { return this.book; }
    getMaxRows() { return this.maxRows; }
    getMaxColumns() { return this.maxCols; }
    getLastRow() {
      for (let r = this.cells.length - 1; r >= 0; r--) if ((this.cells[r] || []).some((v) => v !== "" && v !== undefined)) return r + 1;
      return 0;
    }
    getLastColumn() {
      let max = 0;
      this.cells.forEach((line) => (line || []).forEach((v, c) => { if (v !== "" && v !== undefined) max = Math.max(max, c + 1); }));
      return max;
    }
    getRange(row, col, numRows, numCols) {
      if (arguments.length !== 2 && arguments.length !== 4) throw new Error("fake Sheets: use getRange(row, column) or getRange(row, column, numRows, numColumns)");
      if (numRows === undefined) { numRows = 1; numCols = 1; }
      [row, col, numRows, numCols].forEach((n) => { if (!Number.isInteger(n)) throw new Error("fake Sheets: range arguments must be integers, got " + n); });
      if (numRows < 1) throw new Error("The number of rows in the range must be at least 1.");
      if (numCols < 1) throw new Error("The number of columns in the range must be at least 1.");
      if (row < 1 || col < 1 || row + numRows - 1 > this.maxRows || col + numCols - 1 > this.maxCols) {
        throw new Error("The coordinates of the range are outside the dimensions of the sheet.");
      }
      return new Range(this, row, col, numRows, numCols);
    }
    getDataRange() { return this.getRange(1, 1, Math.max(1, this.getLastRow()), Math.max(1, this.getLastColumn())); }
    // New rows start without formatting here; Code.gs must format what it adds.
    insertRowsAfter(afterPosition, howMany) {
      if (!Number.isInteger(afterPosition) || afterPosition < 1 || afterPosition > this.maxRows) throw new Error("fake Sheets: bad insertRowsAfter position");
      if (!Number.isInteger(howMany) || howMany < 1) throw new Error("fake Sheets: bad insertRowsAfter count");
      const blank = Array.from({ length: howMany }, () => undefined);
      if (afterPosition < this.cells.length) this.cells.splice(afterPosition, 0, ...blank);
      if (afterPosition < this.formats.length) this.formats.splice(afterPosition, 0, ...blank);
      this.maxRows += howMany;
      return this;
    }
    setFrozenRows(rows) { this.frozenRows = rows; }
    getFrozenRows() { return this.frozenRows; }
    // Test helpers, not part of the Apps Script API.
    _format(row, col) { return (this.formats[row - 1] || [])[col - 1]; }
  }

  class Spreadsheet {
    constructor(name) {
      this.id = "sheet_" + crypto.randomBytes(6).toString("hex");
      this.name = name;
      this.sheets = [new Sheet(this, "Sheet1")];
      this.tz = "America/Los_Angeles";
    }
    getId() { return this.id; }
    getName() { return this.name; }
    getUrl() { return "https://docs.google.com/spreadsheets/d/" + this.id + "/edit"; }
    getSheets() { return this.sheets.slice(); }
    getSheetByName(name) { return this.sheets.find((s) => s.name === name) || null; }
    insertSheet(name) {
      if (typeof name !== "string") throw new Error("fake Sheets: insertSheet(name) needs a name");
      if (this.getSheetByName(name)) throw new Error(`A sheet with the name "${name}" already exists. Please enter another name.`);
      const s = new Sheet(this, name);
      this.sheets.push(s);
      return s;
    }
    setSpreadsheetTimeZone(tz) { this.tz = tz; }
    getSpreadsheetTimeZone() { return this.tz; }
  }

  const SpreadsheetApp = {
    create(name) {
      if (typeof name !== "string") throw new Error("fake Sheets: create(name) needs a name");
      const book = new Spreadsheet(name);
      books.set(book.id, book);
      return book;
    },
    openById(id) {
      const book = books.get(id);
      if (!book) throw new Error("Requested entity was not found.");
      return book;
    }
  };

  // ---- PropertiesService ----

  class Properties {
    constructor() { this.data = {}; }
    getProperty(key) { return Object.prototype.hasOwnProperty.call(this.data, key) ? this.data[key] : null; }
    setProperty(key, value) {
      if (typeof value !== "string") throw new Error("fake Properties: value for " + key + " must be a string");
      this.data[key] = value;
      return this;
    }
    getProperties() { return Object.assign({}, this.data); }
    setProperties(properties, deleteAllOthers) {
      if (deleteAllOthers) this.data = {};
      Object.keys(properties).forEach((k) => this.setProperty(k, properties[k]));
      return this;
    }
    deleteProperty(key) { delete this.data[key]; return this; }
    getKeys() { return Object.keys(this.data); }
  }
  const scriptProps = new Properties();
  const PropertiesService = { getScriptProperties: () => scriptProps };

  // ---- LockService: one script lock shared by every "execution" ----

  const lockState = { holder: null, other: { name: "another execution" } };
  class Lock {
    tryLock(timeoutInMillis) {
      if (typeof timeoutInMillis !== "number") throw new Error("fake Lock: tryLock(timeoutInMillis)");
      if (lockState.holder && lockState.holder !== this) return false;
      lockState.holder = this;
      return true;
    }
    waitLock(timeoutInMillis) {
      if (typeof timeoutInMillis !== "number") throw new Error("fake Lock: waitLock(timeoutInMillis)");
      if (lockState.holder && lockState.holder !== this) throw new Error("Lock timeout: another process was holding the lock for too long.");
      lockState.holder = this;
    }
    releaseLock() { if (lockState.holder === this) lockState.holder = null; }
    hasLock() { return lockState.holder === this; }
  }
  const LockService = { getScriptLock: () => new Lock() };

  // ---- Utilities ----

  const Charset = { UTF_8: "UTF-8", US_ASCII: "US-ASCII" };
  function bytesOf(data, charset) {
    if (Array.isArray(data)) return Buffer.from(data.map((b) => b & 0xff));
    if (typeof data !== "string") throw new Error("fake Utilities: data must be a string or a byte array");
    if (charset === undefined) {
      // The charset-less overload's encoding is not something to rely on for non-ASCII text.
      if (/[^\x00-\x7f]/.test(data)) throw new Error("fake Utilities: pass Utilities.Charset.UTF_8 for non-ASCII text");
      return Buffer.from(data, "latin1");
    }
    if (charset === Charset.UTF_8) return Buffer.from(data, "utf8");
    if (charset === Charset.US_ASCII) return Buffer.from(data.replace(/[^\x00-\x7f]/g, "?"), "latin1");
    throw new Error("fake Utilities: unknown charset " + charset);
  }

  const WEEKDAY = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };
  const WEEKDAY_LONG = { Mon: "Monday", Tue: "Tuesday", Wed: "Wednesday", Thu: "Thursday", Fri: "Friday", Sat: "Saturday", Sun: "Sunday" };
  function pad(n, width) { return String(n).padStart(width, "0"); }

  // java.text.SimpleDateFormat, for the letters Code.gs uses. Others throw so nothing goes unchecked.
  function formatDate(date, timeZone, format) {
    if (arguments.length !== 3) throw new Error("fake Utilities: formatDate(date, timeZone, format)");
    if (!isDate(date)) throw new Error("fake Utilities: formatDate needs a Date");
    if (typeof timeZone !== "string" || typeof format !== "string") throw new Error("fake Utilities: timeZone and format must be strings");
    let zone = timeZone;
    try {
      new Intl.DateTimeFormat("en-US", { timeZone: zone });
    } catch (err) {
      zone = "UTC"; // java.util.TimeZone turns an unknown id into GMT
    }
    const p = {};
    new Intl.DateTimeFormat("en-US", {
      timeZone: zone, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit", weekday: "short"
    }).formatToParts(new Date(date.getTime())).forEach((x) => { p[x.type] = x.value; });
    const v = { y: +p.year, M: +p.month, d: +p.day, H: +p.hour, m: +p.minute, s: +p.second, u: WEEKDAY[p.weekday], S: date.getTime() % 1000 };
    let out = "";
    for (let i = 0; i < format.length;) {
      const ch = format[i];
      if (ch === "'") {
        const end = format.indexOf("'", i + 1);
        if (end === -1) throw new Error("fake Utilities: unterminated quote in " + format);
        out += end === i + 1 ? "'" : format.slice(i + 1, end);
        i = end + 1;
      } else if (/[A-Za-z]/.test(ch)) {
        let j = i;
        while (format[j] === ch) j++;
        const n = j - i;
        if (ch === "y") out += n === 2 ? pad(v.y % 100, 2) : pad(v.y, n);
        else if (ch === "M" && n <= 2) out += pad(v.M, n);
        else if ("dHmsuS".includes(ch)) out += pad(v[ch], n);
        else if (ch === "E") out += n <= 3 ? p.weekday : WEEKDAY_LONG[p.weekday];
        else throw new Error(`fake Utilities: pattern letter '${ch}' (x${n}) is not modelled`);
        i = j;
      } else {
        out += ch;
        i++;
      }
    }
    return out;
  }

  const Utilities = {
    Charset,
    getUuid: () => crypto.randomUUID(),
    base64Encode: (data, charset) => bytesOf(data, charset).toString("base64"),
    base64EncodeWebSafe: (data, charset) => bytesOf(data, charset).toString("base64").replace(/\+/g, "-").replace(/\//g, "_"),
    newBlob(data) {
      const bytes = bytesOf(data, typeof data === "string" ? Charset.UTF_8 : undefined);
      return {
        getBytes: () => Array.from(bytes, (b) => (b > 127 ? b - 256 : b)),
        getDataAsString: () => bytes.toString("utf8")
      };
    },
    formatDate
  };

  // ---- Session, ContentService, HtmlService ----

  const user = { getEmail: () => me };
  const Session = { getEffectiveUser: () => user, getActiveUser: () => user, getScriptTimeZone: () => scriptTz };

  class TextOutput {
    constructor(content) { this.content = String(content); this.mimeType = "TEXT"; }
    getContent() { return this.content; }
    setMimeType(mimeType) { this.mimeType = mimeType; return this; }
    getMimeType() { return this.mimeType; }
  }
  const ContentService = {
    MimeType: { JSON: "JSON", TEXT: "TEXT", CSV: "CSV" },
    createTextOutput: (content) => new TextOutput(content === undefined ? "" : content)
  };

  class HtmlOutput {
    constructor(html) { this.html = html; this.title = ""; this.metaTags = []; }
    getContent() { return this.html; }
    setTitle(title) { this.title = String(title); return this; }
    getTitle() { return this.title; }
    addMetaTag(name, content) { this.metaTags.push({ name, content }); return this; }
    setXFrameOptionsMode() { return this; }
  }
  const HtmlService = {
    XFrameOptionsMode: { DEFAULT: "DEFAULT", ALLOWALL: "ALLOWALL" },
    createHtmlOutput(html) {
      if (html !== undefined && typeof html !== "string") throw new Error("fake HtmlService: createHtmlOutput(html) needs a string");
      return new HtmlOutput(html || "");
    }
  };

  // ---- ScriptApp ----

  const triggers = [];
  let triggerSeq = 0;
  class Trigger {
    constructor(fn, spec) { this.fn = fn; this.spec = spec; this.id = "trigger_" + ++triggerSeq; }
    getHandlerFunction() { return this.fn; }
    getUniqueId() { return this.id; }
    getEventType() { return "CLOCK"; }
  }
  const ScriptApp = {
    EventType: { CLOCK: "CLOCK" },
    getProjectTriggers: () => triggers.slice(),
    deleteTrigger(trigger) {
      const i = triggers.indexOf(trigger);
      if (i === -1) throw new Error("fake ScriptApp: unknown trigger");
      triggers.splice(i, 1);
    },
    newTrigger(functionName) {
      if (typeof functionName !== "string") throw new Error("fake ScriptApp: newTrigger(functionName)");
      return {
        timeBased() {
          const spec = {};
          const builder = {
            everyMinutes(n) {
              if (![1, 5, 10, 15, 30].includes(n)) throw new Error("The number of minutes must be 1, 5, 10, 15 or 30.");
              spec.everyMinutes = n;
              return builder;
            },
            everyHours(n) { spec.everyHours = n; return builder; },
            create() {
              if (!spec.everyMinutes && !spec.everyHours) throw new Error("fake ScriptApp: a clock trigger needs a frequency");
              const t = new Trigger(functionName, spec);
              triggers.push(t);
              return t;
            }
          };
          return builder;
        }
      };
    },
    getService: () => ({ getUrl: () => serviceUrl })
  };

  // ---- Gmail advanced service: one mailbox, ours ----

  const mail = {
    messages: new Map(), threads: new Map(), sent: [], sendAttempts: [], failNext: [], failGetOnce: 0, nextIds: [],
    problems: [], calls: { send: 0, get: 0, list: 0, threadsGet: 0, sendAsList: 0 },
    sendAs: [{ sendAsEmail: me, isPrimary: true, isDefault: true }, { sendAsEmail: "charles@simreal.co", isPrimary: false }]
  };
  let idSeq = 0;
  function newId() {
    if (mail.nextIds.length) return mail.nextIds.shift();
    idSeq++;
    return (BigInt("0x18c3f0a1b2c30000") + BigInt(idSeq)).toString(16);
  }
  function needMe(userId, call) {
    if (userId !== "me") throw new Error(`fake Gmail: ${call} must be called with userId "me", got ${JSON.stringify(userId)}`);
  }
  function view(m, optionalArgs) {
    const args = optionalArgs || {};
    const format = args.format || "full";
    let headers = m.headers.map((h) => ({ name: h.name, value: h.value }));
    if (format === "metadata" && args.metadataHeaders) {
      const want = [].concat(args.metadataHeaders).map((x) => String(x).toLowerCase());
      headers = headers.filter((h) => want.includes(h.name.toLowerCase()));
    }
    const out = {
      id: m.id, threadId: m.threadId, labelIds: m.labelIds.slice(), snippet: m.snippet, historyId: "1",
      internalDate: String(m.internalDate), sizeEstimate: 2048
    };
    if (format !== "minimal") out.payload = { mimeType: "text/plain", headers };
    return out;
  }
  function apiError(call, message) {
    return new Error(`API call to gmail.users.${call} failed with error: ${message}`);
  }

  const Gmail = {
    Users: {
      Messages: {
        send(resource, userId) {
          mail.calls.send++;
          if (arguments.length !== 2) throw new Error("fake Gmail: Messages.send(resource, userId)");
          needMe(userId, "Messages.send");
          if (!resource || typeof resource.raw !== "string") throw apiError("messages.send", "'raw' RFC822 payload message string or uploading message via /upload/* URL required");
          mail.sendAttempts.push({ at: clock.ms, resource });
          const parsed = parseRaw(resource.raw);
          if (mail.failNext.length) throw apiError("messages.send", mail.failNext.shift());
          parsed.problems.forEach((p) => mail.problems.push(p));
          const to = headerOf(parsed.headers, "To");
          if (!/^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]+$/.test(to) || to.includes("..")) throw apiError("messages.send", "Invalid To header");
          let threadId = null;
          if (resource.threadId != null) {
            const ids = mail.threads.get(resource.threadId);
            if (!ids) throw apiError("messages.send", "Requested entity was not found.");
            // Gmail files a message into the thread only when it is a reply with a matching subject.
            const first = mail.messages.get(ids[0]);
            const isReply = headerOf(parsed.headers, "In-Reply-To") && headerOf(parsed.headers, "References");
            if (isReply && baseSubject(headerOf(parsed.headers, "Subject")) === baseSubject(headerOf(first.headers, "Subject"))) threadId = resource.threadId;
          }
          const id = newId();
          if (!threadId) {
            threadId = id;
            mail.threads.set(id, []);
          }
          const headers = parsed.headers.concat([
            { name: "Message-Id", value: "<CA+fake" + id + "@mail.gmail.com>" },
            { name: "Date", value: new Date(clock.ms).toUTCString() }
          ]);
          const m = { id, threadId, labelIds: ["SENT"], internalDate: clock.ms, headers, snippet: parsed.body.slice(0, 120), parsed, resource };
          mail.messages.set(id, m);
          mail.threads.get(threadId).push(id);
          mail.sent.push(m);
          if (mail.onSend) mail.onSend(m);
          return { id, threadId, labelIds: ["SENT"] };
        },
        get(userId, id, optionalArgs) {
          mail.calls.get++;
          needMe(userId, "Messages.get");
          if (mail.failGetOnce > 0) {
            mail.failGetOnce--;
            throw apiError("messages.get", "Backend Error");
          }
          const m = mail.messages.get(id);
          if (!m) throw apiError("messages.get", "Requested entity was not found.");
          return view(m, optionalArgs);
        },
        list(userId, optionalArgs) {
          mail.calls.list++;
          needMe(userId, "Messages.list");
          const args = optionalArgs || {};
          let q = String(args.q || "");
          let pool = Array.from(mail.messages.values());
          if (/from:\(mailer-daemon OR postmaster\)/.test(q)) {
            pool = pool.filter((m) => /^(mailer-daemon|postmaster)@/.test(addressOf(headerOf(m.headers, "From"))));
            q = q.replace(/from:\(mailer-daemon OR postmaster\)/, "");
          }
          const newer = /newer_than:(\d+)d/.exec(q);
          if (newer) {
            pool = pool.filter((m) => m.internalDate > clock.ms - Number(newer[1]) * DAY);
            q = q.replace(newer[0], "");
          }
          if (q.trim()) throw new Error("fake Gmail: query not modelled: " + args.q);
          pool.sort((a, b) => b.internalDate - a.internalDate);
          pool = pool.slice(0, args.maxResults || 100);
          const out = { resultSizeEstimate: pool.length };
          if (pool.length) out.messages = pool.map((m) => ({ id: m.id, threadId: m.threadId }));
          return out;
        }
      },
      Threads: {
        get(userId, id, optionalArgs) {
          mail.calls.threadsGet++;
          needMe(userId, "Threads.get");
          const ids = mail.threads.get(id);
          if (!ids) throw apiError("threads.get", "Requested entity was not found.");
          const messages = ids.map((x) => mail.messages.get(x)).sort((a, b) => a.internalDate - b.internalDate);
          return { id, historyId: "1", messages: messages.map((m) => view(m, optionalArgs)) };
        }
      },
      Settings: {
        SendAs: {
          list(userId) {
            mail.calls.sendAsList++;
            needMe(userId, "Settings.SendAs.list");
            return { sendAs: mail.sendAs.map((s) => Object.assign({}, s)) };
          }
        }
      }
    }
  };

  // Test side: a message arrives in the mailbox (a reply, an auto-reply, a bounce).
  mail.deliver = function (m) {
    const id = newId();
    let threadId = m.threadId;
    if (!threadId) {
      threadId = id;
      mail.threads.set(id, []);
    } else if (!mail.threads.has(threadId)) {
      throw new Error("fake Gmail: no thread " + threadId);
    }
    const headers = [{ name: "From", value: m.from }, { name: "To", value: me }, { name: "Subject", value: m.subject || "" }];
    Object.keys(m.headers || {}).forEach((k) => headers.push({ name: k, value: m.headers[k] }));
    mail.messages.set(id, { id, threadId, labelIds: ["INBOX", "UNREAD"], internalDate: m.at == null ? clock.ms : m.at, headers, snippet: m.snippet || "" });
    mail.threads.get(threadId).push(id);
    return id;
  };

  // ---- console ----

  const fakeConsole = {};
  ["log", "info", "warn", "error"].forEach((level) => {
    fakeConsole[level] = (...args) => {
      const line = util.format(...args);
      (output[level === "info" ? "log" : level]).push(line);
      if (process.env.VERBOSE) process.stdout.write(`    [${level}] ${line}\n`);
    };
  });

  return {
    globals: {
      SpreadsheetApp, PropertiesService, LockService, Utilities, Session, ContentService, HtmlService, ScriptApp, Gmail,
      console: fakeConsole
    },
    state: { books, props: scriptProps, lock: lockState, triggers, mail, output, serviceUrl }
  };
}

module.exports = { makeFakes, parseRaw, decodeWords, headerOf, addressOf };
