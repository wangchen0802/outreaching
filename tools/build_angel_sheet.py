"""Build collateral/SimReal-天使投资人名单.xlsx (+ .csv of the main sheet) from intel/investors/angels.json.

angels.json holds individual angels found by the angel sweep. Each record has:
- identity: name, role, base;
- evidence: investments, checkSize;
- fit: hooks, whyMoved, influence;
- public channels: x, site, email, warmPath;
- outreach: opener;
- review: tier, keep, confidence, verifyNote, sources.

Sheets:
- 天使名单: records with keep, tier A → C;
- 复核未通过;
- 说明.

Needs openpyxl.

Usage: python3 tools/build_angel_sheet.py
"""
import csv
import json
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "investors" / "angels.json"
OUT = ROOT / "collateral" / "SimReal-天使投资人名单.xlsx"
OUT_CSV = ROOT / "collateral" / "SimReal-天使投资人名单.csv"
TIER_RANK = {"A": 0, "B": 1, "C": 2}
CONF = {"high": "高", "medium": "中", "low": "低"}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
COLS = [("序号", 6), ("档位", 6), ("姓名", 22), ("现任", 30), ("所在地", 16), ("相关点", 22), ("为什么会被这封邮件打动", 48),
        ("影响力", 30), ("天使投资记录", 48), ("单笔金额", 14), ("X", 28), ("个人网站", 26), ("公开邮箱", 26),
        ("可能的引荐路径", 30), ("开场句（英文，放在 Hi 之后）", 60), ("把握", 6), ("复核说明", 40), ("来源", 60)]


def row(i, a):
    return [i, a.get("tier", ""), a["name"], a["role"], a["base"], "、".join(a.get("hooks") or []), a["whyMoved"],
            a["influence"], a["investments"], a.get("checkSize") or "未找到", a.get("x") or "未找到",
            a.get("site") or "", a.get("email") or "未找到", a.get("warmPath") or "未找到", a["opener"],
            CONF.get(a.get("confidence"), ""), a.get("verifyNote", ""), "\n".join((a.get("sources") or [])[:6])]


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
    order = lambda a: (TIER_RANK.get(a.get("tier"), 3), {"high": 0, "medium": 1, "low": 2}.get(a.get("confidence"), 3),  # noqa: E731
                       a["name"].lower())
    kept = sorted([a for a in data if a.get("keep") and not a.get("mainland")], key=order)
    dropped = sorted([a for a in data if not a.get("keep") or a.get("mainland")], key=lambda a: a["name"].lower())
    table = [row(i, a) for i, a in enumerate(kept, 1)]

    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "天使名单", COLS, table)
    sheet(wb, "复核未通过", [("姓名", 24), ("现任", 30), ("原因", 70), ("来源", 60)],
          [[a["name"], a["role"], a.get("verifyNote", ""), "\n".join((a.get("sources") or [])[:3])] for a in dropped])

    tiers = {t: sum(1 for a in kept if a.get("tier") == t) for t in "ABC"}
    with_x = sum(1 for a in kept if a.get("x") and a["x"] != "未找到")
    with_email = sum(1 for a in kept if a.get("email") and a["email"] != "未找到")
    ws = wb.create_sheet("说明")
    notes = [
        f"共 {len(kept)} 位个人天使（不含中国大陆）：A 档 {tiers['A']} 位，B 档 {tiers['B']} 位，C 档 {tiers['C']} 位。复核未通过 {len(dropped)} 位，单独列出。",
        "档位：A = 和邮件高度相关、近一两年仍在投、有公开渠道能联系到；B = 相关度好；C = 有可能。",
        "相关点：这位天使和邮件里哪几点最贴近，可选年轻创始人、RL 环境 / AI 数据、RSI / 前沿研究、量化交易、稳定币 / 加密、数据基础设施、英国 / LSE / 剑桥、YC 圈、华人圈。",
        "每位都有具体的天使投资记录和来源链接，并由第二个调研员逐条复核：投资是不是本人出的钱、人是不是对的、时间是不是近期。",
        f"联系方式只列本人公开的：X {with_x} 位，本人公开邮箱 {with_email} 位。没有按格式猜邮箱，也没有用数据经纪网站。查不到写'未找到'。"
        "大多数天使最好的渠道是 X 私信或熟人引荐（见'可能的引荐路径'）。",
        "开场句：放在邮件 Hi 之后的第一句，引用这位天使公开做过的一件事（投资、文章、演讲），比通用的 Hi 更容易被读下去。",
        "导入 Google 表格：drive.google.com → 新建 → 文件上传 → 右键 → 打开方式 → Google 表格。",
    ]
    for line in notes:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    for r in ws.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([c for c, _ in COLS])
        w.writerows(table)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(kept)} angels (A {tiers['A']}, B {tiers['B']}, C {tiers['C']}), "
          f"{len(dropped)} dropped, {with_x} with X, {with_email} with email")


if __name__ == "__main__":
    main()
