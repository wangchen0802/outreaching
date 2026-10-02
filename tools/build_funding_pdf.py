"""Build collateral/src/funding-playbook.html: the fundraising playbook (Luke Sophinos' cold-email
method applied to SimReal) plus every resource and channel from intel/resources/resources.json.

Inputs: ops/templates.md (investor email), lists/investors.csv + intel/outreach/investor-waves.json
(C/B/A groups), intel/investors/captable.json (comparable-company cap tables, optional) and
intel/resources/resources.json. Render the HTML to PDF with the Chromium script in the scratchpad.

Usage: python3 tools/build_funding_pdf.py
"""
import csv
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_resources_sheet as rs  # noqa: E402
import templates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "collateral" / "src" / "funding-playbook.html"
CN = re.compile(r"中国|国内|香港|上海|北京|深圳|杭州|广东|张江")
CAT_ORDER = ["加速器与孵化器", "Fellowship 与早期项目", "非稀释资助", "比赛与奖金", "算力与云额度", "投资人渠道",
             "客户与销售渠道", "曝光与发布平台", "社区与活动", "政府与政策", "创业福利"]
TACTIC_CAT = {"accelerators": "加速器", "fellowships-grants": "资助", "compute-perks": "算力与福利",
              "investor-access": "投资人渠道", "community-events": "社区与活动", "visibility-launch": "曝光",
              "sales-channels": "销售渠道", "china-programs": "国内"}
STATUS_RANK = {"开放中": 0, "滚动申请": 1, "即将开放": 2, "未确认": 3, "已截止": 4}
FIT_RANK = {"高": 0, "中": 1, "低": 2}


def e(s):
    return html.escape(str(s or ""))


def link(s):
    """Escape text and turn bare URLs into short links."""
    out = e(s)
    return re.sub(r"(https?://[^\s<>\"'）)，、；]+)", lambda m: f'<a href="{m.group(1)}">{m.group(1).split("://", 1)[1][:60]}</a>', out)


def style():
    src = (ROOT / "collateral" / "src" / "customer-playbook.html").read_text(encoding="utf-8")
    css = src.split("<style>", 1)[1].split("</style>", 1)[0]
    return css + """
  .tpl { border: 0.6pt solid var(--rule); background: var(--paper); margin: 2mm 0 4mm; break-inside: avoid; }
  .tpl .row { display: grid; grid-template-columns: 30mm 1fr; border-top: 0.6pt solid var(--rule); }
  .tpl .row:first-child { border-top: 0; }
  .tpl .k { padding: 2.4mm 3mm; font: 500 8pt/1.45 var(--sans); color: var(--accent); border-right: 0.6pt solid var(--rule); }
  .tpl .v { padding: 2.4mm 3.5mm; font: 400 8.6pt/1.6 var(--sans); color: var(--ink); white-space: pre-wrap; }
  .tpl .v.subj { font-weight: 500; }
  .groups { display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1.2pt solid var(--ink); border-bottom: 0.6pt solid var(--rule); margin: 2mm 0 4mm; }
  .groups > div { padding: 3mm 2.5mm 3mm 0; display: grid; gap: 0.8mm; align-content: start; }
  .groups > div + div { padding-left: 3mm; border-left: 0.6pt solid var(--rule); }
  .groups .n { font: 400 20pt/1.05 var(--serif); color: var(--ink); }
  .groups .t { font: 500 9pt/1.35 var(--sans); color: var(--ink); }
  .groups .d { font-size: 7.8pt; line-height: 1.5; color: var(--muted); }
  table.res td, table.res th { font-size: 7.9pt; line-height: 1.5; }
  table.res td:first-child { width: 34mm; }
  table.res td a, .sources a { color: var(--body); text-decoration: none; word-break: break-all; }
  .fit { display: inline-block; font: 400 7pt/1 var(--mono); padding: 0.8mm 1.2mm; border: 0.5pt solid var(--rule); border-radius: 0.8mm; color: var(--muted); margin-top: 1mm; }
  .fit.hi { color: var(--accent); border-color: var(--accent); }
  .cat h3 { break-after: avoid; }
  .names { font-size: 8.4pt; line-height: 1.7; }
"""


def investor_groups():
    with open(ROOT / "lists" / "investors.csv", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    waves = json.loads((ROOT / "intel" / "outreach" / "investor-waves.json").read_text(encoding="utf-8"))
    groups = {1: [], 2: [], 3: [], 9: []}
    for r in rows:
        w = waves.get(r["slug"], {}).get("wave", 2)
        groups.setdefault(w, []).append(r)
    return groups


def email_rows():
    t = templates.load()
    en = t[("investor", "email", "en")]
    subject, body = en.split("\n", 1)
    paras = [p.strip() for p in body.strip().split("\n\n")]
    # paras: greeting, hook, team, company, traction, ask, signature
    labels = ["① 个性化开场", "② 证明我们做得成", "③ 一句话讲公司", "④ 进展", "⑤ 明确请求"]
    hook_note = "[Hook]：针对这家机构的一句话，引用它最近投的公司、发的文章或观点（每封不同，已写好）"
    rows = [("主题", subject.split(":", 1)[1].strip(), True), ("称呼", paras[0], False)]
    rows.append((labels[0], hook_note, False))
    for label, p in zip(labels[1:], paras[2:6]):
        rows.append((label, p, False))
    rows.append(("署名", paras[6], False))
    return rows


def short(text, n):
    """First clause of a field, capped at n characters."""
    t = (text or "").strip()
    for sep in ("；", "。", ";"):
        head = t.split(sep, 1)[0]
        if len(head) <= n and head != t:
            return head
    return t if len(t) <= n else t[:n].rstrip("，、 ") + "…"


def apply_link(r):
    m = re.search(r"https?://[^\s<>\"'）)，、；]+", r["howToApply"] or "") or next(
        (re.match(r"https?://\S+", s) for s in r["sources"] if re.match(r"https?://", s)), None)
    if not m:
        return e(short(r["howToApply"], 40))
    url = m.group(0)
    return f'<a href="{url}">{e(url.split("://", 1)[1][:42])}</a>'


def resource_table(items):
    out = ['<table class="res"><thead><tr><th>名称</th><th>给什么</th><th style="width:36mm">时间</th>'
           '<th style="width:36mm">链接</th></tr></thead><tbody>']
    for r in items:
        fit = f'<span class="fit{" hi" if r["fit"] == "高" else ""}">适合度 {e(r["fit"])} · {e(r["status"])}</span>'
        out.append(f'<tr><td>{e(r["name"])}<br>{fit}</td><td>{e(short(r["offer"], 90))}</td>'
                   f'<td>{e(short(r["timing"], 60))}</td><td>{apply_link(r)}</td></tr>')
    out.append("</tbody></table>")
    return "".join(out)


def order(r):
    return (STATUS_RANK.get(r["status"], 3), r["_deadline"] or "9999", FIT_RANK[r["fit"]], r["name"].lower())


def main():
    data = json.loads((ROOT / "intel" / "resources" / "resources.json").read_text(encoding="utf-8"))
    items = [r for r in data["items"] if r.get("verdict") != "撤下"]
    for r in items:
        r["_deadline"] = "" if r["status"] == "已截止" else rs.next_deadline(r["timing"])
    verified = sum(1 for r in items if r.get("verdict") in ("确认", "更正"))
    groups = investor_groups()
    n_inv = sum(len(v) for v in groups.values())
    cap_path = ROOT / "intel" / "investors" / "captable.json"
    cap = json.loads(cap_path.read_text(encoding="utf-8")) if cap_path.exists() else None

    soon = sorted([r for r in items if r["_deadline"] and r["_deadline"] <= "2026-12-31" and r["fit"] != "低"],
                  key=lambda r: (r["_deadline"], FIT_RANK[r["fit"]]))
    overseas = [r for r in items if not CN.search(r["region"])]
    china = sorted([r for r in items if CN.search(r["region"]) and r["fit"] != "低" and r["status"] != "已截止"], key=order)
    later = sorted([r for r in items if r["fit"] == "低" or r["status"] == "已截止"], key=lambda r: r["name"].lower())

    h = [f"<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><title>SimReal 融资与资源手册</title><style>{style()}</style></head><body>"]

    # Cover
    h.append("""<header class="top"><img src="img/simreal-logo-ink.png" alt="SimReal">
<div class="meta"><span class="label">Internal · Fundraising</span><b>融资与资源手册 · 2026 年 10 月</b></div></header>
<div class="hero"><span class="label">Cold email first</span>
<h1>先冷邮件：<em>按 Luke Sophinos 的方法融资</em>，再加上这个阶段能争取的所有资源</h1>
<p>第一部分把 Sophinos 的三阶段冷邮件方法用到我们身上：找投资人、拿到第一次会议、推进融资，写清已经做完什么、下一步做什么。第二部分整理了这个阶段能争取的资源和渠道，来自 Reddit、Hacker News、X 上创业者的讨论和官方页面，重要的已逐项复核截止时间、金额和申请条件。</p></div>""")
    cap_n = len(cap["investors"]) if cap else 0
    h.append(f"""<div class="stats">
<div class="stat"><span class="n">{n_inv + cap_n}</span><span class="d">投资人进表<br>已有 {n_inv} 家 + 同类公司反查 {cap_n} 家</span></div>
<div class="stat"><span class="n" style="font-size:18pt">{len(groups[1])} · {len(groups[2])} · {len(groups[3])}</span><span class="d">C / B / A 组<br>从 C 组先发，A 组最后发</span></div>
<div class="stat"><span class="n">{len(items)}</span><span class="d">项资源和渠道<br>其中 {verified} 项已复核</span></div>
<div class="stat"><span class="n hot">10/4</span><span class="d">PearX W27 截止<br>太平洋时间 23:59，迟交到 10/8</span></div></div>""")
    h.append("""<div class="summary"><h2>一页看懂</h2><ol>
<li><b>方法：</b>融资就是销售，关键是给谁发、怎么发。先从同类公司的融资记录里找投资人，做成 300–400 人的表，每人回答四个问题；每封邮件五段；从最不匹配的 C 组发起，边发边改，最匹配的 A 组最后发。</li>
<li><b>已经做完：</b>148 封投资人邮件改成五段式；按匹配度分好 C / B / A 组；邮件里放 BP 链接（审批页"发件信息"里填一次，所有邮件自动替换）。</li>
<li><b>这周要做：</b>备好 BP 链接（用能看打开数据的分享方式）；装 Mailtrack 一类的打开追踪；从 C 组开始发，每天不超过 30 封。</li>
<li><b>近期截止：</b>PearX 10/4（迟交 10/8）；a16z speedrun 优先窗口 10/12–11/1；YC W27 11/2；深圳语料券 11/10；Innovate UK Frontier AI 11/11；NeurIPS 12/6 起。</li>
<li><b>需要你定：</b>查邮箱用不用 Hunter.io（见 2.2）；公司主体放在哪个国家（影响英国、美国、国内项目的资格）。</li>
</ol></div>""")

    # Part 1 – phase 1
    h.append("""<section class="chapter"><div class="chapter-head"><span class="label">Part 1 · Phase 1</span>
<h2>阶段 1：找到投资人</h2><p>方法：以自己的产品为起点，找出同类公司，逐家查它们的投资人，汇总成名单。投过同类公司的投资人已经认可这个赛道，更愿意投同一领域里不直接竞争的项目。</p></div>""")
    if cap:
        h.append(f"<p>我们反查了 {len(cap['companies'])} 家同类公司（专家数据、RL 环境、评测、后训练平台，以及国内的数据公司），"
                 f"从公开融资公告里找到 {cap['rounds']} 轮融资、{len(cap['investors'])} 家此前不在名单里的投资人。下表是投过同类公司最多的投资人。</p>")
        h.append('<table class="res"><thead><tr><th>投资人</th><th>投过的同类公司</th><th style="width:22mm">领投次数</th><th style="width:30mm">出现过的轮次</th></tr></thead><tbody>')
        for inv in cap["top"]:
            h.append(f'<tr><td>{e(inv["name"])}</td><td>{e("、".join(inv["companies"]))}</td><td>{inv["leads"]}</td><td>{e("、".join(inv["stages"]))}</td></tr>')
        h.append("</tbody></table>")
        h.append(f'<p class="fine">完整名单在 collateral/SimReal-投资人总表.xlsx。没找到融资信息的公司：{e("、".join(cap["notFound"]) or "无")}。</p>')
    else:
        h.append("<p>同类公司反查正在进行，完成后补进本节和投资人总表。</p>")
    h.append("""<div class="note"><p><b>和原方法的差别：</b>原方法用 Crunchbase 的 financials 页面查投资人。这里打不开 Crunchbase，改用公开的融资公告和新闻，每条都附来源。有 Crunchbase Pro 账号的话，可以再补漏。</p>
<p><b>投过直接竞品的投资人</b>（如 Mercor、Fleet、Halluminate 的股东）不排除。他们最懂这个赛道，但可能有冲突，邮件开场要讲清我们和那家公司的差别（金融方向、量化团队、自有专家）。</p></div></section>""")

    # Phase 2
    h.append("""<section class="chapter"><div class="chapter-head"><span class="label">Part 1 · Phase 2</span>
<h2>阶段 2：拿到第一次会议</h2><p>五步：做投资人表、找邮箱、写五要素邮件、分组发送、追踪并迭代。</p></div>
<h3><span class="no">2.1</span>投资人表：每人回答四个问题</h3>
<ol class="num"><li>通常投哪一轮（种子、A 轮还是更后）？</li><li>典型支票多大？</li><li>领投还是跟投？</li><li>投过哪些同类公司？</li></ol>
<p>投资人的投资论点通常围绕特定市场。投过 RL 环境、专家数据、评测公司的人，更可能对整个领域感兴趣。表里每家都标了 C / B / A 组，审批页上的卡片按同样的组排序。</p>
<h3><span class="no">2.2</span>找邮箱</h3>
<p>原方法用 Hunter.io 批量查邮箱。我们之前定的规则是：只用本人或所在机构公开发布的地址，不按格式猜，不用数据经纪网站。Hunter.io 的地址大多是按格式推出来的，和这条规则冲突，所以没有用。</p>
<div class="callout"><p><b>建议：</b>保留原规则。冷邮件被退回或进垃圾箱，会伤到 business@simreal.co 这个域名的发信信誉，之后发给客户和伙伴的邮件也会受影响。如果决定用 Hunter.io，只用它标为已验证（verified）的地址，填到审批页卡片的"自己查到的邮箱"里，并控制每天发送量。</p></div>
<h3><span class="no">2.3</span>五要素邮件（已用于全部 148 封）</h3>""")
    h.append('<div class="tpl">' + "".join(
        f'<div class="row"><div class="k">{e(k)}</div><div class="v{" subj" if subj else ""}">{e(v)}</div></div>' for k, v, subj in email_rows()) + "</div>")
    h.append("""<p class="fine">原方法的例子：开场引用对方的播客观点；能力写 Thiel Fellow、Forbes 30 under 30 和已有的软承诺；公司用一句话讲清；进展写三个月内招到的人和 beta 用户数；最后请求一次短会。我们对应写的是：针对这家的开场、量化团队背景、一句话产品、Xitadel 结果和 Surge AI / AfterQuery 合作、2,000 万美元种子轮加 BP 链接和约 20 分钟。中文邮件结构相同。</p>
<h3><span class="no">2.4</span>分组发送：C → B → A</h3>""")
    g = groups
    def names(rows, k=14):
        return "、".join(r["名称"] for r in rows[:k]) + ("等" if len(rows) > k else "")
    h.append(f"""<div class="groups">
<div><span class="n">{len(g[1])}</span><span class="t">C 组：第 1 周</span><span class="d">匹配度相对低：战略投资部门、亚洲综合基金、后期为主的机构、间接相关的天使。用来练手和收集反馈。</span></div>
<div><span class="n">{len(g[2])}</span><span class="t">B 组：第 2 周</span><span class="d">方向对：投过数据或评测公司的种子基金、量化机构的投资部门、相关的天使。</span></div>
<div><span class="n">{len(g[3])}</span><span class="t">A 组：第 3 周</span><span class="d">最匹配、最想拿下：投过 RL 环境 / 专家数据 / 评测、能领投种子轮的基金。</span></div>
<div><span class="n">{len(g[9])}</span><span class="t">暂缓</span><span class="d">已投直接竞品、只投后期，或很难接触到的。</span></div></div>
<p class="names"><b>A 组：</b>{e(names(g[3], 30))}</p>
<p class="names"><b>B 组举例：</b>{e(names(g[2]))}</p>
<p class="names"><b>C 组举例：</b>{e(names(g[1]))}</p>
<p>原因：pitch 会随着反馈越改越好，不要一上来就打最想拿下的基金。每组发完看回复，改开场和 BP，再发下一组。跟进在第 5 天和第 12 天，模板在审批页每张卡片里。</p>
<h3><span class="no">2.5</span>追踪与迭代</h3>
<ul class="plain"><li><b>邮件打开：</b>在 Gmail 装 Mailtrack 一类的插件，看谁打开了、打开了几次。</li>
<li><b>BP 阅读：</b>用 DocSend、Papermark 这类能看阅读数据的链接，知道对方看了哪几页、看了多久。</li>
<li><b>每周复盘：</b>打开率低就改主题；打开了但不回复就改开场和进展那两段；哪类开场回复多，下一组就多用。</li></ul>
</section>""")

    # Phase 3
    h.append("""<section class="chapter flow"><div class="chapter-head"><span class="label">Part 1 · Phase 3</span>
<h2>阶段 3：推进融资</h2><p>任何投资人电话之前，先把 BP 准备好。</p></div>
<ul class="plain"><li><b>BP：</b>原方法推荐研究 Airbnb 的种子轮 BP。我们的 BP 已经有了（Delta1 仓库）。发出去之前压到 10–12 页，用可追踪的链接分享，不用附件。</li>
<li><b>首次电话（20–30 分钟）：</b>两分钟讲清我们做什么、为什么现在、为什么是我们；然后讲 Xitadel 的结果和已有合作；留一半时间回答问题。</li>
<li><b>资料室：</b>Xitadel 运行记录和复现说明、合作方证明、团队简历、股权结构，对方要时当天能发。</li>
<li><b>节奏：</b>首次会议尽量排在两到三周内，进展更新同步发给所有在谈的投资人。融资就是销售，管道越满，谈判越主动。</li></ul>
<h3><span class="no">3.1</span>线程推荐的四份免费投资人名单（合计 1,000+ 家）</h3>
<table class="res"><thead><tr><th>名单</th><th>内容</th></tr></thead><tbody>
<tr><td>Matt Estes</td><td>750 家种子基金的表格</td></tr>
<tr><td>Shai Goldman</td><td>219 家早期 VC 的 Airtable</td></tr>
<tr><td>Trace Cohen</td><td>500 家美国活跃投资人的表格</td></tr>
<tr><td>Yuliya Bel</td><td>愿意接受冷接触的投资人名单</td></tr></tbody></table>
<p class="fine">这几份名单是 2022 年整理的，链接在原线程里；本环境打不开，没能核对。可以用来补漏和交叉检查，查到的新基金同样按四个问题和 C / B / A 分组；邮箱仍按 2.2 的规则处理。</p></section>""")

    # Part 2 – calendar
    h.append("""<section class="chapter"><div class="chapter-head"><span class="label">Part 2 · Calendar</span>
<h2>年底前的截止时间</h2><p>只列适合度高和中的项目。"更正"表示复核时改过日期或条件。</p></div>
<table class="res"><thead><tr><th style="width:22mm">截止</th><th>项目</th><th>给什么</th><th style="width:16mm">适合度</th></tr></thead><tbody>""")
    for r in soon:
        h.append(f'<tr><td class="num">{e(r["_deadline"])}</td><td>{e(r["name"])}</td><td>{e(short(r["offer"], 90))}</td><td>{e(r["fit"])}</td></tr>')
    h.append("</tbody></table></section>")

    # Part 2 – categories
    h.append(f"""<section class="chapter"><div class="chapter-head"><span class="label">Part 2 · Resources</span>
<h2>海外资源与渠道（按类别）</h2><p>适合度高和中、还没截止的项目，按状态和截止时间排。完整的 {len(items)} 项在 collateral/SimReal-资源与渠道清单.xlsx。</p></div>""")
    for cat in CAT_ORDER:
        rows = sorted([r for r in overseas if r["category"] == cat and r["fit"] != "低" and r["status"] != "已截止"], key=order)
        if not rows:
            continue
        h.append(f'<div class="cat"><h3>{e(cat)}<span class="no">{len(rows)} 项</span></h3>{resource_table(rows)}</div>')
    h.append("</section>")

    h.append("""<section class="chapter"><div class="chapter-head"><span class="label">Part 2 · China &amp; Hong Kong</span>
<h2>国内与香港</h2><p>需要在国内或香港有主体才能申请的项目。语料券、算力券和数据交易所对做数据的公司特别有用。</p></div>""")
    h.append(resource_table(china))
    h.append("</section>")

    # Tactics
    h.append("""<section class="chapter"><div class="chapter-head"><span class="label">Part 2 · From founders</span>
<h2>创业者经验（Reddit、Hacker News、X）</h2><p>每类挑两条，完整 101 条在清单的"社区经验"表。</p></div><table class="res"><thead><tr><th style="width:22mm">类别</th><th style="width:44mm">做法</th><th>说明</th></tr></thead><tbody>""")
    seen = {}
    for t in data.get("tactics", []):
        c = t.get("category", "")
        if seen.get(c, 0) >= 2:
            continue
        seen[c] = seen.get(c, 0) + 1
        h.append(f'<tr><td>{e(TACTIC_CAT.get(c, c))}</td><td>{e(t["tactic"])}</td><td>{e(short(t["detail"], 140))}</td></tr>')
    h.append("</tbody></table>")
    h.append(f"""<h3>不建议优先做的（{len(later)} 项）</h3><p class="names">{e("、".join(r["name"] for r in later))}</p>
<p class="fine">这些项目适合度低或已经截止，原因写在清单里。</p>
<div class="sources"><h4 style="margin-top:6mm">方法与来源</h4>
<p>冷邮件方法：Luke Sophinos 2022 年 10 月的 X 线程（x.com/lukesophinos/status/1580241908156092417），内容按你整理的摘要。资源来自 8 个方向的检索（加速器、资助、算力与福利、投资人渠道、社区与活动、曝光平台、销售渠道、国内项目），每项的来源链接在清单里；适合度高或近期开放的 {len([r for r in items if r.get("verdict") in ("确认", "更正", "未复核")])} 项中，{verified} 项由第二个调研员复核过。本环境打不开 Reddit、X 和多数官网，信息来自搜索结果摘要，申请前请点开官方链接再确认一次。日期以 2026-10-02 为准。</p></div>
<div class="end"><img src="img/simreal-mark-ink.png" alt=""><div><b>SimReal</b><span>business@simreal.co · simreal.co</span></div></div>
</section></body></html>""")
    OUT.write_text("".join(h), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
