"""Fold the overseas-VC re-research (verified JSON records) into the investor segments.

Each input file is a JSON array of records with the fields the research workflow
returns (slug, name, contact, email, emailType, hook, priority, keep, verdict*...).

- Records whose slug is already in V1a/V1b/V2 update that row in place.
- New records go to intel/outreach/V3.csv.
- Every record is also saved to intel/outreach/vc-overseas-refresh.json (the research record
  the overseas-VC spreadsheet is built from).

Personal addresses go to 邮箱; official fund inboxes go first in 备用渠道, where the
approval page picks them up as the generic address.

Usage: python3 tools/vc_refresh.py DIR [DIR ...]
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "outreach"
COLS = ["track", "slug", "名称", "类型", "地区", "语言", "官网", "联系人", "职位", "联系人来源", "称呼", "邮箱", "邮箱来源",
        "备用渠道", "备选联系人", "钩子", "钩子来源", "切入点", "风险", "置信度"]
OLD = ["V1a", "V1b", "V2"]
CONFIDENCE = {"A": "高", "B": "中", "C": "低"}
NONE = ("", "未找到", "无")


def blank(v):
    return (v or "").strip() in NONE


def first_name(contact):
    if blank(contact):
        return ""
    person = re.split(r"\s*[;；&、,]\s*|\s+and\s+", contact.strip())[0]
    person = re.sub(r"[（(].*?[)）]", "", person).strip()
    return person.split()[0] if person else ""


def load(dirs):
    recs = {}
    for d in dirs:
        for p in sorted(pathlib.Path(d).glob("*.json")):
            for r in json.loads(p.read_text(encoding="utf-8")):
                recs[r["slug"]] = r
    return recs


def channel(r):
    parts = []
    if r["emailType"] in ("官方投递", "官方通用") and not blank(r["email"]):
        parts.append(f"{r['email']}（{r['emailType']}，来源 {r['emailSource']}）")
    if not blank(r.get("altChannel")):
        parts.append(r["altChannel"])
    return " ；".join(parts) or "未找到"


def to_row(r, old=None):
    row = dict(old or {})
    personal = r["emailType"] == "个人公开" and not blank(r["email"])
    row.update({
        "track": "investor",
        "slug": r["slug"],
        "名称": r["name"],
        "类型": r["type"],
        "地区": r["region"],
        "语言": "en",
        "官网": r.get("website") or row.get("官网", ""),
        "联系人": r["contact"] if not blank(r["contact"]) else "未找到",
        "职位": r["role"] if not blank(r["contact"]) else "",
        "联系人来源": r["contactSource"],
        "称呼": first_name(r["contact"]),
        "邮箱": r["email"] if personal else "未找到",
        "邮箱来源": f"{r['emailSource']} ｜ 原文：{r['emailEvidence']}" if personal else "",
        "备用渠道": channel(r),
        "钩子": r["hook"],
        "钩子来源": f"{r['hookSource']}（{r['hookDate']}）",
        "切入点": r["thesisFit"] + (f"；阶段：{r['stage']}" if not blank(r.get("stage")) else ""),
        "风险": "；".join(x for x in [f"冲突：{r['conflicts']}" if not blank(r["conflicts"]) else "", r.get("notes", "")] if x) or "无",
        "置信度": CONFIDENCE[r["priority"]],
    })
    row.setdefault("备选联系人", "")
    return row


def main():
    recs = load(sys.argv[1:])
    if not recs:
        raise SystemExit("no records")
    seen = set()
    for seg in OLD:
        path = SRC / f"{seg}.csv"
        with open(path, encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        out = []
        for row in rows:
            r = recs.get(row["slug"])
            if r is not None:
                seen.add(row["slug"])
                out.append(to_row(r, row))
            else:
                out.append(row)
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
            w.writeheader()
            w.writerows(out)
    new = [to_row(r) for slug, r in recs.items() if slug not in seen and r["keep"]]
    with open(SRC / "V3.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(new)
    (SRC / "vc-overseas-refresh.json").write_text(
        json.dumps(sorted(recs.values(), key=lambda r: r["slug"]), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(seen)} existing rows updated, {len(new)} new rows in V3, {len(recs)} records saved")


if __name__ == "__main__":
    main()
