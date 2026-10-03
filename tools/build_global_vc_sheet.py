"""Build collateral/SimReal-非大陆投资人总表.xlsx (+ .csv of the main sheet) from everything we have researched.

Merges, one row per investor:
- lists/investors.csv: the approval-page investors, with contacts, published emails and hooks;
- intel/investors/table.json: the cap-table investor table;
- intel/investors/profiles.json: stage, check size and notes per investor;
- intel/outreach/seeds.json: the V1 overseas seed list and the non-mainland part of V2;
- intel/resources/resources.json: investor channels, accelerators and fellowships;
- intel/investors/enrich.json: HQ / type / website / pitch-channel checks for rows whose region was unconfirmed;
- intel/investors/expand.json: investors found in a later sweep of comparable rounds, each with a source.

Mainland China investors are left out. Funds headquartered in mainland China with a Hong Kong or
US-dollar arm go to a separate reference sheet.

Sheets:
- 非大陆投资人
- 加速器与早期项目
- 大陆机构境外基金（参考）
- 找更多投资人
- 说明

Needs openpyxl.

Usage: python3 tools/build_global_vc_sheet.py
"""
import csv
import json
import pathlib
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_investor_table import norm, squash  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "collateral" / "SimReal-非大陆投资人总表.xlsx"
OUT_CSV = ROOT / "collateral" / "SimReal-非大陆投资人总表.csv"
ENRICH = ROOT / "intel" / "investors" / "enrich.json"
EXPAND = ROOT / "intel" / "investors" / "expand.json"
CONFIDENCE = {"high": "已核实", "medium": "大致", "low": "存疑"}
NONE = ("", "未找到", "无", "未确认", "未知", None)
CJK = re.compile(r"[一-鿿]")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# English-named investors from cap tables that are headquartered in mainland China.
MAINLAND_EN = {"baicapital", "classin"}
# Chinese-named investors from cap tables that are not mainland.
NON_MAINLAND_CN = {"大湾区共同家园基金": "中国香港"}
# Different spellings of the same investor across sources -> the name to merge into.
SAME_AS = {"Hudson River Trading": "HRT Ventures", "淡马锡 / Vertex（新加坡）": "Vertex Ventures Southeast Asia & India",
           "香港投资管理有限公司 HKIC（港投公司）": "HKIC"}
GROUP_LABEL = {1: "C 组", 2: "B 组", 3: "A 组", 9: "暂缓"}
GROUP_RANK = {3: 0, 2: 1, 1: 2, 9: 4}
PLATFORM = re.compile(r"Signal by NFX|OpenVC|vcsheet|AngelList|Superscout|VC scouts|Launching Legends|Cerebral Valley|operator angels", re.I)
HEAD_FONT = Font(name="Arial", bold=True, color="FFFFFF")
HEAD_FILL = PatternFill("solid", fgColor="111110")
BODY_FONT = Font(name="Arial", size=10)
WRAP = Alignment(wrap_text=True, vertical="top")


def blank(v):
    return (v.strip() if isinstance(v, str) else v) in NONE


def keys_of(name):
    """Every key a name can match on: the normalized name, the part in parentheses, the squashed name."""
    ks = {norm(name), squash(name)}
    for inner in re.findall(r"[（(]([^）)]+)[）)]", name or ""):
        if not CJK.search(inner) and len(inner) > 3:
            ks.add(norm(inner))
    head = re.split(r"[（(/]", name or "")[0].strip()
    if head:
        ks.update({norm(head), squash(head)})
    ks = {k for k in ks if k and len(k) > 1}
    return ks or {(name or "").strip().lower()}


def urls(text):
    return re.findall(r"https?://[^\s;，；、）)\]]+", text or "")


class Book:
    def __init__(self):
        self.rows, self.index = [], {}

    def find(self, name):
        for k in keys_of(SAME_AS.get(name, name)):
            if k in self.index:
                return self.index[k]
        return None

    def add(self, name, src, **fields):
        row = self.find(name)
        if row is None:
            row = {"name": name, "srcs": [], "sources": []}
            self.rows.append(row)
        for k in keys_of(name) | keys_of(SAME_AS.get(name, name)):
            self.index.setdefault(k, row)
        if src not in row["srcs"]:
            row["srcs"].append(src)
        for k, v in fields.items():
            if k == "sources":
                row["sources"] += [u for u in v if u not in row["sources"]]
            elif not blank(v) and blank(row.get(k)):
                row[k] = v.strip() if isinstance(v, str) else v
        return row


def region_ok(region):
    """True for non-mainland, False for mainland, None when unknown."""
    r = region or ""
    if r.startswith("海外") or r.startswith("中国香港") or r.startswith("香港") or r.startswith("新加坡"):
        return True
    if r.startswith("国内") or r.startswith("中国大陆"):
        return False
    return None


def main():
    book, reference, programs, platforms = Book(), [], [], []
    waves = json.loads((ROOT / "intel" / "outreach" / "investor-waves.json").read_text(encoding="utf-8"))
    enrich = json.loads(ENRICH.read_text(encoding="utf-8")) if ENRICH.exists() else {}
    excluded = 0

    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not region_ok(r["地区"]):
                excluded += 1
                continue
            w = waves.get(r["slug"], {})
            email, esrc = r["邮箱"], r["邮箱来源"]
            book.add(r["名称"], "审批页", kind=r["类型"], region=r["地区"], verified="是", website=r["官网"],
                     contact=r["联系人"], title=r["职位"], contactSource=r["联系人来源"], email=email,
                     emailSource=esrc, channel=r["备用渠道"], hook=r["钩子"], angle=r["切入点"], risk=r["风险"],
                     group=w.get("wave"), card="v-" + r["slug"],
                     sources=urls(r["联系人来源"]) + urls(r["钩子来源"]) + urls(esrc))

    for p in json.loads((ROOT / "intel" / "investors" / "profiles.json").read_text(encoding="utf-8")):
        ok = region_ok(p["region"])
        if ok is False:
            continue
        row = book.find(p["name"])
        if row is None and ok is None:
            continue
        book.add(p["name"], "投资人档案", kind=p["kind"], region=p["region"], verified="是" if ok else None,
                 stage=p["stage"], check=p["check"], lead=p["lead"], contact=p["contact"],
                 contactSource=p.get("contactSource"), email=p["email"], emailSource=p.get("emailSource"),
                 note=p.get("note"), sources=p.get("sources") or [])

    for t in json.loads((ROOT / "intel" / "investors" / "table.json").read_text(encoding="utf-8")):
        name = t["name"]
        if re.match(r"unnamed|未具名", name, re.I):
            continue
        ok = region_ok(t["region"])
        region, verified = t["region"], "是"
        if ok is None:
            e = enrich.get(name) or {}
            if e.get("mainland") is True:
                ok = False
            elif e.get("region"):
                ok, region, verified = True, e["region"], CONFIDENCE.get(e.get("confidence"), "大致")
            elif name in NON_MAINLAND_CN:
                ok, region = True, NON_MAINLAND_CN[name]
            elif CJK.search(name) or squash(name) in MAINLAND_EN:
                ok = False
            else:
                ok, region, verified = True, "未核实", "否"
        if not ok:
            excluded += 1
            continue
        e = enrich.get(name) or {}
        book.add(name, "同类公司反查" if t["status"].startswith("新增") else "审批页", kind=e.get("kind") or t["kind"],
                 region=region, verified=verified, stage=t["stage"], check=t["check"], lead=t["lead"],
                 similar=t["similar"], contact=t["contact"], email=t["email"], website=e.get("website"),
                 channel=e.get("channel"),
                 note=e.get("note"), group=t["group"] if t["group"] != 1 or t["status"] == "已在审批页" else None,
                 sources=urls(t["sources"]) + (e.get("sources") or []))

    for x in json.loads(EXPAND.read_text(encoding="utf-8")) if EXPAND.exists() else []:
        if x.get("mainland"):
            excluded += 1
            continue
        book.add(x["name"], "新补充（2026-10）", kind=x["kind"], region=x["region"],
                 verified=CONFIDENCE.get(x.get("confidence"), "大致"), stage=x.get("stage"), similar=x.get("backed"),
                 website=x.get("website"), channel=x.get("channel"), note=x.get("note"), sources=x.get("sources") or [])

    seeds = json.loads((ROOT / "intel" / "outreach" / "seeds.json").read_text(encoding="utf-8"))
    for s in seeds["V1"]:
        if s["名称"].startswith("（"):
            continue
        book.add(s["名称"], "海外种子名单", kind=s["类型"], region="海外（" + s["地区"] + "）", verified="是",
                 contact=s["已知对接人"], similar=s["本赛道已投"], hook=s["匹配理由"],
                 sources=urls(s["对接人来源"]) + urls(s.get("观点链接")))
    for s in seeds["V2"]:
        reg = s.get("地区") or ""
        if s["名称"].startswith("（") or not reg:
            continue
        if "中国大陆" not in reg and "北京" not in reg and "上海" not in reg:
            book.add(s["名称"], "国内种子名单（境外部分）", kind=s["类型"], region=reg, verified="是",
                     contact=s["已知对接人"], similar=s["本赛道已投"], hook=s["匹配理由"],
                     sources=urls(s["对接人来源"]) + urls(s.get("观点链接")))
        elif re.search(r"香港|美国|新加坡|德国", reg):
            reference.append([s["名称"], s["类型"], reg, s["已知对接人"], s["本赛道已投"], s["匹配理由"],
                              " ; ".join(urls(s["对接人来源"]) + urls(s.get("观点链接")))])

    res = json.loads((ROOT / "intel" / "resources" / "resources.json").read_text(encoding="utf-8"))
    for i in res["items"]:
        if i.get("verdict") == "撤下":
            continue
        mainland = i["region"].startswith("中国大陆") or i["region"].startswith("中国 /")
        if i["category"] == "投资人渠道":
            if PLATFORM.search(i["name"]):
                platforms.append([i["name"], i["region"], i["offer"], i["howToApply"], " ; ".join(i["sources"])])
            elif mainland or "蓝驰" in i["name"]:
                reference.append([i["name"], "VC", i["region"], "", "", i["fitWhy"], " ; ".join(i["sources"])])
            else:
                book.add(i["name"], "资源清单", kind="天使网络" if "Angel" in i["name"] else "VC", region=i["region"],
                         verified="是", hook=i["fitWhy"], channel=i["howToApply"], sources=i["sources"])
        elif i["category"] in ("加速器与孵化器", "Fellowship 与早期项目") and not mainland:
            programs.append([i["name"], i["category"], i["region"], i["status"], i["timing"], i["offer"],
                             i["eligibility"], i["howToApply"], " ; ".join(i["sources"])])

    platforms += [
        ["Matt Estes：750 家种子基金表格", "全球（以美国为主）", "Luke Sophinos 线程推荐的免费名单，2022 年整理", "原线程里有链接；本环境打不开，没能核对", ""],
        ["Shai Goldman：219 家早期 VC 的 Airtable", "美国", "同上", "同上", ""],
        ["Trace Cohen：500 家美国活跃投资人表格", "美国", "同上", "同上", ""],
        ["Yuliya Bel：愿意接受冷接触的投资人名单", "全球", "同上", "同上", ""],
    ]

    def order(r):
        has_email = 0 if not blank(r.get("email")) else 1
        return (0 if r.get("card") else 1, GROUP_RANK.get(r.get("group"), 3), has_email, r["name"].lower())

    rows = sorted(book.rows, key=order)
    cols = [("序号", 6), ("机构 / 投资人", 28), ("类型", 10), ("地区", 18), ("地区已核实", 9), ("官网", 26), ("分组", 8),
            ("阶段", 22), ("单笔金额", 24), ("是否领投", 22), ("投过的同类公司", 34), ("联系人", 22), ("职位", 18),
            ("公开邮箱", 28), ("邮箱类型", 10), ("邮箱来源", 36), ("备用渠道（表单 / 基金邮箱）", 36), ("开场钩子 / 匹配理由", 60),
            ("备注", 40), ("审批页卡片", 18), ("出处", 20), ("来源链接", 60)]
    table = []
    for n, r in enumerate(rows, 1):
        email, ekind, esrc = pick_email(r)
        hook = r.get("hook") or r.get("angle") or ""
        note = "；".join(x for x in [r.get("note"), r.get("risk") and "风险：" + r["risk"]] if x)
        table.append([n, r["name"], r.get("kind") or "", r.get("region") or "", r.get("verified") or "",
                      r.get("website") or "", GROUP_LABEL.get(r.get("group"), ""), r.get("stage") or "", r.get("check") or "",
                      r.get("lead") or "", r.get("similar") or "", r.get("contact") or "未找到", r.get("title") or "",
                      email, ekind, esrc, r.get("channel") or "", hook, note, r.get("card") or "",
                      "、".join(r["srcs"]), "\n".join(r["sources"][:6])])

    wb = Workbook()
    wb.remove(wb.active)
    sheet(wb, "非大陆投资人", cols, table)
    sheet(wb, "加速器与早期项目", [("项目", 34), ("类别", 16), ("地区", 26), ("状态", 10), ("时间", 30), ("给什么", 44),
                                ("谁能申请", 40), ("怎么申请", 40), ("来源", 50)], programs)
    sheet(wb, "大陆机构境外基金（参考）", [("机构", 28), ("类型", 10), ("地区", 26), ("已知对接人", 30), ("本赛道已投", 40),
                                     ("匹配理由", 60), ("来源", 50)], reference)
    sheet(wb, "找更多投资人", [("名单 / 平台", 40), ("地区", 20), ("内容", 50), ("怎么用", 50), ("来源", 50)], platforms)

    added = sum(1 for r in rows if "新补充（2026-10）" in r["srcs"])
    with_email = sum(1 for t in table if t[13] != "未找到")
    personal = sum(1 for t in table if t[14] == "个人公开")
    unverified = sum(1 for t in table if t[4] in ("否", "存疑"))
    ws = wb.create_sheet("说明")
    notes = [
        f"共 {len(table)} 家非中国大陆投资人（VC、天使、战略投资、加速器）：之前调研查到的 {len(table) - added} 家，加上 2026-10 补查的 {added} 家。"
        f"其中有公开邮箱 {with_email} 家"
        f"（本人邮箱 {personal} 家，机构投递邮箱 {with_email - personal} 家），已在审批页、有写好邮件的 {sum(1 for t in table if t[19])} 家。另有加速器与早期项目 {len(programs)} 个，"
        f"大陆机构的境外/美元基金 {len(reference)} 家（参考），找更多投资人的名单和平台 {len(platforms)} 个。",
        f"已排除中国大陆机构 {excluded} 家。香港、新加坡、台湾和其他海外机构都算在内。",
        "排序：审批页里已有邮件的排最前（A 组 → B 组 → C 组，有邮箱的在前），其余按名称排；用'出处'列可以筛选来源。",
        "'地区已核实'：是 = 之前调研时已核实；已核实 / 大致 / 存疑 = 2026-10 补查时的把握程度（大致 = 根据公开资料和常识判断，没有逐条找到官网原文）。"
        f"还没把握的（否 / 存疑）{unverified} 家。",
        "邮箱只列本人或所在机构公开发布的地址，'邮箱来源'列写了出处；没有按格式猜，也没有用数据经纪网站。查不到写'未找到'。",
        "出处：审批页 = 已写好冷邮件的 148 家投资人卡片；同类公司反查 = 从 50 多家同类公司（RL 环境、评测、专家数据）的融资记录里找到的投资人；"
        "海外种子名单 / 投资人档案 / 资源清单 = 之前几轮调研的结果；"
        f"新补充（2026-10）= 这次按同类公司融资记录和 AI 早期基金补查到的 {added} 家，每家附来源，并由第二个调研员复核过。",
        "导入 Google 表格：打开 drive.google.com → 新建 → 文件上传，选这个 xlsx → 上传后右键 → 打开方式 → Google 表格。"
        "或者在 sheets.new 里 文件 → 导入 → 上传。",
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
        w.writerow([c for c, _ in cols])
        w.writerows(table)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(table)} investors ({with_email} with email, {unverified} region unverified), "
          f"{len(programs)} programs, {len(reference)} reference, {len(platforms)} platforms; excluded {excluded} mainland")


def pick_email(r):
    """(address, kind, source): the investor's own published address first, then a fund inbox from the channel."""
    for field in ("email", "channel"):
        found = EMAIL.findall(r.get(field) or "")
        if found:
            e = found[0]
            local = e.lower().split("@")[0]
            person = (r.get("contact") or "").lower()
            kind = "个人公开" if field == "email" and len(local) > 2 and local in person else "机构投递"
            src = r.get("emailSource") if field == "email" and not blank(r.get("emailSource")) else r.get(field)
            return e, kind, src or ""
    return "未找到", "", ""


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


if __name__ == "__main__":
    main()
