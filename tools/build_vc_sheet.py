"""Build collateral/SimReal-海外VC名单.xlsx from intel/outreach/vc-overseas-refresh.json and the drafts.

Sheets: 可直接发邮件 (a published address), 无公开邮箱 (form / profile / intro), 暂不联系, 说明.
Needs openpyxl.

Usage: python3 tools/build_vc_sheet.py
"""
import json
import pathlib
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import drafts  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "collateral" / "SimReal-海外VC名单.xlsx"
NONE = ("", "未找到", "无")
TYPE_RANK = {"个人公开": 0, "官方投递": 1, "官方通用": 2, "未找到": 3}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")


def blank(v):
    return (v or "").strip() in NONE


def how_to(r):
    who = r["contact"] if not blank(r["contact"]) else ""
    if r["emailType"] == "个人公开":
        return f"直接写给 {who}" if who else "直接发"
    if who:
        return f"第一句写明请转交 {who}（Could you forward this to {who}?）"
    return "写给团队（Hi team）"


def email_of(slug):
    p = drafts.TRACK_DIRS["investor"] / f"{slug}.md"
    if not p.exists():
        return "", ""
    email = drafts.parse(p)["parts"].get("email", "")
    subject_line, _, body = email.partition("\n")
    return subject_line.split(":", 1)[-1].strip(), body.strip()


def sheet(wb, title, cols, rows):
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
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions
    return ws


def main():
    recs = json.loads((ROOT / "intel" / "outreach" / "vc-overseas-refresh.json").read_text(encoding="utf-8"))
    keep = [r for r in recs if r["keep"]]
    order = lambda r: (r["priority"], TYPE_RANK[r["emailType"]], r["name"].lower())  # noqa: E731
    with_email = sorted([r for r in keep if not blank(r["email"])], key=order)
    no_email = sorted([r for r in keep if blank(r["email"])], key=order)
    dropped = sorted([r for r in recs if not r["keep"]], key=lambda r: r["name"].lower())

    wb = Workbook()
    wb.remove(wb.active)
    cols = [("序号", 6), ("优先级", 7), ("机构", 22), ("类型", 8), ("地区", 14), ("联系人", 18), ("职位", 26),
            ("邮箱", 30), ("邮箱类型", 10), ("写法", 30), ("开场句（英文，已写进正文）", 60), ("为什么找他们", 40),
            ("冲突 / 注意", 36), ("投资阶段", 18), ("邮箱来源", 50), ("联系人来源", 40), ("审批页卡片", 22),
            ("邮件主题", 40), ("邮件正文", 90)]
    rows = []
    for i, r in enumerate(with_email, 1):
        subject, body = email_of(r["slug"])
        rows.append([i, r["priority"], r["name"], r["type"], r["region"], r["contact"], r["role"], r["email"],
                     r["emailType"], how_to(r), r["hook"], r["thesisFit"], r["conflicts"], r["stage"],
                     f"{r['emailSource']} ｜ 原文：{r['emailEvidence']}", r["contactSource"], "v-" + r["slug"],
                     subject, body])
    sheet(wb, "可直接发邮件", cols, rows)

    cols = [("序号", 6), ("优先级", 7), ("机构", 22), ("类型", 8), ("地区", 14), ("联系人", 18), ("职位", 26),
            ("备用渠道（表单 / 公开主页）", 60), ("开场句（英文）", 60), ("为什么找他们", 40), ("冲突 / 注意", 36),
            ("联系人来源", 40), ("审批页卡片", 22)]
    rows = [[i, r["priority"], r["name"], r["type"], r["region"], r["contact"], r["role"], r["altChannel"],
             r["hook"], r["thesisFit"], r["conflicts"], r["contactSource"], "v-" + r["slug"]]
            for i, r in enumerate(no_email, 1)]
    sheet(wb, "无公开邮箱", cols, rows)

    cols = [("机构", 26), ("联系人", 20), ("原因", 80)]
    sheet(wb, "暂不联系", cols, [[r["name"], r["contact"], r["dropReason"]] for r in dropped])

    ws = wb.create_sheet("说明")
    notes = [
        f"共 {len(recs)} 家海外投资人：可直接发邮件 {len(with_email)} 家，无公开邮箱 {len(no_email)} 家，暂不联系 {len(dropped)} 家。",
        "优先级：A = 2025–2026 投过 RL 环境 / 专家数据 / 评测 / 后训练公司（或公开写过这个方向），投种子，且有可用邮箱；B = 方向对但没邮箱，或有邮箱但匹配弱一些；C = 弱相关，或大机构只能靠引荐。",
        "邮箱类型：个人公开 = 本人或所在基金公开发布的本人地址；官方投递 = 基金公开的 BP 投递邮箱（pitch@、deals@ 等）；官方通用 = info@、hello@ 等。",
        "所有邮箱都由第二个调研员逐条复核：搜到本人或基金公开发布的原文才保留。没有按格式猜，没有用 RocketReach、ContactOut 等数据经纪网站。",
        "发到官方邮箱时，第一句写明请转交哪位合伙人（见'写法'列）。",
        "发件邮箱 business@simreal.co。正文按模板 ops/templates.md 生成，开场句是针对这家机构的一句话；跟进：第 5 天、第 12 天（模板同一处）。",
        "审批页（https://claude.ai/artifact/WCBiAySyzEqAHkJ2YkbUj2）的'投资人'标签里有同样的卡片，可以一键打开 Gmail 草稿并记录发送和跟进。",
        "来源后面标'(搜索摘要)'的，是在搜索结果里看到的原文；本环境打不开基金官网，发之前可以点开来源再看一眼。",
    ]
    for n in notes:
        ws.append([n])
    ws.column_dimensions["A"].width = 120
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(with_email)} with email, {len(no_email)} without, {len(dropped)} dropped")


if __name__ == "__main__":
    main()
