"""Render lists/duke-alumni-investors.csv as a printable page and PDF.

Output: collateral/src/duke-alumni-investors.html and collateral/SimReal-Duke-alumni-investors.pdf
(rendered with the pre-installed headless Chromium).

Usage: python3 tools/build_duke_pdf.py [--draft "note shown under the title"]
"""
import argparse
import csv
import datetime
import html
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "lists" / "duke-alumni-investors.csv"
EXCL = ROOT / "lists" / "duke-alumni-investors.md"
OUT_HTML = ROOT / "collateral" / "src" / "duke-alumni-investors.html"
OUT_PDF = ROOT / "collateral" / "SimReal-Duke-alumni-investors.pdf"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
NOT_FOUND = {"", "not found", "none", "n/a", "none found"}


def e(s):
    return html.escape(str(s or ""))


def short(s):
    """Drop trailing parenthetical or ';' notes: 'Paradigm (also CEO of Nudge)' -> 'Paradigm'."""
    s = str(s or "").strip()
    cut = re.split(r"\s*[(;]", s, maxsplit=1)[0].strip(" ,")
    return cut or s


def link(s):
    out = e(s).replace(" (search snippet)", "").replace(" (read)", "")
    return re.sub(r"(https?://[^\s<>\"')，;]+)",
                  lambda m: f'<a href="{m.group(1)}">{m.group(1).split("://", 1)[1].rstrip("/")[:70]}</a>', out)


def duke_line(r):
    d = short(r["duke"] or r["duke_degree"])
    y = str(r["duke_grad_year"] or "")
    if y and y not in d and f"'{y[2:]}" not in d:
        d += f" · {y}"
    return d


def excluded_rows():
    rows, on = [], False
    for line in EXCL.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Checked and left out"):
            on = True
            continue
        if on and line.startswith("| ") and not line.startswith("| Name") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                rows.append(cells[:3])
    return rows


def card(r):
    parts = [f'<div class="card fit-{e(r["fit"]).lower()}">',
             f'<div class="head"><span class="rank">{e(r["rank"])}</span>'
             f'<div><div class="name">{e(r["name"])}</div>'
             f'<div class="role">{e(short(r["title"]))} · <b>{e(short(r["firm"]))}</b></div></div>'
             f'<span class="pill">{e(r["fit"])} fit</span></div>',
             f'<div class="meta">Duke: {e(duke_line(r))} &nbsp;|&nbsp; Confidence: {e(r["confidence"])}'
             + (f' &nbsp;|&nbsp; {e(r["location"])}' if r["location"] and "not" not in r["location"].lower() else "")
             + '</div>',
             f'<p class="bio">{e(r["bio"])}</p>',
             '<table class="kv">']
    rows = [("Stage", e(r["stage_focus"]))]
    if r["relevant_investments"].strip().lower() not in NOT_FOUND:
        rows.append(("Relevant deals", e(r["relevant_investments"])))
    rows.append(("Why them", e(r["fit_reason"])))
    if r["hook"].strip():
        rows.append(("Hook", f'<i>{e(r["hook"])}</i>'))
    contact = []
    contact.append(f'Email: {e(r["email"])}' + (f' (published at {link(r["email_source"])})' if r["email"] != "not found" else " (not published)"))
    if r["other_contact"].strip().lower() not in NOT_FOUND:
        contact.append(f'Fund route: {link(r["other_contact"])}')
    for label, k in (("LinkedIn", "linkedin"), ("X", "x"), ("Site", "personal_site")):
        if r[k].strip().lower() not in NOT_FOUND:
            contact.append(f'{label}: {link(r[k])}')
    rows.append(("Contact", "<br>".join(contact)))
    if r["already_in_simreal_pipeline"]:
        rows.append(("Note", f'Fund already in SimReal pipeline: {e(r["already_in_simreal_pipeline"])}'))
    parts += [f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows]
    parts += ['</table></div>']
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", default="")
    args = ap.parse_args()
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    excl = excluded_rows()
    n = {f: sum(r["fit"] == f for r in rows) for f in ("High", "Medium", "Low")}
    n_email = sum(r["email"] != "not found" for r in rows)
    today = datetime.date.today().isoformat()

    summary = ["<table class='sum'><tr><th>#</th><th>Name</th><th>Firm</th><th>Title</th><th>Duke</th><th>Fit</th></tr>"]
    for r in rows:
        summary.append(f"<tr><td>{e(r['rank'])}</td><td><b>{e(r['name'])}</b></td><td>{e(short(r['firm']))}</td>"
                       f"<td>{e(short(r['title']))}</td><td>{e(duke_line(r))}</td>"
                       f"<td><span class='dot fit-{e(r['fit']).lower()}'></span>{e(r['fit'])}</td></tr>")
    summary.append("</table>")

    sections = []
    for f in ("High", "Medium", "Low"):
        tier = [r for r in rows if r["fit"] == f]
        if tier:
            sections.append(f"<h2>{f} fit · {len(tier)}</h2>" + "\n".join(card(r) for r in tier))

    manual_html = ""
    manual = ROOT / "intel" / "outreach" / "duke" / "manual-check.json"
    if manual.exists():
        items = json.load(open(manual, encoding="utf-8"))
        manual_html = ("<h2>Worth a manual check · " + str(len(items)) + "</h2><table class='sum ex'><tr><th>Name</th><th>Firm</th><th>Why</th></tr>"
                       + "".join(f"<tr><td><b>{e(m['name'])}</b></td><td>{e(m['firm'])}</td><td>{e(m['why'])} {link(m['route'])}</td></tr>" for m in items)
                       + "</table>")

    ex_html = ""
    if excl:
        ex_html = ("<h2>Checked and left out · " + str(len(excl)) + "</h2><table class='sum ex'><tr><th>Name</th><th>Firm</th><th>Reason</th></tr>"
                   + "".join(f"<tr><td>{e(a)}</td><td>{e(short(b))}</td><td>{e(c)}</td></tr>" for a, b, c in excl) + "</table>")

    draft = f'<div class="draft">{e(args.draft)}</div>' if args.draft else ""
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Duke Alumni Investors</title>
<style>
@page {{ size: Letter; margin: 14mm 13mm; }}
:root {{ --ink:#1b2430; --muted:#5b6675; --line:#dfe3e8; --blue:#00539B; --high:#1a7f4b; --med:#b7791f; --low:#8a94a3; }}
body {{ font-family: "DejaVu Sans", Arial, sans-serif; color: var(--ink); font-size: 9.2pt; line-height: 1.42; background:#fff; margin:0; }}
h1 {{ color: var(--blue); font-size: 20pt; margin: 0 0 2pt; }}
h2 {{ color: var(--blue); font-size: 13pt; border-bottom: 2px solid var(--blue); padding-bottom: 2pt; margin: 16pt 0 8pt; break-after: avoid; }}
.sub {{ color: var(--muted); margin-bottom: 8pt; }}
.draft {{ background:#fff4e0; border:1px solid #f0c27a; padding:6pt 8pt; border-radius:4pt; margin:6pt 0 8pt; }}
.facts {{ display:flex; gap:8pt; margin:8pt 0; }}
.fact {{ flex:1; border:1px solid var(--line); border-radius:5pt; padding:6pt 8pt; }}
.fact b {{ display:block; font-size:15pt; color: var(--blue); }}
ul.notes {{ margin:4pt 0 0 14pt; padding:0; color: var(--ink); }}
table.sum {{ width:100%; border-collapse: collapse; font-size: 8.2pt; }}
table.sum th {{ text-align:left; background:#eef3f9; color: var(--blue); padding:3pt 4pt; }}
table.sum td {{ border-bottom: 1px solid var(--line); padding:2.5pt 4pt; vertical-align: top; }}
table.sum tr {{ break-inside: avoid; }}
.dot {{ display:inline-block; width:7pt; height:7pt; border-radius:50%; margin-right:3pt; vertical-align:middle; }}
.dot.fit-high, .card.fit-high .pill {{ background: var(--high); }}
.dot.fit-medium, .card.fit-medium .pill {{ background: var(--med); }}
.dot.fit-low, .card.fit-low .pill {{ background: var(--low); }}
.card {{ border:1px solid var(--line); border-left: 4px solid var(--blue); border-radius: 5pt; padding: 7pt 9pt; margin: 0 0 8pt; break-inside: avoid; }}
.card.fit-high {{ border-left-color: var(--high); }} .card.fit-medium {{ border-left-color: var(--med); }} .card.fit-low {{ border-left-color: var(--low); }}
.head {{ display:flex; align-items:flex-start; gap:7pt; }}
.head > div {{ flex:1; }}
.rank {{ font-weight:bold; color: var(--muted); min-width: 14pt; }}
.name {{ font-weight:bold; font-size: 11pt; }}
.role {{ color: var(--muted); }}
.pill {{ color:#fff; font-size:7.5pt; padding:1pt 6pt; border-radius:8pt; white-space:nowrap; }}
.meta {{ color: var(--muted); font-size: 8pt; margin: 3pt 0 4pt 21pt; }}
.bio {{ margin: 0 0 4pt 21pt; }}
table.kv {{ margin-left: 21pt; border-collapse: collapse; width: calc(100% - 21pt); }}
table.kv th {{ text-align:left; vertical-align:top; color: var(--blue); font-weight: bold; width: 74pt; padding: 1.5pt 6pt 1.5pt 0; }}
table.kv td {{ padding: 1.5pt 0; word-break: break-word; }}
a {{ color: var(--blue); text-decoration: none; }}
.ex td:nth-child(3) {{ color: var(--muted); }}
</style></head><body>
<h1>Duke alumni investors: angel, seed and early stage</h1>
<div class="sub">SimReal outreach list · built {today} · public professional information only</div>
{draft}
<div class="facts"><div class="fact"><b>{len(rows)}</b>verified investors</div>
<div class="fact"><b>{n['High']}</b>high fit (AI infra, data, dev tools, fintech, quant)</div>
<div class="fact"><b>{n['Medium']} / {n['Low']}</b>medium / low fit</div>
<div class="fact"><b>{n_email}</b>published personal emails</div>
<div class="fact"><b>{len(excl)}</b>checked and left out</div></div>
<ul class="notes">
<li><b>Who qualifies:</b> a Duke degree (Trinity, Pratt, Fuqua, Law, Med or the Graduate School) finished in 2018 or earlier, plus a 2026 decision-making role (GP, managing or founding partner, MD, investing partner, solo GP, or active angel) at an investor that writes angel to Series A checks.</li>
<li><b>How it was checked:</b> each person was found by a web sweep, verified against public sources by one agent, and then challenged by a separate fact-checker. Most evidence comes from search-result snippets, because fund websites block direct access from this environment.</li>
<li><b>Contacts:</b> {n_email} people have a personal email that they or their fund published. Everyone else has the fund's official route (pitch inbox or form), LinkedIn or X. Emails were never guessed from a pattern or taken from data-broker sites. A warm intro through Duke (Duke Capital Partners, Duke I&amp;E, DukeGEN) beats a cold email.</li>
<li><b>Hooks</b> are one-line openers built only from facts with a cited source. Check them before sending.</li>
</ul>
<h2>At a glance</h2>
{''.join(summary)}
{''.join(sections)}
{manual_html}
{ex_html}
</body></html>"""
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{len(rows)} investors -> {OUT_PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
