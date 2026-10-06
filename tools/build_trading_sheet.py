"""Build collateral/SimReal-交易机构投资人.xlsx (+ .csv of the firm sheet): trading-firm-backed investors.

The investors in scope are:
- the venture or strategic arms of prop-trading / HFT / market-making firms (like Tower Research Ventures,
  HRT Ventures);
- quant and multi-strategy hedge funds;
- crypto market makers;
- Chinese and Asian quant funds;
- people from those firms who angel invest.

Reads intel/investors/trading/*.json, each {"firms": [...], "people": [...], "noEvidence": [...]}, written by
the research sweep. It also reads published emails already in collateral/SimReal-投资人邮箱.csv.

Emails: only addresses the firm or person published themselves. Nothing is pattern-guessed, nothing comes from
data brokers, and press/IR/privacy/careers inboxes are dropped.

Sheets:
- 交易公司与基金
- 交易圈个人
- 暂无投资证据
- 说明

Needs openpyxl.

Usage: python3 tools/build_trading_sheet.py
"""
import csv
import json
import pathlib
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "intel" / "investors" / "trading"
EMAILS = ROOT / "collateral" / "SimReal-投资人邮箱.csv"
OUT = ROOT / "collateral" / "SimReal-交易机构投资人.xlsx"
OUT_CSV = ROOT / "collateral" / "SimReal-交易机构投资人.csv"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
BROKERS = re.compile(r"rocketreach|zoominfo|apollo\.io|contactout|signalhire|lusha|hunter\.io|snov\.io|leadiq|clearbit|"
                     r"neverbounce|theorg\.com|privateequitylist|email-format|emailformat", re.I)
SKIP_LOCAL = re.compile(r"^(press|media|pr|careers|jobs|privacy|legal|compliance|ir|investors|investor-relations|recruiting)@", re.I)
FIT_RANK = {"A": 0, "B": 1, "C": 2}
CONF = {"high": "高", "medium": "中", "low": "低"}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")


def key(name):
    name = re.sub(r"[（(].*?[)）]", " ", name or "").lower()
    name = re.sub(r"\b(ventures?|capital|partners|vc|fund|management|group|the|llc|lp|strategic|investments?)\b", "", name)
    return re.sub(r"[^a-z0-9一-鿿]+", "", name)


# First word of a firm's name -> one key per trading house, so its fund, VC arm and trading desk merge.
ALIAS = {"susquehanna": "sig", "hudson": "hrt", "jane": "janestreet", "flow": "flowtraders", "chicago": "ctc",
         "bam": "balyasny", "two": "deviation", "kronos": "kronos"}


def canon(name):
    """One key per trading house ("Jump Crypto / Jump Capital", "Jump Trading" -> "jump"); SIG Asia stays apart."""
    words = re.findall(r"[a-z0-9]+", re.sub(r"[（(].*?[)）]", " ", name or "").lower())
    if not words:
        return key(name)
    if words[:2] == ["sig", "asia"]:
        return "sigasia"
    if words[:2] == ["d", "e"]:
        return "deshaw"
    return ALIAS.get(words[0], words[0])


def flat(record):
    """Researchers sometimes return a list where text is expected; join those so every cell is text."""
    return {k: v if k == "sources" or not isinstance(v, list) else "；".join(str(x) for x in v) for k, v in record.items()}


def clean_email(value, source):
    """The published, pitch-usable addresses in a field; empty when the source is a broker."""
    if BROKERS.search(source or "") or BROKERS.search(value or ""):
        return []
    return [e for e in EMAIL.findall(value or "") if not SKIP_LOCAL.match(e)]


def known_emails():
    """Published emails already on file, by firm key."""
    out = {}
    if EMAILS.exists():
        with open(EMAILS, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                out.setdefault(canon(r["名称"]), []).append((r["邮箱"], r["来源链接"]))
    return out


def main():
    firms, people, none = [], [], []
    for path in sorted(SRC.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        firms += [flat(f) for f in data.get("firms", [])]
        people += [flat(p) for p in data.get("people", [])]
        none += [flat(n) for n in data.get("noEvidence", [])]
    known = known_emails()

    seen, rows = {}, []
    for f in sorted(firms, key=lambda f: (FIT_RANK.get(f.get("fit"), 3), f.get("confidence") != "high", f["firm"].lower())):
        k = canon(f["firm"])
        if k in seen:
            # The same house from another sweep: keep the best-rated record, add this one's sources to it.
            extra = [u for u in (f.get("sources") or []) if u not in seen[k]["sources"]]
            seen[k]["sources"] += extra
            continue
        f["sources"] = list(f.get("sources") or [])
        seen[k] = f
    for f in seen.values():
        k = canon(f["firm"])
        emails = clean_email(f.get("email"), f.get("emailSource"))
        sources = [f.get("emailSource", "")] * len(emails)
        for e, src in known.get(k, []):
            if e not in emails:
                emails.append(e)
                sources.append(src)
        rows.append([f.get("fit", ""), f["firm"], f.get("arm") or "", f.get("type", ""),
                     f.get("region") or f.get("hq", ""), f.get("evidence", ""), f.get("aiDeals", ""),
                     f.get("partner") or "未找到", "\n".join(emails) or "未找到", "\n".join(s for s in sources if s),
                     f.get("pitchForm") or "", f.get("why", ""), CONF.get(f.get("confidence"), ""),
                     "\n".join((f.get("sources") or [])[:5])])
    table = [[i] + r for i, r in enumerate(rows, 1)]

    people.sort(key=lambda p: (FIT_RANK.get(p.get("fit"), 3), p["name"].lower()))
    prow = [[i, p.get("fit", ""), p["name"], p.get("background", ""), p.get("role", ""), p.get("base", ""),
             p.get("investments", ""), p.get("x") or "未找到",
             "\n".join(clean_email(p.get("email"), p.get("emailSource"))) or "未找到", p.get("why", ""),
             CONF.get(p.get("confidence"), ""), "\n".join((p.get("sources") or [])[:5])] for i, p in enumerate(people, 1)]

    cols = [("序号", 6), ("匹配度", 7), ("交易公司 / 基金", 26), ("投资部门和方式", 34), ("类型", 14), ("地区", 16),
            ("投资证据", 44), ("投过的 AI / 数据 / 金融科技公司", 44), ("负责人", 26), ("公开邮箱", 30),
            ("邮箱来源", 36), ("投递表单", 30), ("为什么适合", 40), ("把握", 6), ("来源", 50)]
    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "交易公司与基金", cols, table)
    sheet(wb, "交易圈个人", [("序号", 6), ("匹配度", 7), ("姓名", 22), ("交易背景", 30), ("现任", 30), ("所在地", 16),
                         ("投资记录", 46), ("X", 24), ("公开邮箱", 26), ("为什么适合", 40), ("把握", 6), ("来源", 50)], prow)
    sheet(wb, "暂无投资证据", [("机构", 28), ("说明", 90)], [[n.get("firm", ""), n.get("note", "")] for n in none])

    with_email = sum(1 for r in table if r[9] != "未找到")
    ws = wb.create_sheet("说明")
    notes = [
        f"交易公司与基金：{len(table)} 家（A 档 {sum(1 for r in table if r[1] == 'A')} 家），其中有公开邮箱的 {with_email} 家；"
        f"交易圈个人：{len(prow)} 位；查过但没找到投资初创公司证据的 {len(none)} 家，单独列出。",
        "范围：自营 / 高频 / 做市公司的投资部门（如 Tower Research Ventures、HRT Ventures）、量化和多策略对冲基金、加密做市商、"
        "中国和亚洲量化私募，以及这些公司里自己做天使投资的创始人和合伙人。",
        "每家都附了投资证据（具体投过的公司和年份）和来源链接。匹配度：A = 投早期且投过 AI / 数据 / 交易基础设施；B = 有战略投资、方向相关；C = 有可能。",
        "邮箱只列机构或本人自己公开的地址，没有按格式猜，也没有用数据网站；press@、ir@、privacy@、careers@ 一律不收。没有邮箱的看'投递表单'或负责人。",
        "这批信息来自搜索结果摘要（本环境打不开网站），发之前点开来源确认一次。",
        "导入 Google 表格：drive.google.com → 新建 → 文件上传 → 右键 → 打开方式 → Google 表格。",
    ]
    for line in notes:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    for r in ws.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    wb.save(OUT)
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([c for c, _ in cols])
        w.writerows(table)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(table)} firms ({with_email} with email), {len(prow)} people, {len(none)} without evidence")


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


if __name__ == "__main__":
    main()
