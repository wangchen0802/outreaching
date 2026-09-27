"""Build approval-page documents from the lists and drafts.

Writes one JSON file per recipient to OUT_DIR (default: build/db/), shaped as the
`prospects/<id>` documents the approval page reads. Ids: customers use the slug,
partners "p-<slug>", investors "v-<slug>". Review and send state are not included:
the page owns them. Pass --with-review to add a fresh `review: {status: "pending"}`
(use it only when creating documents).

Lists: customers come from prospects.csv (matched by company name), partners from
lists/partners.csv and investors from lists/investors.csv (matched by slug).

Usage: python3 tools/build_db.py [--out DIR] [--with-review] [--revision N] [id ...]
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import drafts  # noqa: E402
import templates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREFIX = {"customer": "", "partner": "p-", "investor": "v-"}
TRACK_BASE = {"partner": 1000, "investor": 2000, "customer": 3000}

CATEGORY_ORDER = [
    ("frontier lab", 1),
    ("国内大模型公司", 2),
    ("人类数据", 3), ("专家网络", 3),
    ("RL 环境", 4), ("评测", 5),
    ("垂直 AI", 4),
    ("金融机构", 5),
    ("咨询公司", 5),
]


def category_rank(category):
    for prefix, rank in CATEGORY_ORDER:
        if category.startswith(prefix):
            return rank
    return 9


def read_csv(path):
    p = ROOT / path
    if not p.exists():
        return []
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def split_sources(s):
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "build" / "db"))
    ap.add_argument("--with-review", action="store_true")
    ap.add_argument("--revision", type=int, default=None)
    ap.add_argument("ids", nargs="*")
    args = ap.parse_args()

    customers = {r["公司"]: r for r in read_csv("prospects.csv")}
    lists = {"partner": read_csv("lists/partners.csv"), "investor": read_csv("lists/investors.csv")}
    by_slug = {tr: {r["slug"]: (i, r) for i, r in enumerate(rows)} for tr, rows in lists.items()}

    t = templates.load()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    written = []
    for track, path in drafts.all_paths():
        doc_id = PREFIX[track] + path.stem
        if args.ids and doc_id not in args.ids:
            continue
        d = drafts.parse(path)
        email = d["parts"]["email"]
        lang = drafts.lang_of(email)
        f = drafts.extract_fills(track, email, t)
        if f is None:
            raise SystemExit(f"{path}: email does not match the template; run tools/check_drafts.py")
        subject_line, body = email.split("\n", 1)
        subject = subject_line.split(":", 1)[1].strip() if lang == "en" else subject_line.split("：", 1)[1].strip()
        body = body.strip()
        salutation = body.split("\n\n", 1)[0].strip()
        hook = f.get("[Hook]") or f.get("[合作句]") or f.get("[投资句]") or ""

        if track == "customer":
            row = customers.get(d["title"]) or next(
                (r for k, r in customers.items() if k.startswith(d["title"]) or d["title"].startswith(k)), None)
            if row is None:
                raise SystemExit(f"{path}: no prospects.csv row for '{d['title']}'")
            company, category, region = row["公司"], row["类别"], row["地区"]
            order = TRACK_BASE[track] + category_rank(category) * 100 + (0 if region == "海外" or region.startswith("海外") else 50)
        else:
            hit = by_slug[track].get(path.stem)
            if hit is None:
                raise SystemExit(f"{path}: no lists/{track}s.csv row with slug '{path.stem}'")
            i, row = hit
            company, category, region = row["名称"], row["类型"], row["地区"]
            order = TRACK_BASE[track] + i
        days = templates.FOLLOWUP_DAYS[track]
        doc = {
            "slug": doc_id,
            "track": track,
            "company": company,
            "category": category,
            "region": "海外" if region.startswith("海外") else ("国内" if region.startswith("国内") else region),
            "contact": row.get("联系人", ""),
            "role": row.get("职位", ""),
            "sources": split_sources(row.get("来源链接") or row.get("联系人来源")),
            "angle": row.get("切入点", ""),
            "confidence": row.get("置信度", ""),
            "to": "" if row.get("邮箱", "未找到") in ("", "未找到") else row["邮箱"].strip(),
            "toSource": row.get("邮箱来源", ""),
            "channel": "" if row.get("备用渠道", "") in ("", "未找到") else row["备用渠道"],
            "order": order,
            "updatedAt": now,
            "lang": lang,
            "subject": subject,
            "body": body,
            "salutation": salutation,
            "opening": hook,
            "domains": "",
            "followups": [{"day": days[0], "text": d["parts"]["fu1"]}, {"day": days[1], "text": d["parts"]["fu2"]}],
            "wechat": d["parts"].get("wechat", ""),
            "dm": d["parts"].get("dm", ""),
            "meta_md": d["meta_md"],
            "notes_md": d["notes_md"],
        }
        if args.revision is not None:
            doc["revision"] = args.revision
        if args.with_review:
            doc["revision"] = doc.get("revision", 1)
            doc["review"] = {"status": "pending", "comment": "", "at": None, "forRevision": doc["revision"]}
        (out / f"{doc_id}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        written.append(doc_id)
    print(f"wrote {len(written)} docs to {out}")


if __name__ == "__main__":
    main()
