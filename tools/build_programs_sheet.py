"""Build collateral/SimReal-孵化与种子项目.xlsx: every pre-seed / seed program SimReal can apply to.

Covers:
- the top-100 VC firms' own programs (Sequoia Arc, a16z speedrun, Greylock Edge, ...);
- AI-focused programs;
- fintech / crypto programs;
- UK / Europe / Asia programs.

Reads intel/investors/seed-programs.json: {"programs": [...], "noProgram": [...]}, written by the program sweep and
checked by a second researcher (keep=false entries go to their own sheet).

Sheets:
- 全部项目: open / rolling first, then by next deadline and fit;
- 顶级VC的项目;
- 已停办或核实不了;
- 没有孵化项目的VC;
- 说明.

Needs openpyxl.

Usage: python3 tools/build_programs_sheet.py
"""
import csv
import datetime as dt
import json
import pathlib
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_resources_sheet as dates  # noqa: E402  (reuses its deadline parser)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "investors" / "seed-programs.json"
TOP100 = ROOT / "intel" / "investors" / "strebulaev-2026.csv"
OUT = ROOT / "collateral" / "SimReal-孵化与种子项目.xlsx"
TODAY = dt.date(2026, 10, 8)
FIT_RANK = {"A": 0, "B": 1, "C": 2}
CONF = {"high": "高", "medium": "中", "low": "低"}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
COLS = [("序号", 6), ("适合度", 7), ("项目", 30), ("主办方", 22), ("类型", 14), ("状态", 16), ("最近截止", 12), ("时间", 30),
        ("给什么", 44), ("谁能申请", 40), ("形式 / 地点", 24), ("AI 方向", 8), ("为什么适合 / 不适合", 40), ("申请链接", 36),
        ("把握", 6), ("复核说明", 36), ("来源", 50)]


def top100_names():
    """Core names of the top-100 firms ("Sequoia Capital" -> "sequoia capital", "（可能是 Vy Capital）" -> "vy capital")."""
    names = []
    with open(TOP100, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name = re.sub(r"^（(?:可能是\s*)?|）$", "", r["firm"]).split(" (")[0].strip().lower()
            if name and "无法辨认" not in name and "（" not in name:
                names.append(name)
                short = re.sub(r"(\s+(capital|ventures?|partners|management|investment group|venture partners))+$", "", name)
                if short != name and len(short) > 3:
                    names.append(short)
    return names + ["a16z"]


# Programs the sweep returned twice under different names -> one key.
SAME_AS = {"a16zcryptocryptostartupaccelerator": "a16zcryptocsx"}


def program_key(name):
    """"Seedcamp（pre-seed / seed 投资申请）" and "Seedcamp" -> "seedcamp"."""
    key = re.sub(r"[^a-z0-9]+", "", re.sub(r"[（(].*?[)）]", " ", name.lower()))
    return SAME_AS.get(key, key)


def dedupe(programs):
    """One record per program: the best-rated one (confidence, then more sources), with the others' sources added."""
    best = {}
    order = {"high": 0, "medium": 1, "low": 2}
    for p in sorted(programs, key=lambda p: (order.get(p.get("confidence"), 3), -len(p.get("sources") or []))):
        k = program_key(p["program"]) or p["program"]
        if k in best:
            best[k]["sources"] += [u for u in (p.get("sources") or []) if u not in best[k]["sources"]]
            continue
        p["sources"] = list(p.get("sources") or [])
        best[k] = p
    return list(best.values())


def run_by(operator, top):
    """Whether a top-100 firm runs the program; "非 Founders Fund 运营" names the firm without it being the operator."""
    text = re.sub(r"非[^，,；;）)]*", " ", (operator or "").lower())
    return any(t.search(text) for t in top)


def status_rank(status):
    s = status or ""
    for i, word in enumerate(("开放中", "滚动", "即将开放", "未确认", "已截止")):
        if word in s:
            return i
    return 5


def row(i, p):
    return [i, p.get("fit", ""), p["program"], p.get("operator", ""), p.get("type", ""), p.get("status", ""),
            p.get("_deadline", ""), p.get("timing", ""), p.get("offer", ""), p.get("eligibility", ""), p.get("format", ""),
            p.get("aiFocus", ""), p.get("why", ""), p.get("apply", ""), CONF.get(p.get("confidence"), ""),
            p.get("verifyNote", ""), "\n".join((p.get("sources") or [])[:4])]


def sheet(wb, title, cols, rows):
    ws = wb.create_sheet(title)
    ws.append([c for c, _ in cols])
    for cell in ws[1]:
        cell.font, cell.fill, cell.alignment = HEAD_FONT, HEAD_FILL, WRAP
    for r in rows:
        ws.append(r)
    for r in ws.iter_rows(min_row=2):
        for cell in r:
            cell.font, cell.alignment = BODY_FONT, WRAP
    for i, (_, width) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    dates.TODAY = TODAY
    programs = data["programs"]
    for p in programs:
        # "deadline" (when set, even empty) overrides the date parsed from "timing", which can pick up a start date.
        p["_deadline"] = "" if "已截止" in (p.get("status") or "") or "停办" in (p.get("status") or "") \
            else p["deadline"] if "deadline" in p else dates.next_deadline(p.get("timing", ""))
    kept = dedupe([p for p in programs if p.get("keep", True)])
    live = [p for p in kept if "停办" not in (p.get("status") or "")]
    # Dropped as a duplicate of another entry: not a closed program, so left out of the "已停办" sheet.
    gone = [p for p in programs if not p.get("keep", True) and "重复" not in (p.get("verifyNote") or "")] + \
        [p for p in kept if p not in live]
    live.sort(key=lambda p: (status_rank(p.get("status")), p["_deadline"] or "9999", FIT_RANK.get(p.get("fit"), 3),
                             p["program"].lower()))
    top = [re.compile(r"\b" + re.escape(n) + r"\b") for n in top100_names()]
    from_top = [p for p in live if run_by(p.get("operator"), top)]

    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "全部项目", COLS, [row(i, p) for i, p in enumerate(live, 1)])
    sheet(wb, "顶级VC的项目", COLS, [row(i, p) for i, p in enumerate(from_top, 1)])
    sheet(wb, "已停办或核实不了", [("项目", 30), ("主办方", 22), ("原因", 70), ("来源", 50)],
          [[p["program"], p.get("operator", ""), p.get("verifyNote") or p.get("status", ""), "\n".join((p.get("sources") or [])[:3])]
           for p in gone])
    sheet(wb, "没有孵化项目的VC", [("机构和说明", 100)], [[n] for n in sorted(set(data.get("noProgram", [])))])

    soon = [p for p in live if p["_deadline"] and p["_deadline"] <= (TODAY + dt.timedelta(days=45)).isoformat()]
    ws = wb.create_sheet("说明")
    notes = [
        f"共 {len(live)} 个种子及以前阶段能申请的项目（A 档 {sum(1 for p in live if p.get('fit') == 'A')} 个），"
        f"其中顶级 VC（2026 Strebulaev-Jackson 前 100）自己办的 {len(from_top)} 个；45 天内截止的 {len(soon)} 个。",
        "类型：加速器、驻场（Residency）、孵化器 / Venture studio、VC 种子项目（如 Sequoia Arc、a16z speedrun）、Fellowship、"
        "Scout / 种子基金、大厂创业项目（算力额度、投资）。",
        "排序：开放中和滚动申请的在前，然后按最近截止日期和适合度。'最近截止'从'时间'列里自动取最近一个未来日期。",
        "每个项目都附来源，并由第二个调研员复核过是否还在办、截止时间、条款和申请条件；停办或核实不了的单独列出。",
        "注意'谁能申请'里对公司注册地和所在地的要求：部分项目要求美国或英国公司、要求线下驻场。",
        f"日期以 {TODAY.isoformat()} 为准。信息来自搜索摘要（本环境打不开网站），申请前点开申请链接再确认一次。",
    ]
    for line in notes:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    for r in ws.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(live)} programs ({len(from_top)} from top-100 VCs, {len(soon)} closing "
          f"within 45 days), {len(gone)} dropped")


if __name__ == "__main__":
    main()
