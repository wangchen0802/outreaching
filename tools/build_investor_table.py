"""Phase 1 of the Sophinos method: merge comparable-company cap tables into one investor table.

Reads intel/investors/captable/*.json (rounds per comparable company: leads, participants,
partners, source), lists/investors.csv and intel/outreach/investor-waves.json (existing investors
and their C/B/A groups), and intel/investors/profiles.json when present (stage, check size,
lead/follow and partner per investor).

Writes intel/investors/captable.json (summary used by the funding playbook), intel/investors/table.json and
collateral/SimReal-投资人总表.xlsx (the 4-question investor table). Needs openpyxl.

Usage: python3 tools/build_investor_table.py
"""
import csv
import json
import pathlib
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAP = ROOT / "intel" / "investors" / "captable"
OUT_JSON = ROOT / "intel" / "investors" / "captable.json"
OUT_XLSX = ROOT / "collateral" / "SimReal-投资人总表.xlsx"
PROFILES = ROOT / "intel" / "investors" / "profiles.json"
STOP = {"ventures", "venture", "capital", "partners", "partner", "vc", "fund", "funds", "the", "group", "management",
        "investments", "investment", "holdings", "llc", "lp", "co", "inc", "资本", "创投", "基金", "投资"}
ALIAS = {"andreessenhorowitz": "a16z", "a16zandreessenhorowitz": "a16z", "andreessenhorowitza16z": "a16z",
         "wingventure": "wing", "wingvc": "wing", "lightspeedventure": "lightspeed", "sequoiacapital": "sequoia",
         "decibelventures": "decibel", "bessemerventure": "bessemer", "ycombinator": "ycombinator", "yc": "ycombinator",
         "redpointventures": "redpoint", "01advisors01a": "01advisors", "nvidianventures": "nventures",
         "gvgoogleventures": "gv", "googleventures": "gv"}
GROUP_LABEL = {1: "C 组", 2: "B 组", 3: "A 组", 9: "暂缓"}
# Investor names that are not venture investors we would pitch for a seed round.
NOT_VC = re.compile(r"Khazanah|BlackRock|sovereign|UC Investments|University of California|Coatue|Valiant|Tiger Global|"
                    r"Fidelity|T\. Rowe|SoftBank Vision|Mubadala|Temasek|GIC\b|Nvidia$|NVIDIA$|Microsoft$|Google$|Amazon$", re.I)
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")


CN_SUFFIX = re.compile(r"(创业投资|投资基金|产业基金|创投|资本|基金|投资|创新|集团)+$")


def norm(name):
    s = re.sub(r"[（(].*?[)）]", " ", name or "").lower()
    if re.fullmatch(r"[\u4e00-\u9fff]+", s.strip()):
        return CN_SUFFIX.sub("", s.strip()) or s.strip()
    words = [w for w in re.split(r"[^a-z0-9一-鿿]+", s) if w and w not in STOP]
    key = "".join(words)
    full = re.sub(r"[^a-z0-9一-鿿]+", "", (name or "").lower())
    return ALIAS.get(full) or ALIAS.get(key) or key


def squash(name):
    """Name with parentheses and every non-alphanumeric character removed ("Box Group" -> "boxgroup")."""
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", re.sub(r"[（(].*?[)）]", " ", name or "").lower())


def short_company(name):
    return re.split(r" \(|（", name)[0].strip()


def stage_of(round_name):
    r = round_name.lower()
    if "pre-seed" in r or "pre seed" in r or "天使" in r or "angel" in r:
        return "pre-seed/天使"
    if "seed" in r or "种子" in r:
        return "种子"
    if "series a" in r or "a 轮" in r or "a轮" in r or "pre-a" in r:
        return "A 轮"
    if re.search(r"series [b-z]|[b-f] ?轮|growth|mezzanine", r):
        return "B 轮及以后"
    return "未标明"


def load_rounds():
    rounds, missing = [], []
    for p in sorted(CAP.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        rounds += d.get("rounds", [])
        missing += d.get("notFound", [])
    return rounds, missing


def main():
    rounds, missing = load_rounds()
    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        existing = list(csv.DictReader(f))
    waves = json.loads((ROOT / "intel" / "outreach" / "investor-waves.json").read_text(encoding="utf-8"))
    profiles = {}
    if PROFILES.exists():
        for pr in json.loads(PROFILES.read_text(encoding="utf-8")):
            profiles[norm(pr["name"])] = pr
            profiles.setdefault(squash(pr["name"]), pr)
    known = {}
    for r in existing:
        for k in (norm(r["名称"]), squash(r["名称"]), norm(r["slug"].replace("-", " ")), squash(r["slug"])):
            if k:
                known.setdefault(k, r)

    inv = {}
    for rd in rounds:
        stage = stage_of(rd["round"])
        named = [(n, True) for n in rd["leads"]] + [(n, False) for n in rd["participants"]]
        for name, lead in named:
            k = norm(name)
            if not k:
                continue
            x = inv.setdefault(k, {"name": name, "companies": [], "leads": 0, "rounds": [], "stages": [], "partners": [], "sources": []})
            if short_company(rd["company"]) not in x["companies"]:
                x["companies"].append(short_company(rd["company"]))
            x["leads"] += 1 if lead else 0
            x["rounds"].append(f'{short_company(rd["company"])} {rd["round"]} {rd["date"]}' + ("（领投）" if lead else ""))
            if stage not in x["stages"]:
                x["stages"].append(stage)
            if rd["source"] and rd["source"] not in x["sources"]:
                x["sources"].append(rd["source"])
        for p in rd.get("partners", []):
            m = re.match(r"(.+?)\s*[（(](.+)[)）]", p)
            if m and norm(m.group(2)) in inv and p not in inv[norm(m.group(2))]["partners"]:
                inv[norm(m.group(2))]["partners"].append(m.group(1).strip())

    companies = sorted({short_company(rd["company"]) for rd in rounds})
    rows = []
    for k, x in inv.items():
        old = known.get(k) or known.get(squash(x["name"]))
        x["existing"] = old["slug"] if old else ""
        x["notVC"] = bool(NOT_VC.search(x["name"]))
        if old:
            x["group"] = waves.get(old["slug"], {}).get("wave", 2)
        elif x["notVC"]:
            x["group"] = 9
        else:
            many = len(x["companies"]) >= 2
            early = any(s in ("pre-seed/天使", "种子", "A 轮") for s in x["stages"])
            x["group"] = 3 if many and x["leads"] and early else 2 if (many or (x["leads"] and early)) else 1
        rows.append(x)

    new = [x for x in rows if not x["existing"] and not x["notVC"]]
    top = sorted([x for x in rows if not x["notVC"]], key=lambda x: (-len(x["companies"]), -x["leads"], x["name"].lower()))[:18]
    summary = {
        "companies": companies,
        "rounds": len(rounds),
        "notFound": [m.split(":")[0].split("（")[0] for m in missing],
        "investors": [{"name": x["name"], "companies": x["companies"], "leads": x["leads"], "stages": x["stages"], "group": x["group"]}
                      for x in sorted(new, key=lambda x: (-len(x["companies"]), x["name"].lower()))],
        "top": [{"name": x["name"], "companies": x["companies"], "leads": x["leads"], "stages": x["stages"]} for x in top],
    }

    # The 4-question table: every existing investor plus every new one from the cap tables.
    by_slug = {x["existing"]: x for x in rows if x["existing"]}
    table = []
    for r in existing:
        x = by_slug.get(r["slug"], {})
        prof = profiles.get(norm(r["名称"])) or profiles.get(squash(r["名称"])) or {}
        w = waves.get(r["slug"], {}).get("wave", 2)
        table.append({
            "group": w, "name": r["名称"], "kind": r["类型"], "region": r["地区"],
            "stage": prof.get("stage") or "、".join(x.get("stages", [])) or "未确认",
            "check": prof.get("check") or "未确认",
            "lead": prof.get("lead") or (f'同类公司中领投 {x["leads"]} 次' if x else "未确认"),
            "similar": "、".join(x.get("companies", [])) or (r["钩子"][:80] if r["钩子"] else ""),
            "contact": r["联系人"] + (f'（{r["职位"]}）' if r["职位"] and r["联系人"] != "未找到" else ""),
            "email": r["邮箱"] if r["邮箱"] not in ("", "未找到") else (r["备用渠道"] or "未找到"),
            "status": "已在审批页", "sources": " ; ".join(x.get("sources", [])[:3]) or r["钩子来源"],
        })
    for x in sorted(new, key=lambda x: (-len(x["companies"]), x["name"].lower())):
        prof = profiles.get(norm(x["name"])) or profiles.get(squash(x["name"])) or {}
        table.append({
            "group": x["group"], "name": x["name"], "kind": prof.get("kind", "未确认"), "region": prof.get("region", "未确认"),
            "stage": prof.get("stage") or "、".join(x["stages"]),
            "check": prof.get("check") or "未确认",
            "lead": prof.get("lead") or f'同类公司中领投 {x["leads"]} 次',
            "similar": "、".join(x["companies"]),
            "contact": (prof.get("contact") if prof.get("contact") not in (None, "", "未找到") else None) or ("、".join(x["partners"]) if x["partners"] else "未找到"),
            "email": (f'{prof["email"]}（{prof.get("emailSource", "")}）' if prof.get("email") not in (None, "", "未找到") else "未找到"),
            "status": "新增（同类公司反查）", "sources": " ; ".join(x["sources"][:3]),
        })
    summary["table"] = len(table)
    summary["byGroup"] = {GROUP_LABEL.get(g, "B 组"): sum(1 for t in table if t["group"] == g) for g in (3, 2, 1, 9)}
    summary["checkKnown"] = sum(1 for t in table if t["check"] not in ("未确认", ""))
    summary["withEmail"] = sum(1 for t in table if t["email"] not in ("未找到", ""))
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    rank = {3: 0, 2: 1, 1: 2, 9: 3}
    table.sort(key=lambda t: (rank.get(t["group"], 1), t["status"] != "已在审批页", t["name"].lower()))
    (OUT_JSON.parent / "table.json").write_text(json.dumps(table, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    wb = Workbook()
    ws = wb.active
    ws.title = "投资人总表"
    cols = [("分组", 8), ("投资人", 24), ("类型", 10), ("地区", 14), ("① 通常投哪轮", 18), ("② 典型支票", 18),
            ("③ 领投还是跟投", 18), ("④ 投过的同类公司", 40), ("对接人", 26), ("邮箱 / 渠道", 34), ("状态", 16), ("来源", 50)]
    ws.append([c for c, _ in cols])
    for t in table:
        ws.append([GROUP_LABEL.get(t["group"], "B 组"), t["name"], t["kind"], t["region"], t["stage"], t["check"], t["lead"],
                   t["similar"], t["contact"], t["email"], t["status"], t["sources"]])
    for cell in ws[1]:
        cell.font, cell.fill, cell.alignment = HEAD_FONT, HEAD_FILL, WRAP
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font, cell.alignment = BODY_FONT, WRAP
    for i, (_, w) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions

    ws2 = wb.create_sheet("同类公司融资记录")
    ws2.append(["公司", "轮次", "时间", "金额", "领投", "跟投", "合伙人 / 董事", "来源"])
    for rd in rounds:
        ws2.append([rd["company"], rd["round"], rd["date"], rd["amount"], "、".join(rd["leads"]), "、".join(rd["participants"]),
                    "、".join(rd.get("partners", [])), rd["source"]])
    for cell in ws2[1]:
        cell.font, cell.fill, cell.alignment = HEAD_FONT, HEAD_FILL, WRAP
    for i, w in enumerate([24, 18, 10, 12, 30, 50, 30, 50], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    for row in ws2.iter_rows(min_row=2):
        for cell in row:
            cell.font, cell.alignment = BODY_FONT, WRAP

    ws3 = wb.create_sheet("说明")
    for n in [
        f"按 Luke Sophinos 的方法：从 {len(companies)} 家同类公司（专家数据、RL 环境、评测、后训练平台、国内数据公司）的 {len(rounds)} 轮公开融资里反查投资人，"
        f"加上已有的 {len(existing)} 家，共 {len(table)} 家。",
        "四个问题：① 通常投哪一轮 ② 典型支票 ③ 领投还是跟投 ④ 投过哪些同类公司。①③ 先按同类公司融资记录推出，有单独调研的以调研为准；未确认表示还没查到。",
        "分组：A 组最匹配（投过两家以上同类公司且在早期领投过），最后发；B 组其次；C 组匹配度最低，先发练手；暂缓是主权基金、成长期机构等不投种子轮的。已有投资人沿用审批页上的分组。",
        "邮箱只用本人或机构公开发布的地址；新增投资人的邮箱还没查，审批页上暂时没有它们的卡片。",
        "来源：公开融资公告和新闻（本环境打不开 Crunchbase），每条附链接。",
    ]:
        ws3.append([n])
    ws3.column_dimensions["A"].width = 120
    for r in ws3.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    OUT_XLSX.parent.mkdir(exist_ok=True)
    wb.save(OUT_XLSX)
    print(f"{len(companies)} companies, {len(rounds)} rounds, {len(inv)} investors ({len(new)} new); table {len(table)} rows")


if __name__ == "__main__":
    main()
