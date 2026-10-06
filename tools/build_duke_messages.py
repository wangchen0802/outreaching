"""Build the Duke alumni-directory messages (one per investor) for Amaris to paste into the directory's
"contact this alum" form.

Input:  intel/outreach/duke/messages/part*.json  (per person: rank, name, first_name, reasons, other_text,
                                                  why, note_for_sender)
        lists/duke-alumni-investors.csv          (firm, title, fit)
Output: lists/duke-alumni-messages.csv
        collateral/src/duke-alumni-messages.html
        collateral/SimReal-Duke-alumni-messages.pdf

The intro (form box 2) is the same for everyone apart from the greeting; the "why you" text (box 3) is
written per person from verified facts only. Facts about SimReal come from the CEO's investor email.

Usage: python3 tools/build_duke_messages.py
"""
import csv
import datetime
import html
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "outreach" / "duke" / "messages"
INVESTORS = ROOT / "lists" / "duke-alumni-investors.csv"
OUT_CSV = ROOT / "lists" / "duke-alumni-messages.csv"
OUT_HTML = ROOT / "collateral" / "src" / "duke-alumni-messages.html"
OUT_PDF = ROOT / "collateral" / "SimReal-Duke-alumni-messages.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

INTRO = ("Hi {first},\n\n"
         "I'm Amaris, a current Duke undergrad and co-founder and COO of SimReal (simreal.co), a neolab building "
         "data infra, RL environments and recursive self-improvement (RSI) for future AI. I did data science at "
         "Millennium as a summer intern and have a full-time offer. My co-founders are Charles (CEO; LSE Maths, "
         "Citadel, employee #1 at $1.5B+ stablecoin unicorn United Stables) and Henry (CTO; Cambridge Maths, "
         "ex-Jane Street). We're 3 weeks old and at $7M ARR from agent and expert data orders we're already "
         "delivering.")
SIGN_OFF = "\n\nThank you,\nAmaris"
COLS = ["rank", "name", "firm", "title", "fit", "reasons", "other_text", "intro", "why", "note_for_sender"]


def rank_key(r):
    s = str(r)
    return (1, int(s[1:])) if s.startswith("M") else (0, int(s))


def load():
    meta = {r["name"]: r for r in csv.DictReader(open(INVESTORS, encoding="utf-8-sig"))}
    manual = json.load(open(ROOT / "intel" / "outreach" / "duke" / "manual-check.json", encoding="utf-8"))
    manual = {m["name"]: m for m in manual}
    rows = []
    for path in sorted(SRC.glob("part*.json")):
        for m in json.load(open(path, encoding="utf-8")):
            info = meta.get(m["name"]) or {}
            firm = info.get("firm") or (manual.get(m["name"]) or {}).get("firm", "")
            rows.append({
                "rank": m["rank"], "name": m["name"], "firm": firm, "title": info.get("title", ""),
                "fit": info.get("fit") or "Manual check",
                "reasons": " ; ".join(m["reasons"]), "other_text": m.get("other_text", ""),
                "intro": INTRO.format(first=m["first_name"]),
                "why": m["why"].strip() + SIGN_OFF,
                "note_for_sender": m.get("note_for_sender", ""),
            })
    rows.sort(key=lambda r: rank_key(r["rank"]))
    return rows


def e(s):
    return html.escape(str(s or ""))


def para(s):
    return "<br>".join(e(line) for line in str(s).split("\n"))


def write_pdf(rows):
    today = datetime.date.today().isoformat()
    groups = [("High fit", [r for r in rows if r["fit"] == "High"]),
              ("Medium fit", [r for r in rows if r["fit"] == "Medium"]),
              ("Low fit", [r for r in rows if r["fit"] == "Low"]),
              ("Verify first (Duke year not public)", [r for r in rows if r["fit"] == "Manual check"])]
    blocks = []
    for title, rs in groups:
        if not rs:
            continue
        blocks.append(f"<h2>{e(title)} · {len(rs)}</h2>")
        for r in rs:
            reasons = r["reasons"].replace(" ; Other", f" ; Other: “{r['other_text']}”") if "Other" in r["reasons"] else r["reasons"]
            note = f'<div class="note">Note: {e(r["note_for_sender"])}</div>' if r["note_for_sender"] else ""
            blocks.append(f"""<div class="card"><div class="head"><span class="rank">{e(r['rank'])}</span>
<div><div class="name">{e(r['name'])}</div><div class="role">{e(r['title'])} · {e(r['firm'])}</div></div></div>
<div class="lbl">Why are you contacting this alum? (tick)</div><div class="box tick">{e(reasons)}</div>
<div class="lbl">Box 3: Explain why you have chosen to contact them</div><div class="box">{para(r['why'])}</div>{note}</div>""")
    intro_example = para(INTRO.format(first="[first name]"))
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Duke Alumni Messages</title>
<style>
@page {{ size: Letter; margin: 14mm 13mm; }}
:root {{ --ink:#1b2430; --muted:#5b6675; --line:#dfe3e8; --blue:#00539B; }}
body {{ font-family: "DejaVu Sans", Arial, sans-serif; color: var(--ink); font-size: 9.4pt; line-height: 1.45; background:#fff; margin:0; }}
h1 {{ color: var(--blue); font-size: 20pt; margin: 0 0 2pt; }}
h2 {{ color: var(--blue); font-size: 13pt; border-bottom: 2px solid var(--blue); padding-bottom: 2pt; margin: 16pt 0 8pt; break-after: avoid; }}
.sub {{ color: var(--muted); margin-bottom: 8pt; }}
ul.notes {{ margin:4pt 0 8pt 14pt; padding:0; }}
.card {{ border:1px solid var(--line); border-left: 4px solid var(--blue); border-radius:5pt; padding:7pt 9pt; margin:0 0 8pt; break-inside: avoid; }}
.head {{ display:flex; gap:7pt; align-items:flex-start; }}
.rank {{ font-weight:bold; color: var(--muted); min-width:16pt; }}
.name {{ font-weight:bold; font-size: 11pt; }}
.role {{ color: var(--muted); }}
.lbl {{ color: var(--blue); font-weight:bold; font-size: 8pt; margin: 5pt 0 2pt; text-transform: uppercase; letter-spacing: .3pt; }}
.box {{ background:#f6f8fb; border:1px solid var(--line); border-radius:4pt; padding:5pt 7pt; }}
.box.tick {{ background:#fff; }}
.note {{ color:#8a5a00; font-size:8.5pt; margin-top:4pt; }}
.intro {{ background:#f6f8fb; border:1px solid var(--line); border-radius:5pt; padding:8pt 10pt; }}
</style></head><body>
<h1>Duke alumni messages</h1>
<div class="sub">For Amaris to send through the Duke alumni directory · {len(rows)} alumni · built {today}</div>
<ul class="notes">
<li><b>Box 2 (introduce yourself)</b> is the same for everyone apart from the first name. It's shown once below; the CSV has it filled in per person.</li>
<li><b>Box 3 (why them)</b> is written per person from facts verified in the investor list. Check each one before sending.</li>
<li><b>Tone:</b> Duke's terms of use bar unsolicited commercial solicitation on its sites, so each message asks for advice and introductions, with the traction as context. Send in small batches, highest fit first, and follow up only once.</li>
</ul>
<h2>Box 2: Introduce yourself (same for all)</h2>
<div class="intro">{intro_example}</div>
{''.join(blocks)}
</body></html>"""
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    rows = load()
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    write_pdf(rows)
    words = [len(re.findall(r"\S+", r["why"].replace(SIGN_OFF, ""))) for r in rows]
    print(f"{len(rows)} messages -> {OUT_CSV.relative_to(ROOT)}, {OUT_PDF.relative_to(ROOT)}; "
          f"box 3 words {min(words)}-{max(words)}")


if __name__ == "__main__":
    main()
