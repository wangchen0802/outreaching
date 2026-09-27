"""Turn research rows (intel/outreach/<segment>.csv) into lists and drafts.

- partner rows  -> lists/partners.csv  + drafts/partners/<slug>.md
- investor rows -> lists/investors.csv + drafts/investors/<slug>.md
- customer rows -> prospects.csv (added or updated by company name) + drafts/<slug>.md

Existing drafts are kept unless --force is given (their header, notes and review
history belong to earlier rounds). Rows without a hook are listed but get no draft.

Usage: python3 tools/build_outreach.py [--force] [segment ...]   (default: every segment file)
"""
import argparse
import csv
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import drafts  # noqa: E402
import templates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "outreach"
LIST_COLS = ["slug", "名称", "类型", "地区", "语言", "官网", "联系人", "职位", "联系人来源", "邮箱", "邮箱来源",
             "备用渠道", "备选联系人", "钩子", "钩子来源", "切入点", "风险", "置信度", "分段"]
CUSTOMER_COLS = ["公司", "类别", "地区", "联系人", "职位", "来源链接", "切入点", "置信度", "邮箱", "邮箱来源", "备用渠道"]
SEGMENT_ORDER = ["P1a", "P1b", "P2", "P3", "V1a", "V1b", "V2", "C0", "C1", "C2"]


def clean(v):
    return (v or "").strip()


def head_md(r):
    lines = [f"# {r['名称']}", ""]
    lines.append(f"- 类别：{r['类型']}｜地区：{r['地区']}")
    who = f"**{r['联系人']}**" + (f"，{r['职位']}" if r["职位"] and r["联系人"] != "未找到" else "")
    lines.append(f"- 收件人：{who}")
    lines.append(f"- 置信度：{r['置信度'] or '未标'}")
    if r["联系人来源"]:
        lines.append("- 来源：")
        lines += [f"  - {s.strip()}" for s in r["联系人来源"].split(";") if s.strip()]
    email = r["邮箱"] if r["邮箱"] and r["邮箱"] != "未找到" else "未找到（公开渠道里没有）"
    lines.append(f"- 邮箱：{email}" + (f"（来源：{r['邮箱来源']}）" if r["邮箱来源"] and r["邮箱"] not in ("", "未找到") else ""))
    if r["备用渠道"] and r["备用渠道"] != "未找到":
        lines.append(f"- 备用渠道：{r['备用渠道']}")
    if r["备选联系人"] and r["备选联系人"] != "未找到":
        lines.append(f"- 备选：{r['备选联系人']}")
    lines += ["", "## 调研备注", ""]
    lines += ["**钩子来源**"] + [f"- {s.strip()}" for s in (r["钩子来源"] or "未记录").split(";") if s.strip()]
    lines += ["", "**切入点**", f"- {r['切入点'] or '未写'}", "", "**风险**", f"- {r['风险'] or '无'}"]
    return "\n".join(lines) + "\n"


def name_for(r):
    n = r.get("称呼") or ""
    if n and n != "未找到":
        return n
    # No named contact: the email goes to a generic inbox.
    return f"{r['名称']} team" if r["语言"] == "en" else f"{r['名称']}团队"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("segments", nargs="*")
    args = ap.parse_args()
    segs = args.segments or [s for s in SEGMENT_ORDER if (SRC / f"{s}.csv").exists()]

    t = templates.load()
    lists = {"partner": {}, "investor": {}}
    customers = []
    made, skipped, nohook = 0, 0, []
    for seg in segs:
        with open(SRC / f"{seg}.csv", encoding="utf-8-sig") as f:
            rows = [{k: clean(v) for k, v in r.items() if k} for r in csv.DictReader(f)]
        for r in rows:
            track = r["track"]
            r["分段"] = seg
            if track in lists:
                lists[track].setdefault(r["slug"], r)
            else:
                customers.append(r)
            if not r["钩子"] or r["钩子"] == "未找到":
                nohook.append(f"{seg}/{r['slug']}")
                continue
            path = drafts.TRACK_DIRS[track] / f"{r['slug']}.md"
            if path.exists() and not args.force:
                skipped += 1
                continue
            lang = "en" if r["语言"] == "en" else "zh"
            name = name_for(r)
            parts = templates.render_all(track, lang, r["名称"], name, r["钩子"], t)
            drafts.write(path, head_md(r), track, lang, parts)
            made += 1

    for track, rows in lists.items():
        if not rows:
            continue
        p = ROOT / "lists" / f"{track}s.csv"
        p.parent.mkdir(exist_ok=True)
        existing = {}
        if p.exists():
            with open(p, encoding="utf-8-sig") as f:
                existing = {r["slug"]: r for r in csv.DictReader(f)}
        existing.update(rows)
        with open(p, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=LIST_COLS, extrasaction="ignore")
            w.writeheader()
            for r in existing.values():
                w.writerow(r)

    if customers:
        p = ROOT / "prospects.csv"
        with open(p, encoding="utf-8-sig") as f:
            cur = list(csv.DictReader(f))
        idx = {r["公司"]: r for r in cur}
        for r in customers:
            row = {"公司": r["名称"], "类别": r["类型"], "地区": "海外" if r["地区"].startswith("海外") else "国内",
                   "联系人": r["联系人"], "职位": r["职位"], "来源链接": r["联系人来源"], "切入点": r["切入点"],
                   "置信度": r["置信度"], "邮箱": r["邮箱"], "邮箱来源": r["邮箱来源"], "备用渠道": r["备用渠道"]}
            if r["名称"] in idx:
                # C0 rows only add reachability to existing customers.
                for k in ("邮箱", "邮箱来源", "备用渠道"):
                    idx[r["名称"]][k] = row[k]
            else:
                cur.append(row)
                idx[r["名称"]] = row
        with open(p, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CUSTOMER_COLS, extrasaction="ignore")
            w.writeheader()
            for r in cur:
                w.writerow({k: r.get(k, "") or "" for k in CUSTOMER_COLS})

    print(f"segments {segs}: {made} drafts written, {skipped} kept, {len(nohook)} rows without hook {nohook}")


if __name__ == "__main__":
    main()
