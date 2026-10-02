"""Build collateral/SimReal-资源与渠道清单.xlsx from intel/resources/resources.json.

resources.json holds the verified resource records (name, category, region, offer, eligibility,
timing, status, howToApply, fit, fitWhy, effort, community, sources, verdict, verifyNote) and
the community tactics. Records marked 撤下 are left out.

Sheets: 先办这些 (open or rolling, fit 高), 全部资源, 社区经验, 说明. Needs openpyxl.

Usage: python3 tools/build_resources_sheet.py
"""
import datetime as dt
import json
import pathlib
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "resources" / "resources.json"
OUT = ROOT / "collateral" / "SimReal-资源与渠道清单.xlsx"
TODAY = dt.date(2026, 10, 2)
STATUS_RANK = {"开放中": 0, "滚动申请": 1, "即将开放": 2, "未确认": 3, "已截止": 4}
FIT_RANK = {"高": 0, "中": 1, "低": 2}
EFFORT_RANK = {"低": 0, "中": 1, "高": 2}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")


FULL_DATE = re.compile(r"(20\d\d)[-/.年](\d{1,2})[-/.月](\d{1,2})")
SHORT_DATE = re.compile(r"(?<![\d年/-])(\d{1,2})/(\d{1,2})(?![\d/])")
RANGE_GAP = re.compile(r"^\s*日?\s*[–—\-~～至到]\s*$")


def next_deadline(text):
    """Nearest date on or after today in a timing string, as YYYY-MM-DD, else ''.
    For a range ("10/12–11/1", "2026-10-12 至 2026-11-01") only the end counts."""
    text = text or ""
    found = []  # (start, end, (y, m, d))
    for mt in FULL_DATE.finditer(text):
        found.append((mt.start(), mt.end(), tuple(int(x) for x in mt.groups())))
    for mt in SHORT_DATE.finditer(text):
        m, d = int(mt.group(1)), int(mt.group(2))
        y = TODAY.year if (m, d) >= (TODAY.month, TODAY.day) else TODAY.year + 1
        found.append((mt.start(), mt.end(), (y, m, d)))
    found.sort()
    ends = [f for i, f in enumerate(found)
            if not (i + 1 < len(found) and RANGE_GAP.match(text[f[1]:found[i + 1][0]]))]
    dates = []
    for _, _, (y, m, d) in ends:
        try:
            day = dt.date(y, m, d)
        except ValueError:
            continue
        if day >= TODAY:
            dates.append(day)
    return min(dates).isoformat() if dates else ""


def sheet(wb, title, cols, rows, freeze="C2"):
    ws = wb.create_sheet(title)
    ws.append([c for c, _ in cols])
    for cell in ws[1]:
        cell.font, cell.fill, cell.alignment = HEAD_FONT, HEAD_FILL, WRAP
    for row in rows:
        ws.append(row)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font, cell.alignment = BODY_FONT, WRAP
    for i, (_, width) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.freeze_panes = freeze
    ws.auto_filter.ref = ws.dimensions


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    items = [r for r in data["items"] if r.get("verdict") != "撤下"]
    for r in items:
        r["_deadline"] = "" if r["status"] == "已截止" else next_deadline(r["timing"])
    order = lambda r: (STATUS_RANK.get(r["status"], 3), r["_deadline"] or "9999",  # noqa: E731
                       FIT_RANK[r["fit"]], EFFORT_RANK[r["effort"]], r["name"].lower())

    cols = [("序号", 6), ("名称", 26), ("类别", 14), ("地区", 14), ("状态", 10), ("最近截止", 12), ("时间", 30),
            ("给什么", 40), ("谁能申请", 40), ("为什么适合我们", 40), ("申请成本", 8), ("怎么申请", 40),
            ("创业者评价（Reddit / HN / X）", 50), ("来源", 50), ("核实", 22)]

    def row(i, r):
        check = r.get("verdict", "未复核") + (f"：{r['verifyNote']}" if r.get("verifyNote") else "")
        return [i, r["name"], r["category"], r["region"], r["status"], r["_deadline"], r["timing"], r["offer"],
                r["eligibility"], r["fitWhy"], r["effort"], r["howToApply"], r["community"],
                "\n".join(r["sources"]), check]

    wb = Workbook()
    wb.remove(wb.active)
    now = sorted([r for r in items if r["fit"] == "高" and r["status"] in ("开放中", "滚动申请", "即将开放")], key=order)
    sheet(wb, "先办这些", cols, [row(i, r) for i, r in enumerate(now, 1)])
    everything = sorted(items, key=lambda r: (r["category"],) + order(r))
    sheet(wb, "全部资源", cols, [row(i, r) for i, r in enumerate(everything, 1)])
    tactics = data.get("tactics", [])
    sheet(wb, "社区经验", [("序号", 6), ("类别", 16), ("做法", 34), ("具体说明", 80), ("来源", 50)],
          [[i, t.get("category", ""), t["tactic"], t["detail"], t["source"]] for i, t in enumerate(tactics, 1)])

    ws = wb.create_sheet("说明")
    by_cat = {}
    for r in items:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    notes = [
        f"共 {len(items)} 项资源和渠道，{len(tactics)} 条创业者经验；'先办这些'是匹配度高、现在能申请的 {len(now)} 项，按截止时间排。",
        "分类：" + "，".join(f"{k} {v}" for k, v in sorted(by_cat.items(), key=lambda kv: -kv[1])) + "。",
        "来源：Reddit、Hacker News、X 上的讨论，以及官方页面。本环境打不开这些网站，信息来自搜索结果摘要，申请前请点开官方链接再确认一次。",
        "核实：每项由第二个调研员复核过截止时间、金额和申请条件；'未复核'表示复核时搜索额度用完，只看了来源是否官方。",
        f"日期以 {TODAY.isoformat()} 为准；'最近截止'是从'时间'列里自动取的最近一个未来日期。",
        "公司主体在哪个国家会影响很多项目的资格（英国 SEIS/EIS、Innovate UK；美国 SBIR；国内算力券和补贴），'谁能申请'列写了限制。",
    ]
    for n in notes:
        ws.append([n])
    ws.column_dimensions["A"].width = 120
    for r in ws.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(items)} items, {len(now)} to do now, {len(tactics)} tactics")


if __name__ == "__main__":
    main()
