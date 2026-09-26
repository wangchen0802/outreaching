"""Merge the investor research into intel/vc-funds.csv and intel/vc-deals.csv.

Adds 分段 (海外/国内), 优先级 and 优先级理由 from intel/vc-priority.json.
Usage: python3 tools/vc_merge.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTEL = ROOT / "intel"
SEGMENTS = {"vc-overseas": "海外", "vc-china": "国内"}


def main():
    prio = json.loads((INTEL / "vc-priority.json").read_text(encoding="utf-8"))
    rank = {}
    for seg in ("海外", "国内"):
        for i, (name, why) in enumerate(prio[seg], 1):
            rank[name] = (i, why)
    caution = {name: why for name, why in prio.get("谨慎", [])}

    funds, seen, cols = [], set(), None
    for seg, label in SEGMENTS.items():
        with open(INTEL / f"{seg}-funds.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            cols = cols or reader.fieldnames
            for r in reader:
                key = r["投资方"].strip().lower()
                if key in seen:
                    continue
                seen.add(key)
                r["分段"] = label
                r["优先级"], r["优先级理由"] = rank.get(r["投资方"], ("", ""))
                r["谨慎"] = caution.get(r["投资方"], "")
                funds.append(r)
    missing = [n for n in list(rank) + list(caution) if n.lower() not in seen]
    if missing:
        raise SystemExit(f"priority names not found in funds: {missing}")
    funds.sort(key=lambda r: (r["分段"] != "海外", r["优先级"] == "", r["优先级"] or 99))
    with open(INTEL / "vc-funds.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["分段", "优先级", "优先级理由", "谨慎"] + cols)
        w.writeheader()
        w.writerows(funds)

    deals, dseen, dcols = [], set(), None
    for seg, label in SEGMENTS.items():
        with open(INTEL / f"{seg}-deals.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            dcols = dcols or reader.fieldnames
            for r in reader:
                key = (r["被投公司"].strip().lower(), r["轮次"].strip(), r["日期"].strip())
                if key in dseen:
                    continue
                dseen.add(key)
                r["分段"] = label
                deals.append(r)
    with open(INTEL / "vc-deals.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["分段"] + dcols)
        w.writeheader()
        w.writerows(deals)
    print(f"{len(funds)} funds, {len(deals)} deals")


if __name__ == "__main__":
    main()
