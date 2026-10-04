"""Build the Duke funding and startup-support guide from the research JSON files.

Input:  intel/resources/duke/*.json   (each a JSON array of programs, one file per research segment)
Output: lists/duke-funding-and-support.csv   (one row per program)
        lists/duke-contacts.csv              (one row per named contact or published inbox)
        collateral/src/duke-funding-and-support.html
        collateral/SimReal-Duke-funding-and-support.pdf

Usage: python3 tools/build_duke_support.py
"""
import csv
import datetime
import html
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "resources" / "duke"
OUT_CSV = ROOT / "lists" / "duke-funding-and-support.csv"
OUT_CONTACTS = ROOT / "lists" / "duke-contacts.csv"
OUT_HTML = ROOT / "collateral" / "src" / "duke-funding-and-support.html"
OUT_PDF = ROOT / "collateral" / "SimReal-Duke-funding-and-support.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

SEGMENTS = ["Duke programs", "Duke networks and student funds", "Research Triangle, NC and federal",
            "Student-founder programs and competitions"]
FIT = {"High": 0, "Medium": 1, "Low": 2}
STATUS = {"open": 0, "rolling": 1, "upcoming": 2, "unconfirmed": 3, "closed": 4}
QUAL = {"yes": 0, "likely": 1, "unclear": 2, "no": 3}
COLS = ["segment", "name", "org", "category", "what_you_get", "eligibility", "simreal_qualifies", "timing",
        "status", "how_to_apply", "fit", "fit_why", "contacts", "confidence", "sources"]
NOT_FOUND = {"", "not found", "none", "n/a", "unknown"}


def blank(v):
    return str(v or "").strip().lower() in NOT_FOUND


def norm_status(s):
    s = str(s or "").lower()
    for k in STATUS:
        if k in s:
            return k
    return "unconfirmed"


def key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def load():
    items, seen = [], {}
    for path in sorted(SRC.glob("*.json")):
        for it in json.load(open(path, encoding="utf-8")):
            it["status_key"] = norm_status(it.get("status"))
            k = key(it["name"])
            if k in seen:
                # Same program found by two segments: keep the higher-confidence record, merge contacts.
                old = seen[k]
                names = {key(c.get("name", "")) for c in old.get("contacts") or []}
                old.setdefault("contacts", []).extend(c for c in it.get("contacts") or [] if key(c.get("name", "")) not in names)
                continue
            seen[k] = it
            items.append(it)
    items.sort(key=lambda i: (SEGMENTS.index(i["segment"]) if i.get("segment") in SEGMENTS else 9,
                              FIT.get(i.get("fit"), 3), QUAL.get(str(i.get("simreal_qualifies", "")).lower(), 4),
                              STATUS[i["status_key"]], i["name"]))
    return items


def contact_str(c):
    parts = [c.get("name", ""), c.get("role", "")]
    if not blank(c.get("email")):
        parts.append(c["email"])
    return ", ".join(p for p in parts if p)


def e(s):
    return html.escape(str(s or ""))


def link(s):
    out = e(s).replace(" (search snippet)", "").replace(" (read)", "")
    return re.sub(r"(https?://[^\s<>\"')，;]+)",
                  lambda m: f'<a href="{m.group(1)}">{m.group(1).split("://", 1)[1].rstrip("/")[:60]}</a>', out)


def write_csvs(items):
    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for i in items:
            row = {c: i.get(c, "") for c in COLS}
            row["contacts"] = " ; ".join(contact_str(c) for c in i.get("contacts") or [])
            row["sources"] = " ; ".join(i.get("sources") or [])
            w.writerow(row)
    rows = []
    for i in items:
        for c in i.get("contacts") or []:
            if blank(c.get("name")) and blank(c.get("email")):
                continue
            rows.append({"name": c.get("name", ""), "role": c.get("role", ""), "org": i.get("org", ""),
                         "program": i["name"], "program_fit": i.get("fit", ""),
                         "email": "" if blank(c.get("email")) else c["email"],
                         "email_source": "" if blank(c.get("email")) else c.get("email_source", ""),
                         "profile_url": "" if blank(c.get("profile_url")) else c["profile_url"]})
    uniq, seen = [], set()
    for r in rows:
        k = (key(r["name"]), r["email"].lower())
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    uniq.sort(key=lambda r: (FIT.get(r["program_fit"], 3), r["org"], r["name"]))
    with open(OUT_CONTACTS, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(uniq[0].keys()) if uniq else ["name"])
        w.writeheader()
        w.writerows(uniq)
    return uniq


def card(i):
    q = str(i.get("simreal_qualifies", "")).lower()
    rows = [("What you get", e(i.get("what_you_get"))), ("Eligibility", e(i.get("eligibility"))),
            ("Timing", e(i.get("timing"))), ("How to apply", link(i.get("how_to_apply"))),
            ("Why it fits", e(i.get("fit_why")))]
    cs = [c for c in i.get("contacts") or [] if not (blank(c.get("name")) and blank(c.get("email")))]
    if cs:
        lines = []
        for c in cs:
            bits = [f"<b>{e(c.get('name'))}</b>" if not blank(c.get("name")) else "", e(c.get("role"))]
            if not blank(c.get("email")):
                bits.append(e(c["email"]))
            if not blank(c.get("profile_url")):
                bits.append(link(c["profile_url"]))
            lines.append(", ".join(b for b in bits if b))
        rows.append(("Contacts", "<br>".join(lines)))
    body = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows if v)
    return (f'<div class="card fit-{e(i.get("fit", "")).lower()}"><div class="head"><div><div class="name">{e(i["name"])}</div>'
            f'<div class="role">{e(i.get("org"))} · {e(i.get("category"))}</div></div>'
            f'<span class="tag q-{e(q)}">SimReal qualifies: {e(q or "unclear")}</span>'
            f'<span class="tag st">{e(i["status_key"])}</span><span class="pill">{e(i.get("fit"))} fit</span></div>'
            f'<table class="kv">{body}</table></div>')


def write_pdf(items, contacts):
    today = datetime.date.today().isoformat()
    top = [i for i in items if i.get("fit") == "High" and str(i.get("simreal_qualifies", "")).lower() in ("yes", "likely")
           and i["status_key"] in ("open", "rolling", "upcoming")]
    start = "".join(f"<tr><td><b>{e(i['name'])}</b><br><span class='muted'>{e(i.get('org'))}</span></td>"
                    f"<td>{e(i.get('what_you_get'))}</td><td>{e(i.get('timing'))}</td><td>{link(i.get('how_to_apply'))}</td></tr>"
                    for i in top)
    sections = []
    for seg in SEGMENTS + ["Other"]:
        seg_items = [i for i in items if (i.get("segment") if i.get("segment") in SEGMENTS else "Other") == seg]
        if seg_items:
            sections.append(f"<h2>{e(seg)} · {len(seg_items)}</h2>" + "".join(card(i) for i in seg_items))
    ctab = "".join(f"<tr><td><b>{e(c['name'])}</b><br><span class='muted'>{e(c['role'])}</span></td><td>{e(c['org'])}</td>"
                   f"<td>{e(c['email']) or '<span class=muted>not published</span>'}</td><td>{link(c['profile_url'])}</td></tr>"
                   for c in contacts)
    n_email = sum(bool(c["email"]) for c in contacts)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Duke Funding Guide</title>
<style>
@page {{ size: Letter; margin: 14mm 13mm; }}
:root {{ --ink:#1b2430; --muted:#5b6675; --line:#dfe3e8; --blue:#00539B; --high:#1a7f4b; --med:#b7791f; --low:#8a94a3; }}
body {{ font-family: "DejaVu Sans", Arial, sans-serif; color: var(--ink); font-size: 9pt; line-height: 1.42; background:#fff; margin:0; }}
h1 {{ color: var(--blue); font-size: 20pt; margin: 0 0 2pt; }}
h2 {{ color: var(--blue); font-size: 13pt; border-bottom: 2px solid var(--blue); padding-bottom: 2pt; margin: 16pt 0 8pt; break-after: avoid; }}
.sub, .muted {{ color: var(--muted); }}
.facts {{ display:flex; gap:8pt; margin:8pt 0; }}
.fact {{ flex:1; border:1px solid var(--line); border-radius:5pt; padding:6pt 8pt; }}
.fact b {{ display:block; font-size:15pt; color: var(--blue); }}
ul.notes {{ margin:4pt 0 0 14pt; padding:0; }}
table.sum {{ width:100%; border-collapse: collapse; font-size: 8.2pt; }}
table.sum th {{ text-align:left; background:#eef3f9; color: var(--blue); padding:3pt 4pt; }}
table.sum td {{ border-bottom: 1px solid var(--line); padding:3pt 4pt; vertical-align: top; }}
table.sum tr {{ break-inside: avoid; }}
.card {{ border:1px solid var(--line); border-left: 4px solid var(--blue); border-radius: 5pt; padding: 7pt 9pt; margin: 0 0 8pt; break-inside: avoid; }}
.card.fit-high {{ border-left-color: var(--high); }} .card.fit-medium {{ border-left-color: var(--med); }} .card.fit-low {{ border-left-color: var(--low); }}
.head {{ display:flex; align-items:flex-start; gap:6pt; }}
.head > div {{ flex:1; }}
.name {{ font-weight:bold; font-size: 10.5pt; }}
.role {{ color: var(--muted); }}
.pill {{ color:#fff; font-size:7.5pt; padding:1pt 6pt; border-radius:8pt; white-space:nowrap; background: var(--low); }}
.card.fit-high .pill {{ background: var(--high); }} .card.fit-medium .pill {{ background: var(--med); }}
.tag {{ font-size:7.5pt; padding:1pt 6pt; border-radius:8pt; white-space:nowrap; border:1px solid var(--line); color: var(--muted); }}
.tag.q-yes, .tag.q-likely {{ border-color: var(--high); color: var(--high); }}
.tag.q-no {{ border-color: #b33; color: #b33; }}
table.kv {{ border-collapse: collapse; width: 100%; margin-top: 4pt; }}
table.kv th {{ text-align:left; vertical-align:top; color: var(--blue); width: 74pt; padding: 1.5pt 6pt 1.5pt 0; }}
table.kv td {{ padding: 1.5pt 0; word-break: break-word; }}
a {{ color: var(--blue); text-decoration: none; }}
</style></head><body>
<h1>Duke funding and startup support</h1>
<div class="sub">For SimReal (Duke co-founder: Amaris) · built {today} · public information only</div>
<div class="facts"><div class="fact"><b>{len(items)}</b>programs and resources</div>
<div class="fact"><b>{len(top)}</b>high fit, SimReal qualifies, open or upcoming</div>
<div class="fact"><b>{len(contacts)}</b>named contacts</div>
<div class="fact"><b>{n_email}</b>with a published email</div></div>
<ul class="notes">
<li><b>Qualifies</b> means our reading of the published rules for a startup with a current Duke undergraduate as co-founder. Check each program's latest terms before applying.</li>
<li><b>Status</b> is as of {today}. Deadlines change every cycle; "rolling" means applications are taken year-round.</li>
<li><b>Contacts</b> are listed only when the organization or the person published them. Emails were never guessed or taken from data-broker sites.</li>
</ul>
<h2>Start here · {len(top)}</h2>
<table class="sum"><tr><th>Program</th><th>What you get</th><th>Timing</th><th>Apply</th></tr>{start}</table>
{''.join(sections)}
<h2>Contacts · {len(contacts)}</h2>
<table class="sum"><tr><th>Name</th><th>Organization</th><th>Email</th><th>Profile</th></tr>{ctab}</table>
</body></html>"""
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    items = load()
    contacts = write_csvs(items)
    write_pdf(items, contacts)
    print(f"{len(items)} programs, {len(contacts)} contacts -> {OUT_CSV.relative_to(ROOT)}, {OUT_PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
