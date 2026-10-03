"""Build collateral/SimReal-天使投资人名单.xlsx (+ .csv of the main sheet) from intel/investors/angels.json,
plus the Silicon Valley VC sheet (intel/investors/sv-vcs.json) and the Cambridge / LSE / Duke alumni
investor sheet (intel/investors/alumni.json) when those files exist.

angels.json holds individual angels found by the angel sweep. Each record has:
- identity: name, role, base;
- evidence: investments, checkSize;
- fit: hooks, whyMoved, influence;
- public channels: x, site, email, warmPath;
- outreach: opener;
- review: tier, keep, confidence, verifyNote, sources.

Sheets:
- 天使名单: records with keep, tier A → C;
- 硅谷 VC: Bay Area firms with keep, fit A → C, marked when already in the investor master sheet;
- 剑桥·LSE·Duke 校友: alumni investors with keep;
- 复核未通过: angels, firms and alumni that failed the check;
- 说明.

Needs openpyxl.

Usage: python3 tools/build_angel_sheet.py
"""
import csv
import json
import pathlib
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "investors" / "angels.json"
SV = ROOT / "intel" / "investors" / "sv-vcs.json"
ALUMNI = ROOT / "intel" / "investors" / "alumni.json"
MASTER = ROOT / "collateral" / "SimReal-非大陆投资人总表.csv"
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


SV_COLS = [("序号", 6), ("匹配度", 7), ("机构", 26), ("城市", 14), ("类型", 12), ("阶段", 18), ("单笔金额", 16),
           ("投过的 AI 公司", 46), ("负责 AI / 种子的合伙人", 30), ("合伙人 X", 26), ("官网", 26), ("官方投递渠道", 34),
           ("为什么适合", 40), ("已在总表", 8), ("把握", 6), ("复核说明", 36), ("来源", 50)]
AL_COLS = [("序号", 6), ("学校", 10), ("匹配度", 7), ("姓名", 22), ("在校经历", 26), ("现任", 30), ("所在地", 16),
           ("投资记录", 44), ("和 AI 的关系", 34), ("X", 26), ("个人网站", 24), ("公开邮箱", 24), ("校友引荐路径", 30),
           ("开场句（英文）", 56), ("把握", 6), ("复核说明", 36), ("来源", 50)]


def master_names():
    """Squashed names of the investors already in the master sheet, to mark overlaps."""
    if not MASTER.exists():
        return set()
    with open(MASTER, encoding="utf-8-sig") as f:
        return {squash(r["机构 / 投资人"]) for r in csv.DictReader(f)}


def squash(name):
    name = re.sub(r"[（(].*?[)）]", " ", name or "").lower()
    name = re.sub(r"\b(ventures?|capital|partners|vc|fund|management|the)\b", "", name)
    return re.sub(r"[^a-z0-9]+", "", name)


def sv_row(i, f, known):
    return [i, f.get("fit", ""), f["name"], f["city"], f["type"], f["stage"], f.get("checkSize") or "未找到", f["aiDeals"],
            f.get("partner") or "未找到", f.get("partnerX") or "未找到", f.get("website") or "", f.get("pitchChannel") or "未找到",
            f["whyFit"], "是" if squash(f["name"]) in known else "", CONF.get(f.get("confidence"), ""), f.get("verifyNote", ""),
            "\n".join((f.get("sources") or [])[:5])]


def al_row(i, p):
    return [i, p["school"], p.get("fit", ""), p["name"], p["schoolDetail"], p["role"], p["base"], p["investing"],
            p["aiRelevance"], p.get("x") or "未找到", p.get("site") or "", p.get("email") or "未找到", p.get("warmPath") or "未找到",
            p["opener"], CONF.get(p.get("confidence"), ""), p.get("verifyNote", ""), "\n".join((p.get("sources") or [])[:5])]


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
    failed = [[a["name"], "天使", a["role"], a.get("verifyNote", ""), "\n".join((a.get("sources") or [])[:3])] for a in dropped]

    firms = json.loads(SV.read_text(encoding="utf-8")) if SV.exists() else []
    known = master_names()
    sv_kept = sorted([f for f in firms if f.get("keep", True) and f.get("active", True)],
                     key=lambda f: (TIER_RANK.get(f.get("fit"), 3), f["name"].lower()))
    if firms:
        sheet(wb, "硅谷 VC", SV_COLS, [sv_row(i, f, known) for i, f in enumerate(sv_kept, 1)])
        failed += [[f["name"], "硅谷 VC", f.get("city", ""), f.get("verifyNote") or "已停止投资", "\n".join((f.get("sources") or [])[:3])]
                   for f in firms if f not in sv_kept]

    people = json.loads(ALUMNI.read_text(encoding="utf-8")) if ALUMNI.exists() else []
    al_kept = sorted([p for p in people if p.get("keep", True) and not p.get("mainland")],
                     key=lambda p: (p["school"], TIER_RANK.get(p.get("fit"), 3), p["name"].lower()))
    if people:
        sheet(wb, "剑桥·LSE·Duke 校友", AL_COLS, [al_row(i, p) for i, p in enumerate(al_kept, 1)])
        failed += [[p["name"], p["school"] + " 校友", p.get("role", ""), p.get("verifyNote", ""), "\n".join((p.get("sources") or [])[:3])]
                   for p in people if p not in al_kept]

    sheet(wb, "复核未通过", [("名称", 24), ("名单", 14), ("现任 / 地点", 30), ("原因", 70), ("来源", 60)], failed)

    tiers = {t: sum(1 for a in kept if a.get("tier") == t) for t in "ABC"}
    with_x = sum(1 for a in kept if a.get("x") and a["x"] != "未找到")
    with_email = sum(1 for a in kept if a.get("email") and a["email"] != "未找到")
    ws = wb.create_sheet("说明")
    notes = [
        f"天使名单：{len(kept)} 位个人天使（不含中国大陆），A 档 {tiers['A']} 位，B 档 {tiers['B']} 位，C 档 {tiers['C']} 位。"
        + (f"硅谷 VC：{len(sv_kept)} 家湾区仍在投的机构。" if firms else "")
        + (f"剑桥 / LSE / Duke 校友投资人：{len(al_kept)} 位。" if people else "")
        + f"复核没通过的 {len(failed)} 条单独列在'复核未通过'。",
        "档位：A = 和邮件高度相关、近一两年仍在投、有公开渠道能联系到；B = 相关度好；C = 有可能。",
        "相关点：这位天使和邮件里哪几点最贴近，可选年轻创始人、RL 环境 / AI 数据、RSI / 前沿研究、量化交易、稳定币 / 加密、数据基础设施、英国 / LSE / 剑桥、YC 圈、华人圈。",
        "每位都有具体的天使投资记录和来源链接，并由第二个调研员逐条复核：投资是不是本人出的钱、人是不是对的、时间是不是近期。",
        f"联系方式只列本人公开的：X {with_x} 位，本人公开邮箱 {with_email} 位。没有按格式猜邮箱，也没有用数据经纪网站。查不到写'未找到'。"
        "大多数天使最好的渠道是 X 私信或熟人引荐（见'可能的引荐路径'）。",
        "开场句：放在邮件 Hi 之后的第一句，引用这位天使公开做过的一件事（投资、文章、演讲），比通用的 Hi 更容易被读下去。",
        "硅谷 VC：按首字母逐一列出总部或主要投资团队在旧金山湾区（旧金山、帕洛阿尔托、门洛帕克、山景城等）且 2024–2026 年仍在投的机构，"
        "包括种子基金、个人基金、大公司投资部门和投钱的加速器。匹配度：A = 投种子 / 天使轮且投过 AI 基础设施、数据或 agent；B = 早期并投 AI；C = 其他。"
        "'已在总表'表示这家也在《非大陆投资人总表》或审批页里。合伙人和投递渠道只列官方公开的。",
        "校友：每位都有来源同时证明他读过剑桥、LSE 或 Duke，并且在做投资；校友天使组织也列在里面。开场句可以提共同的学校。",
        "大致 / 把握中的条目：部分信息来自调研员已有的知识，没有逐条找到原文，发之前点开官网确认一次。",
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
