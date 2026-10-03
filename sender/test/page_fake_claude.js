// Fake claude.ai runtime for page_test.py, injected with add_init_script before the page runs.
// claude.use("db") resolves an in-memory store with the contract's semantics: set replaces,
// update merges nested objects (arrays and scalars replace) and needs an existing doc, snapshots
// are frozen and arrive asynchronously. Every write is recorded in window.__dbWrites.
// The seed comes from window.__PAGE_SEED__ = {docs: {path: body}, canEdit, pageOrigin}.
(function () {
  "use strict";
  var seed = window.__PAGE_SEED__;
  if (!seed || location.origin !== seed.pageOrigin || window.__fakeClaude) return;
  window.__fakeClaude = true;

  function clone(v) { return v === undefined ? undefined : JSON.parse(JSON.stringify(v)); }
  function plain(v) { return v !== null && typeof v === "object" && !Array.isArray(v); }
  function freeze(v) {
    if (v && typeof v === "object") { Object.values(v).forEach(freeze); Object.freeze(v); }
    return v;
  }
  function merge(target, patch) {
    Object.keys(patch).forEach(function (k) {
      if (plain(patch[k]) && plain(target[k])) target[k] = merge(Object.assign({}, target[k]), patch[k]);
      else target[k] = clone(patch[k]);
    });
    return target;
  }
  function err(code, message) { var e = new Error(message); e.code = code; return e; }

  var store = {};
  Object.keys(seed.docs || {}).forEach(function (p) { store[p] = freeze(clone(seed.docs[p])); });
  var writes = window.__dbWrites = [];
  var docSubs = {}, colSubs = {};
  var meta = { fromCache: false, hasPendingWrites: false };

  function colOf(path) { return path.split("/").slice(0, -1).join("/"); }
  function docSnap(path) {
    var d = store[path];
    return { id: path.split("/").pop(), exists: !!d, data: function () { return d; }, metadata: meta };
  }
  function colSnap(col) {
    var docs = Object.keys(store).filter(function (p) { return colOf(p) === col; }).sort().map(docSnap);
    return { docs: docs, size: docs.length, empty: !docs.length, docChanges: function () { return []; }, metadata: meta };
  }
  function notify(path) {
    setTimeout(function () {
      (docSubs[path] || []).forEach(function (fn) { fn(docSnap(path)); });
      var col = colOf(path);
      (colSubs[col] || []).forEach(function (fn) { fn(colSnap(col)); });
    }, 0);
  }
  function subscribe(map, key, fn, snap) {
    (map[key] = map[key] || []).push(fn);
    setTimeout(function () { fn(snap()); }, 0);
    return function () { map[key] = (map[key] || []).filter(function (f) { return f !== fn; }); };
  }
  function checkPath(path, even) {
    var n = String(path).split("/").length;
    if ((n % 2 === 0) !== even) throw new TypeError("bad path parity: " + path);
  }

  function docRef(path) {
    checkPath(path, true);
    return {
      id: path.split("/").pop(), path: path,
      get: function () { return Promise.resolve(docSnap(path)); },
      set: function (data) {
        if (!plain(data)) return Promise.reject(err("invalid_argument", "body must be an object"));
        writes.push({ op: "set", path: path, data: clone(data) });
        store[path] = freeze(clone(data));
        notify(path);
        return Promise.resolve();
      },
      update: function (data) {
        if (!store[path]) return Promise.reject(err("invalid_argument", "update needs an existing document"));
        writes.push({ op: "update", path: path, data: clone(data) });
        store[path] = freeze(merge(clone(store[path]), data));
        notify(path);
        return Promise.resolve();
      },
      delete: function () {
        writes.push({ op: "delete", path: path });
        delete store[path];
        notify(path);
        return Promise.resolve();
      },
      onSnapshot: function (next) { return subscribe(docSubs, path, next, function () { return docSnap(path); }); }
    };
  }
  var db = Object.freeze({
    doc: docRef,
    collection: function (col) {
      checkPath(col, false);
      return {
        path: col,
        doc: function (id) { return docRef(col + "/" + id); },
        get: function () { return Promise.resolve(colSnap(col)); },
        onSnapshot: function (next) { return subscribe(colSubs, col, next, function () { return colSnap(col); }); }
      };
    }
  });
  var downloads = window.__downloads = [];
  var caps = {
    db: db,
    downloads: { save: function (f) { downloads.push(f); return Promise.resolve(); } },
    user: { canEdit: function () { return Promise.resolve(seed.canEdit !== false); }, isOwner: function () { return Promise.resolve(true); } }
  };
  window.__dbStore = function () { return clone(store); };
  window.claude = Object.freeze({
    use: function (name) {
      return new Promise(function (resolve) { setTimeout(function () { resolve(caps[name] || null); }, 5); });
    }
  });
})();
