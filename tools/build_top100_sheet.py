"""Build collateral/SimReal-Top100VC-2026.xlsx and an Apollo-ready CSV from intel/investors/strebulaev-2026.csv.

The source is the 2026 Strebulaev-Jackson Venture Ranking image (top 100 US VC firms), transcribed by hand.
Rows whose logo could not be read are marked 待确认 and left out of the Apollo CSV until resolved.

Usage: python3 tools/build_top100_sheet.py
"""
import csv
import json
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "investors" / "strebulaev-2026.csv"
# Stage research per rank: {"rows": [...], "verified": [...]} from the stage sweep; verified rows override.
STAGES = ROOT / "intel" / "investors" / "top100-stages.json"
CONF = {"high": "高", "medium": "中", "low": "低"}
FIT = {"A": "A：积极投种子", "B": "B：偶尔投种子 / 以 A 轮为主", "C": "C：不太可能投种子"}
OUT = ROOT / "collateral" / "SimReal-Top100VC-2026.xlsx"
APOLLO = ROOT / "collateral" / "SimReal-Top100VC-Apollo导入.csv"


def load_stages():
    """Stage facts per rank; a verifier's correction replaces the researcher's stages, seed vehicle and fit."""
    if not STAGES.exists():
        return {}
    data = json.loads(STAGES.read_text(encoding="utf-8"))
    out = {int(r["rank"]): dict(r) for r in data.get("rows", [])}
    for v in data.get("verified", []):
        r = out.setdefault(int(v["rank"]), {})
        if not v.get("ok", True):
            r.update({k: v[k] for k in ("stages", "seedVehicle", "seedFit") if v.get(k)})
            r["note"] = (v.get("note") or "") + "（复核后更正）"
            r["sources"] = list(dict.fromkeys((v.get("sources") or []) + (r.get("sources") or [])))
        else:
            r["note"] = (r.get("note") or "") + "（已复核）"
    return out


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    stages = load_stages()
    wb = Workbook()
    ws = wb.active
    ws.title = "Top 100"
    cols = [("排名", 6), ("机构", 34), ("分数", 8), ("代表投资", 22), ("投资阶段", 30), ("主力阶段", 18),
            ("适合我们的种子轮", 22), ("种子项目 / 渠道", 26), ("首笔金额", 18), ("领投", 12), ("方向", 30), ("备注", 40),
            ("阶段信息把握", 8), ("阶段来源", 44), ("辨认把握", 26), ("官网域名", 20)]
    ws.append([c for c, _ in cols])
    for cell in ws[1]:
        cell.font = Font(name="Arial", bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="111110")
    for r in rows:
        g = stages.get(int(r["rank"]), {})
        ws.append([int(r["rank"]), r["firm"], int(r["score"]), r["top_deal"], g.get("stages", ""), g.get("core", ""),
                   FIT.get(g.get("seedFit"), ""), g.get("seedVehicle", ""), g.get("check", ""), g.get("leads", ""),
                   g.get("sectors", ""), g.get("note", ""), CONF.get(g.get("confidence"), ""),
                   "\n".join((g.get("sources") or [])[:3]), r["certainty"], r["domain"]])
    for i, (_, w) in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for r in ws.iter_rows(min_row=2):
        for cell in r:
            cell.font, cell.alignment = Font(name="Arial", size=10), Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    notes = wb.create_sheet("说明")
    for line in [
        "来源：2026 Strebulaev-Jackson Venture Ranking（美国前 100 家 VC），按截图逐行转录；分数和代表投资照抄图中数字。",
        "辨认把握：清楚 = logo 文字可读；较清楚 = logo 可辨但有点糊；已核实 = 看不清的 logo 已用公开的排名转载（f4.fund、The VC Corner、Rothschild）对上；"
        "较可能 = 证据吻合但没找到排名原文；待确认 = 还没查到，括号里是最可能的候选。",
        "官网域名只填了有把握的，供 Apollo 匹配公司用；空着的直接按名称搜。",
        "投资阶段：每家投哪些轮次、主力阶段、有没有专门的种子项目（如 Sequoia Arc、a16z speedrun、Greylock Edge）、首笔金额和是否领投，附来源；"
        "'适合我们的种子轮'按对 3 周大的 AI 公司种子轮的可能性分 A / B / C。A 档和把握低的条目由第二个调研员复核过。",
        "SimReal-Top100VC-Apollo导入.csv 收了除'待确认'以外的机构（Company Name, Website 两列），可以在 Apollo 里用 CSV 导入批量查公司；'待确认'的几家可以按括号里的候选名单独搜。",
    ]:
        notes.append([line])
    notes.column_dimensions["A"].width = 110
    wb.save(OUT)
    with open(APOLLO, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Company Name", "Website"])
        for r in rows:
            if not r["certainty"].startswith("待确认"):
                w.writerow([r["firm"].split(" (")[0], r["domain"]])
    print(f"wrote {OUT.relative_to(ROOT)} and {APOLLO.relative_to(ROOT)}: "
          f"{sum(1 for r in rows if not r['certainty'].startswith('待确认'))} firms ready for Apollo")


if __name__ == "__main__":
    main()
