"""Merge the per-segment vendor-claims research into one dataset and a buyer index.

Inputs:  intel/<segment>-claims.csv, intel/<segment>-vendors.csv (see ops/intel-brief.md)
Outputs: intel/claims.csv   all claims, names normalised, exact duplicates removed
         intel/vendors.csv  one row per vendor
         intel/buyers.md    reverse index: each customer, which vendors claim it, for what,
                            and whether it is already on prospects.csv

Usage: python3 tools/intel_merge.py
"""
import collections
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTEL = ROOT / "intel"

CLAIM_COLS = ["供应商", "客户或合作方", "客户类型", "关系类型", "工作内容或领域", "原文证据", "来源链接", "来源日期", "来源类型", "置信度"]
VENDOR_COLS = ["供应商", "类型", "规模", "地区", "官网", "简介", "主要领域", "收录声明数"]

# Canonical name -> aliases (matched case-insensitively as whole names or leading words).
ALIASES = {
    "OpenAI": ["openai", "chatgpt"],
    "Anthropic": ["anthropic", "claude"],
    "Google DeepMind": ["google deepmind", "deepmind", "google", "gemini", "google research", "google cloud"],
    "Meta": ["meta", "meta ai", "meta superintelligence labs", "msl", "facebook", "llama"],
    "xAI": ["xai", "spacexai", "grok", "x.ai"],
    "Microsoft": ["microsoft", "microsoft ai", "msft"],
    "Amazon": ["amazon", "aws", "amazon agi", "amazon nova"],
    "Apple": ["apple"],
    "NVIDIA": ["nvidia", "nemotron"],
    "Cohere": ["cohere"],
    "Mistral AI": ["mistral", "mistral ai"],
    "Reflection AI": ["reflection", "reflection ai"],
    "Thinking Machines Lab": ["thinking machines", "thinking machines lab"],
    "IBM": ["ibm", "granite"],
    "Ai2": ["ai2", "allen institute", "allen institute for ai", "allenai"],
    "字节跳动": ["字节跳动", "字节", "bytedance", "seed", "豆包", "doubao", "火山引擎", "volcengine"],
    "阿里巴巴": ["阿里巴巴", "阿里", "alibaba", "qwen", "通义", "通义千问", "阿里云"],
    "腾讯": ["腾讯", "tencent", "混元", "hunyuan"],
    "百度": ["百度", "baidu", "文心", "ernie"],
    "月之暗面": ["月之暗面", "moonshot", "moonshot ai", "kimi"],
    "智谱": ["智谱", "zhipu", "z.ai", "glm", "智谱ai"],
    "DeepSeek": ["deepseek", "深度求索", "幻方"],
    "MiniMax": ["minimax", "稀宇"],
    "阶跃星辰": ["阶跃星辰", "阶跃", "stepfun"],
    "华为": ["华为", "huawei", "盘古"],
    "小米": ["小米", "xiaomi", "mimo"],
    "商汤": ["商汤", "sensetime"],
    "科大讯飞": ["科大讯飞", "讯飞", "iflytek"],
    "百川智能": ["百川", "百川智能", "baichuan"],
    "美团": ["美团", "meituan", "longcat"],
    "快手": ["快手", "kuaishou"],
    "京东": ["京东", "jd"],
}
_ALIAS_INDEX = {a: canon for canon, al in ALIASES.items() for a in al + [canon.lower()]}


def canon(name):
    n = re.sub(r"\s+", " ", (name or "").strip())
    key = n.lower()
    if key in _ALIAS_INDEX:
        return _ALIAS_INDEX[key]
    # "Google (Gemini team)" / "Meta（MSL）" -> look at the part before a bracket.
    head = re.split(r"[（(/,，]", key)[0].strip()
    return _ALIAS_INDEX.get(head, n)


def read_csv(path, cols):
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [{c: (r.get(c) or "").strip() for c in cols} for r in rows]


def prospect_names():
    names = set()
    p = ROOT / "prospects.csv"
    if p.exists():
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                names.add(canon(r["公司"]))
                names.add(canon(r["公司"].split(" ")[0]))
    return names


def main():
    claim_files = sorted(f for f in INTEL.glob("*-claims.csv"))
    vendor_files = sorted(f for f in INTEL.glob("*-vendors.csv"))
    if not claim_files:
        raise SystemExit("no intel/*-claims.csv files yet")

    claims, seen = [], set()
    for f in claim_files:
        segment = f.name[: -len("-claims.csv")]
        for r in read_csv(f, CLAIM_COLS):
            r["供应商"] = canon(r["供应商"])
            r["客户或合作方"] = canon(r["客户或合作方"])
            key = (r["供应商"].lower(), r["客户或合作方"].lower(), r["来源链接"])
            if key in seen or not r["客户或合作方"]:
                continue
            seen.add(key)
            r["分段"] = segment
            claims.append(r)

    vendors = {}
    for f in vendor_files:
        for r in read_csv(f, VENDOR_COLS):
            name = canon(r["供应商"])
            r["供应商"] = name
            old = vendors.get(name)
            # Keep the row with the most filled-in fields.
            if old is None or sum(bool(v) for v in r.values()) > sum(bool(v) for v in old.values()):
                vendors[name] = r
    per_vendor = collections.Counter(c["供应商"] for c in claims)
    for name, n in per_vendor.items():
        vendors.setdefault(name, {c: "" for c in VENDOR_COLS} | {"供应商": name})
    for name, r in vendors.items():
        r["收录声明数"] = str(per_vendor.get(name, 0))

    with open(INTEL / "claims.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CLAIM_COLS + ["分段"])
        w.writeheader()
        w.writerows(sorted(claims, key=lambda c: (c["客户或合作方"], c["供应商"])))
    with open(INTEL / "vendors.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=VENDOR_COLS)
        w.writeheader()
        w.writerows(sorted(vendors.values(), key=lambda v: -int(v["收录声明数"] or 0)))

    # Reverse index: customer -> vendors.
    rank = {"高": 3, "中": 2, "低": 1}
    by_cust = collections.defaultdict(list)
    for c in claims:
        if c["供应商"] == "未具名供应商" or c["关系类型"] == "投资方":
            continue
        by_cust[c["客户或合作方"]].append(c)
    on_list = prospect_names()

    def summary(rows):
        vend = collections.OrderedDict()
        for r in sorted(rows, key=lambda r: -rank.get(r["置信度"], 0)):
            vend.setdefault(r["供应商"], r)
        # A vendor whose only link is a change (e.g. paused work) is labelled, not counted as current.
        labels = [v + ("（变动）" if r["关系类型"].startswith("客户变动") else "") for v, r in vend.items()]
        current = sum(1 for r in vend.values() if not r["关系类型"].startswith("客户变动"))
        best = max(rank.get(r["置信度"], 0) for r in rows)
        domains = "；".join(sorted({r["工作内容或领域"] for r in rows if r["工作内容或领域"]}))[:160]
        types = "、".join(sorted({r["客户类型"] for r in rows if r["客户类型"]}))
        return labels, current, best, domains, types

    unnamed = collections.Counter(c["客户或合作方"] for c in claims if c["供应商"] == "未具名供应商")
    lines = ["# 买方反向索引", "",
             f"由 tools/intel_merge.py 从 {len(claim_files)} 个分段、{len(claims)} 条公开声明生成。"
             "「供应商数」只算点名的供应商；置信度取该客户所有声明里最高的一条。", ""]
    lines += ["## 全部买方（按点名的现有供应商数排序）", "",
              "| 客户 | 类型 | 现有供应商数 | 点名的供应商 | 采购内容 | 最高置信度 | 在我们名单上 |", "|---|---|---|---|---|---|---|"]
    summaries = {cust: summary(rows) for cust, rows in by_cust.items()}
    ordered = sorted(summaries.items(), key=lambda kv: (-kv[1][1], kv[0]))
    new_prospects = []
    for cust, (labels, current, best, domains, types) in ordered:
        listed = "是" if cust in on_list else ""
        best_s = {3: "高", 2: "中", 1: "低"}.get(best, "")
        lines.append(f"| {cust} | {types} | {current} | {'、'.join(labels)} | {domains} | {best_s} | {listed} |")
        if not listed and best >= 2:
            new_prospects.append((cust, types, current, "、".join(labels), domains))
    lines += ["", "## 不在我们名单上的买方（至少一条中或高置信度声明）", "",
              "| 客户 | 类型 | 现有供应商数 | 点名的供应商 | 采购内容 |", "|---|---|---|---|---|"]
    lines += [f"| {c} | {t} | {n} | {v} | {d} |" for c, t, n, v, d in new_prospects]
    if unnamed:
        lines += ["", "## 公开承认向外采购、但没点名供应商的买方", ""]
        lines += [f"- {c}（{n} 条）" for c, n in unnamed.most_common()]
    (INTEL / "buyers.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(claims)} claims, {len(vendors)} vendors, {len(by_cust)} buyers, {len(new_prospects)} new prospects")


if __name__ == "__main__":
    main()
