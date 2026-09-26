"""Build approval-page documents from prospects.csv and drafts/*.md.

Writes one JSON file per company to OUT_DIR (default: build/db/), shaped as the
`prospects/<slug>` documents the approval page reads. Review state is not
included: the page owns it. Pass --with-review to add a fresh
`review: {status: "pending"}` (use it only when creating documents).

Usage: python3 tools/build_db.py [--out DIR] [--with-review] [--revision N] [slug ...]
"""
import argparse
import csv
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

CATEGORY_ORDER = [
    ("frontier lab", 1),
    ("国内大模型公司", 2),
    ("人类数据供应商", 3),
    ("垂直 AI", 4),
    ("金融机构", 5),
    ("咨询公司", 5),
]

def category_rank(category):
    for prefix, rank in CATEGORY_ORDER:
        if category.startswith(prefix):
            return rank
    return 9


def parse_draft(path):
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    meta_md = text.split("\n", 1)[1].split("## 调研备注", 1)[0].strip()
    notes_md = text.split("## 调研备注", 1)[1].split("\n---\n", 1)[0].strip()
    email = text.split("## 邮件", 1)[1].split("\n---\n", 1)[0].strip()
    wechat = ""
    if "## 微信版（引荐后）" in text:
        wechat = text.split("## 微信版（引荐后）", 1)[1].strip()

    lang = "en" if email.startswith("Subject:") else "zh"
    subject_line, body = email.split("\n", 1)
    subject = subject_line.split(":", 1)[1].strip() if lang == "en" else subject_line.split("：", 1)[1].strip()
    body = body.strip()
    paragraphs = body.split("\n\n")
    salutation = paragraphs[0].strip()
    # Template v2: greeting, intro, credentials, then the paragraph that opens with the per-company hook.
    coop = paragraphs[3].strip()
    marker = " I'd like to understand" if lang == "en" else "想了解贵司"
    opening = coop.split(marker, 1)[0].strip()
    domains = ""
    return {
        "title": title,
        "lang": lang,
        "subject": subject,
        "body": body,
        "salutation": salutation,
        "opening": opening,
        "domains": domains,
        "wechat": wechat,
        "meta_md": meta_md,
        "notes_md": notes_md,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "build" / "db"))
    ap.add_argument("--with-review", action="store_true")
    ap.add_argument("--revision", type=int, default=None)
    ap.add_argument("slugs", nargs="*")
    args = ap.parse_args()

    rows = {}
    with open(ROOT / "prospects.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows[row["公司"]] = row

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    written = []
    for path in sorted((ROOT / "drafts").glob("*.md")):
        slug = path.stem
        if args.slugs and slug not in args.slugs:
            continue
        d = parse_draft(path)
        row = rows.get(d["title"])
        if row is None:
            # Draft titles and CSV company names should match; fall back to a prefix match.
            row = next((r for k, r in rows.items() if k.startswith(d["title"]) or d["title"].startswith(k)), None)
        if row is None:
            raise SystemExit(f"{slug}: no prospects.csv row for '{d['title']}'")
        doc = {
            "slug": slug,
            "company": row["公司"],
            "category": row["类别"],
            "region": row["地区"],
            "contact": row["联系人"],
            "role": row["职位"],
            "sources": [s.strip() for s in row["来源链接"].split(";") if s.strip()],
            "angle": row["切入点"],
            "confidence": row["置信度"],
            "order": category_rank(row["类别"]) * 100 + (0 if row["地区"] == "海外" else 50),
            "updatedAt": now,
            **{k: v for k, v in d.items() if k != "title"},
        }
        if args.revision is not None:
            doc["revision"] = args.revision
        if args.with_review:
            doc["revision"] = doc.get("revision", 1)
            doc["review"] = {"status": "pending", "comment": "", "at": None, "forRevision": doc["revision"]}
        (out / f"{slug}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        written.append(slug)
    print(f"wrote {len(written)} docs to {out}: {', '.join(written)}")


if __name__ == "__main__":
    main()
