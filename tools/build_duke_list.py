"""Build the Duke-alumni investor list from the verify workflow outputs.

Input:  intel/outreach/duke/verify-*.json  (each a list of {batch, enriched, review})
        intel/outreach/duke/excluded-early.json  (names dropped before verification, with reasons)
Output: lists/duke-alumni-investors.csv
        lists/duke-alumni-investors.md

The skeptic's corrections are applied over the enriched record; a "reject" verdict
moves the person to the excluded table. Firms already in lists/investors.csv are
flagged so the same fund is not emailed twice.

Usage: python3 tools/build_duke_list.py
"""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "outreach" / "duke"
OUT_CSV = ROOT / "lists" / "duke-alumni-investors.csv"
OUT_MD = ROOT / "lists" / "duke-alumni-investors.md"

COLS = ["rank", "name", "firm", "title", "location", "duke_degree", "duke_grad_year", "grad_year_basis",
        "decision_maker", "stage_focus", "sectors", "fit", "fit_reason", "bio", "relevant_investments",
        "hook", "email", "email_source", "other_contact", "linkedin", "x", "personal_site",
        "already_in_simreal_pipeline", "confidence", "check_verdict", "check_notes", "sources"]

FIT_ORDER = {"High": 0, "Medium": 1, "Low": 2}
CONF_ORDER = {"High": 0, "Medium": 1, "Low": 2}
DM_ORDER = {"yes": 0, "unclear": 1, "no": 2}
NOT_FOUND = {"", "not found", "none", "n/a", "未找到"}


def blank(v):
    return str(v or "").strip().lower() in NOT_FOUND


def key(name):
    return re.sub(r"[^a-z]", "", re.sub(r"\(.*?\)", "", name.lower()))


def pipeline_firms():
    out = []
    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            base = re.sub(r"[（(].*?[）)]", "", r["名称"]).strip().lower()
            if len(base) >= 5 and re.match(r"^[a-z0-9 .&*'-]+$", base):
                out.append((base, r["slug"], r["联系人"]))
    return out


def in_pipeline(firm, firms):
    f = firm.lower()
    hits = [f"{slug} (contact: {who})" for base, slug, who in firms if base in f]
    return "; ".join(hits)


def load():
    people, excluded = {}, []
    for path in sorted(SRC.glob("verify-*.json")):
        for item in json.load(open(path, encoding="utf-8")):
            reviews = {key(r["name"]): r for r in ((item.get("review") or {}).get("reviews") or [])}
            for p in (item.get("enriched") or {}).get("people") or []:
                rv = reviews.get(key(p["name"]))
                rec = dict(p)
                rec["check_verdict"] = rv["verdict"] if rv else "not checked"
                rec["check_notes"] = (rv.get("notes") or "") if rv else ""
                if rv:
                    for c in rv.get("corrections") or []:
                        val = c["value"]
                        if c["field"] == "duke_grad_year":
                            m = re.search(r"\d{4}", val or "")
                            val = int(m.group()) if m else None
                        rec[c["field"]] = val
                        rec["check_notes"] = (rec["check_notes"] + f" | {c['field']}: {c['evidence']}").strip(" |")
                reason = ""
                if not p.get("include"):
                    reason = p.get("exclude_reason") or "failed a criterion"
                elif rv and rv["verdict"] == "reject":
                    reason = "fact-check: " + (rv.get("reject_reason") or rv.get("notes") or "rejected")
                elif rec.get("duke_grad_year") and int(rec["duke_grad_year"]) > 2018:
                    reason = f"Duke degree completed {rec['duke_grad_year']} (after 2018)"
                elif rec.get("decision_maker") == "no" or rec.get("still_active_2026") == "no":
                    reason = "not a current decision maker"
                k = key(p["name"])
                if reason:
                    excluded.append({"name": p["name"], "firm": rec.get("firm", ""), "reason": reason})
                    people.pop(k, None)
                else:
                    people[k] = rec
    early = SRC / "excluded-early.json"
    if early.exists():
        for name, reason in json.load(open(early, encoding="utf-8")).items():
            excluded.append({"name": name, "firm": "", "reason": reason})
    kept = {key(p["name"]) for p in people.values()}
    excluded = [e for e in excluded if key(e["name"]) not in kept]
    seen, uniq = set(), []
    for e in excluded:
        if key(e["name"]) not in seen:
            seen.add(key(e["name"]))
            uniq.append(e)
    return list(people.values()), uniq


def joined(*lists):
    out = []
    for lst in lists:
        for u in lst or []:
            if u and u not in out:
                out.append(u)
    return " ; ".join(out)


def main():
    people, excluded = load()
    firms = pipeline_firms()
    people.sort(key=lambda p: (FIT_ORDER.get(p.get("fit"), 3), DM_ORDER.get(p.get("decision_maker"), 3),
                               CONF_ORDER.get(p.get("confidence"), 3), p["name"]))
    rows = []
    for i, p in enumerate(people, 1):
        rows.append({
            "rank": i, "name": p["name"], "firm": p.get("firm", ""), "title": p.get("title_2026", ""),
            "location": p.get("location", ""), "duke_degree": p.get("duke_degree", ""),
            "duke_grad_year": p.get("duke_grad_year") or "", "grad_year_basis": p.get("grad_year_basis", ""),
            "decision_maker": p.get("decision_maker", ""), "stage_focus": p.get("stage_focus", ""),
            "sectors": p.get("sectors", ""), "fit": p.get("fit", ""), "fit_reason": p.get("fit_reason", ""),
            "bio": p.get("bio", ""), "relevant_investments": p.get("relevant_investments", ""),
            "hook": p.get("hook", ""),
            "email": "not found" if blank(p.get("email")) else p["email"],
            "email_source": "" if blank(p.get("email")) else p.get("email_source", ""),
            "other_contact": p.get("other_contact", ""), "linkedin": p.get("linkedin_url", ""),
            "x": p.get("x_url", ""), "personal_site": p.get("personal_site", ""),
            "already_in_simreal_pipeline": in_pipeline(p.get("firm", ""), firms),
            "confidence": p.get("confidence", ""), "check_verdict": p.get("check_verdict", ""),
            "check_notes": p.get("check_notes", ""),
            "sources": joined(p.get("duke_sources"), p.get("role_sources"), p.get("investment_sources"),
                              p.get("hook_sources")),
        })
    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    write_md(rows, excluded)
    print(f"{len(rows)} investors -> {OUT_CSV.relative_to(ROOT)}; {len(excluded)} excluded")


def contact_lines(r):
    lines = []
    if r["email"] != "not found":
        lines.append(f"Email: {r['email']} (published at {r['email_source']})")
    else:
        lines.append("Email: not published")
    if not blank(r["other_contact"]):
        lines.append(f"Fund route: {r['other_contact']}")
    for label, k in (("LinkedIn", "linkedin"), ("X", "x"), ("Site", "personal_site")):
        if not blank(r[k]):
            lines.append(f"{label}: {r[k]}")
    return lines


def write_md(rows, excluded):
    n_email = sum(r["email"] != "not found" for r in rows)
    out = ["# Duke alumni investors: angel, seed and early stage",
           "",
           "These are Duke alumni (any Duke degree finished in 2018 or earlier) who make investment decisions "
           "at angel, pre-seed, seed or Series A investors, as of October 2026. Each person was found by a "
           "web sweep, checked against public sources, and then reviewed by a separate fact-checker. "
           "Full columns and sources are in `duke-alumni-investors.csv`.",
           "",
           f"- **{len(rows)} investors**: {sum(r['fit'] == 'High' for r in rows)} high fit, "
           f"{sum(r['fit'] == 'Medium' for r in rows)} medium, {sum(r['fit'] == 'Low' for r in rows)} low "
           "(high = backs seed or Series A AI infrastructure, data, dev tools, fintech or quant).",
           f"- **Personal email published**: {n_email}. Everyone else is reached through the fund's official "
           "route, LinkedIn or a warm Duke intro. Emails were never guessed from a pattern or taken from "
           "data-broker sites.",
           "- **Already in the SimReal pipeline** means the fund is in `lists/investors.csv` with a different "
           "contact. Choose one person per fund.",
           ""]
    for tier in ("High", "Medium", "Low"):
        tier_rows = [r for r in rows if r["fit"] == tier]
        if not tier_rows:
            continue
        out += [f"## {tier} fit ({len(tier_rows)})", ""]
        for r in tier_rows:
            year = r["duke_grad_year"] or "not published"
            out.append(f"### {r['rank']}. {r['name']}, {r['title']}, {r['firm']}")
            out.append("")
            out.append(f"*Duke: {r['duke_degree']} · Graduated: {year} · Stage: {r['stage_focus']}"
                       f" · Confidence: {r['confidence']}*")
            out.append("")
            out.append(r["bio"])
            out.append("")
            if not blank(r["relevant_investments"]) and r["relevant_investments"].lower() != "none found":
                out.append(f"- **Relevant deals:** {r['relevant_investments']}")
            out.append(f"- **Why them:** {r['fit_reason']}")
            if r["hook"]:
                out.append(f"- **Hook:** {r['hook']}")
            for line in contact_lines(r):
                out.append(f"- {line}")
            if r["already_in_simreal_pipeline"]:
                out.append(f"- **Already in pipeline:** {r['already_in_simreal_pipeline']}")
            out.append("")
    if excluded:
        out += ["## Checked and left out", "", "| Name | Firm | Reason |", "|---|---|---|"]
        for e in sorted(excluded, key=lambda e: e["name"]):
            out.append(f"| {e['name']} | {e['firm']} | {e['reason'].replace('|', '/')} |")
        out.append("")
    OUT_MD.write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
