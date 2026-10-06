"""Build collateral/SimReal-投资人邮箱.xlsx (+ .csv): every published investor email we have, one row per address.

Sources:
- lists/investors.csv and intel/outreach/V*.csv: researched investors, with published emails and fund inboxes;
- intel/investors/enrich.json and intel/resources/resources.json: inboxes found while checking;
- intel/investors/emails-found.json: the email hunt over the investor, angel, Silicon Valley VC and alumni
  lists, written by a search-snippet sweep and kept only when a provenance check passed.

Only addresses the person or the firm published themselves. Nothing is pattern-guessed and nothing
comes from data brokers.

Sheets:
- 邮箱: one row per address;
- 还没找到: targets with no address yet, with the best other channel;
- 说明.
Also writes collateral/SimReal-邮件合并.csv for Gmail mail merge (non-mainland rows only): First name, Email,
Company, Opener (the sourced one-line hook for that investor; a fund inbox gets "Could you pass this to ...").

Needs openpyxl.

Usage: python3 tools/build_email_sheet.py <targets.json>
(targets.json lists everyone the hunt covered: name, kind, region, lists.)
"""
import csv
import json
import pathlib
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOUND = ROOT / "intel" / "investors" / "emails-found.json"
OUT = ROOT / "collateral" / "SimReal-投资人邮箱.xlsx"
OUT_CSV = ROOT / "collateral" / "SimReal-投资人邮箱.csv"
MERGE_CSV = ROOT / "collateral" / "SimReal-邮件合并.csv"
MAINLAND = re.compile(r"^(国内|中国大陆)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL = re.compile(r"https?://[^\s;，；、）)\]]+")
BROKERS = re.compile(r"rocketreach|zoominfo|apollo\.io|contactout|signalhire|lusha|hunter\.io|snov\.io|leadiq|clearbit|adapt\.io|"
                     r"theorg\.com|email-format|emailformat|getemail|voilanorbert|anymailfinder", re.I)
SKIP_LOCAL = re.compile(r"^(press|media|careers|jobs|privacy|legal|compliance|ir|investors|investor-relations|recruiting|noreply|no-reply)@", re.I)
# Addresses found on these pages serve another purpose (privacy requests, terms), not pitches.
OFF_PAGE = re.compile(r"privacy|terms|legal|cookie|gdpr", re.I)
KIND_RANK = {"个人公开": 0, "机构投递": 1, "机构通用": 2}
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
INBOX = re.compile(r"^(pitch|seed|deals|submit|apply|embed|aistart|ventures|build|strategicvc|bp|bpchina|invest|founders|startups|plan)@", re.I)


def kind_of(email, owner_is_person):
    if owner_is_person:
        return "个人公开"
    return "机构投递" if INBOX.match(email) else "机构通用"


def how_to(row):
    if row["kind"] == "个人公开":
        return f"直接写给 {row['owner']}" if row["owner"] else "直接写给本人"
    if row.get("contact") and row["contact"] not in ("未找到", ""):
        return f"第一句写明请转交 {row['contact']}（Could you pass this to {row['contact']}?）"
    return "写给团队（Hi team）"


def main(targets_path):
    targets = json.loads(pathlib.Path(targets_path).read_text(encoding="utf-8"))
    info = {t["name"]: t for t in targets}
    rows, seen = [], set()

    def add(name, email, kind, owner, source, quote, origin, contact=""):
        e = email.strip().strip(".").lower()
        if e in seen or "simreal" in e or SKIP_LOCAL.match(e) or BROKERS.search(source or "") or OFF_PAGE.search(source or ""):
            return
        seen.add(e)
        t = info.get(name, {})
        rows.append({"name": name, "category": t.get("kind", ""), "region": t.get("region", ""), "email": e, "kind": kind,
                     "owner": owner, "contact": contact, "source": source, "quote": quote, "origin": origin,
                     "lists": "、".join(t.get("lists", []))})

    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            for e in EMAIL.findall(r["邮箱"] or ""):
                add(r["名称"], e, "个人公开", r["联系人"], " ".join(URL.findall(r["邮箱来源"])[:2]) or r["邮箱来源"],
                    r["邮箱来源"], "之前的调研", r["联系人"])
            for e in EMAIL.findall(r["备用渠道"] or ""):
                add(r["名称"], e, kind_of(e, False), r["名称"], " ".join(URL.findall(r["备用渠道"])[:2]) or r["备用渠道"],
                    r["备用渠道"], "之前的调研", r["联系人"])
    for seg in ("V1a", "V1b", "V2", "V3"):
        with open(ROOT / "intel" / "outreach" / f"{seg}.csv", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                for e in EMAIL.findall(r["邮箱"] or ""):
                    add(r["名称"], e, "个人公开", r["联系人"], " ".join(URL.findall(r["邮箱来源"])[:2]) or r["邮箱来源"],
                        r["邮箱来源"], "之前的调研", r["联系人"])
                for e in EMAIL.findall(r["备用渠道"] or ""):
                    add(r["名称"], e, kind_of(e, False), r["名称"], " ".join(URL.findall(r["备用渠道"])[:2]) or r["备用渠道"],
                        r["备用渠道"], "之前的调研", r["联系人"])
    for name, x in json.loads((ROOT / "intel" / "investors" / "enrich.json").read_text(encoding="utf-8")).items():
        for e in EMAIL.findall(x.get("channel") or ""):
            add(name, e, kind_of(e, False), name, " ".join(URL.findall(x["channel"])[:2]), x["channel"], "之前的调研")
    for i in json.loads((ROOT / "intel" / "resources" / "resources.json").read_text(encoding="utf-8"))["items"]:
        if i["category"] == "投资人渠道":
            for e in EMAIL.findall(i.get("howToApply") or ""):
                add(i["name"], e, kind_of(e, False), i["name"], " ".join(i["sources"][:2]), i["howToApply"], "之前的调研")

    if FOUND.exists():
        found = json.loads(FOUND.read_text(encoding="utf-8"))
        verdict = {(c["name"], c["email"].lower()): c for c in found.get("checks", [])}
        for r in found["results"]:
            for e in r.get("emails") or []:
                c = verdict.get((r["name"], e["email"].lower()))
                if c is None or not c["keep"] or e["email"].lower() not in (e.get("snippet") or "").lower():
                    continue
                add(r["name"], e["email"], c["kind"], e["owner"], e["url"], e["snippet"], "这次搜索")

    rows.sort(key=lambda r: (KIND_RANK.get(r["kind"], 3), r["name"].lower()))
    cols = [("序号", 6), ("名称", 26), ("类别", 10), ("地区", 18), ("邮箱", 32), ("邮箱类型", 10), ("邮箱属于", 20),
            ("写法", 34), ("来源链接", 44), ("来源原文", 50), ("出自", 10), ("在哪些名单里", 26)]
    table = [[i, r["name"], r["category"], r["region"], r["email"], r["kind"], r["owner"], how_to(r), r["source"],
              r["quote"], r["origin"], r["lists"]] for i, r in enumerate(rows, 1)]

    have = {r["name"] for r in rows}
    missing = [t for t in targets if t["name"] not in have]
    searched = set()
    if FOUND.exists():
        searched = {r["name"] for r in json.loads(FOUND.read_text(encoding="utf-8"))["results"] if r.get("searched")}
    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "邮箱", cols, table)
    missing.sort(key=lambda t: (t["name"] not in searched, t["prio"], t["name"].lower()))
    sheet(wb, "还没找到", [("名称", 28), ("状态", 16), ("类别", 10), ("地区", 20), ("官网域名", 22), ("在哪些名单里", 26)],
          [[t["name"], "搜过，没有公开邮箱" if t["name"] in searched else "还没搜", t["kind"], t["region"], t["domain"],
            "、".join(t["lists"])] for t in missing])

    personal = sum(1 for r in rows if r["kind"] == "个人公开")
    ws = wb.create_sheet("说明")
    notes = [
        f"共 {len(rows)} 个邮箱，覆盖 {len(have)} 家机构或个人：本人公开 {personal} 个，机构投递 / 通用邮箱 {len(rows) - personal} 个。"
        f"'还没找到'列了其余 {len(missing)} 家：搜过但没有公开邮箱的 {sum(1 for t in missing if t['name'] in searched)} 家，"
        f"还没搜的 {sum(1 for t in missing if t['name'] not in searched)} 家（这一轮的搜索额度只够排在前面的 {len(searched)} 家）。",
        "只收本人或所在机构自己公开发布的地址（官网、官方文档、本人主页、本人帖子），每个都有来源链接和搜索结果里的原文。"
        "没有按格式猜（比如 名字@基金.com），也没有用 RocketReach、ZoomInfo、Apollo、Hunter 等数据网站；这类来源一律剔除。",
        "'出自'为'这次搜索'的地址，是从搜索结果的摘要里找到的（本环境打不开基金官网），由第二个调研员检查过来源，"
        "剔除了 press@、privacy@、careers@、LP 询问等非投资用途的邮箱。摘要有时会转述网页，所以发之前请点开来源链接确认一次，个人邮箱尤其要确认。",
        "写法：机构邮箱在第一句写明请转交哪位合伙人；本人邮箱直接写给本人。",
        "没有邮箱的：天使多数可以在 X 上私信（见《天使与硅谷VC名单》的 X 列）；基金可以用官网表单或熟人引荐。",
        "导入 Google 表格：drive.google.com → 新建 → 文件上传 → 右键 → 打开方式 → Google 表格。",
    ]
    for line in notes:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    for r in ws.iter_rows():
        for cell in r:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    write_merge(rows)
    wb.save(OUT)
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([c for c, _ in cols])
        w.writerows(table)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} emails for {len(have)} targets ({personal} personal), {len(missing)} without")


def openers():
    """Sourced one-line hooks per investor name, from the approval page, the angel list and the alumni list."""
    hooks = {}
    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["语言"] == "en" and r["钩子"]:
                hooks[r["名称"]] = r["钩子"]
    for name in ("angels.json", "alumni.json"):
        path = ROOT / "intel" / "investors" / name
        if path.exists():
            for a in json.loads(path.read_text(encoding="utf-8")):
                if a.get("keep", True) and a.get("opener"):
                    hooks.setdefault(a["name"], a["opener"])
    return hooks


def write_merge(rows):
    hooks = openers()
    with open(MERGE_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["First name", "Email", "Company", "Opener"])
        for r in rows:
            if MAINLAND.match(r["region"] or "") or re.search(r"[\u4e00-\u9fff]", r["name"]):
                continue
            company = re.split(r"[（(]", r["name"])[0].strip()
            hook = hooks.get(r["name"], "")
            if r["kind"] == "个人公开":
                first = (r["owner"] or "").split()[0] if r["owner"] else "there"
            else:
                first = company + " team"
                contact = r.get("contact") or ""
                if contact and not contact.startswith("未找到"):
                    hook = f"Could you pass this to {contact}? " + hook
            w.writerow([first, r["email"], company, hook.strip()])


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
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions


if __name__ == "__main__":
    main(sys.argv[1])
