"""Build intel/page/index.html from intel/claims.csv, intel/vendors.csv and intel/findings.json.

Usage: python3 tools/build_intel_page.py
"""
import csv
import hashlib
import json
import re
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from intel_merge import canon, is_unnamed, prospect_names  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTEL = ROOT / "intel"


def anchor(name):
    """ASCII anchor for a buyer (the artifact viewer only passes [A-Za-z0-9._~-] hashes)."""
    a = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if len(a) < 2 or re.search(r"[^\x00-\x7f]", name):
        a = (a + "-" if len(a) >= 2 else "") + hashlib.md5(name.encode("utf-8")).hexdigest()[:6]
    return "b-" + a


def main():
    claims = []
    with open(INTEL / "claims.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            claims.append({
                "vendor": r["供应商"], "buyer": r["客户或合作方"], "btype": r["客户类型"], "rel": r["关系类型"],
                "what": r["工作内容或领域"], "quote": r["原文证据"], "url": r["来源链接"], "date": r["来源日期"],
                "stype": r["来源类型"], "conf": r["置信度"], "unnamedBuyer": is_unnamed(r["客户或合作方"]),
            })
    vendors = []
    with open(INTEL / "vendors.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            vendors.append({"name": r["供应商"], "type": r["类型"], "size": r["规模"], "region": r["地区"],
                            "about": r["简介"], "fields": r["主要领域"], "n": r["收录声明数"]})
    data = {
        "asOf": "2026-09-25",
        "claims": claims,
        "vendors": vendors,
        "onList": sorted(prospect_names()),
        "findings": json.loads((INTEL / "findings.json").read_text(encoding="utf-8")),
        "ids": {c["buyer"]: anchor(c["buyer"]) for c in claims},
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tpl = (INTEL / "page" / "template.html").read_text(encoding="utf-8")
    out = INTEL / "page" / "index.html"
    out.write_text(tpl.replace("__DATA__", blob), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(claims)} claims, {len(vendors)} vendors)")


if __name__ == "__main__":
    main()
