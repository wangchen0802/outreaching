"""Derive prospects.csv rows from draft headers for drafts that have no row yet.

Prints the rows for review; with --write appends them to prospects.csv.
"""
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_db import parse_draft  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = re.compile(r"https?://[^\s）)，、；]+")


def bullet(meta, key):
    m = re.search(r"^- " + key + r"[^：:]*[：:](.*)$", meta, re.M)
    return m.group(1).strip() if m else ""


def block(meta, key):
    """A top-level bullet plus its indented sub-bullets."""
    m = re.search(r"^- " + key + r"[^\n]*(?:\n(?:  +- |  +)[^\n]*)*", meta, re.M)
    return m.group(0) if m else ""


def sentences(text, limit=180):
    out = ""
    for piece in re.split(r"(?<=[。；])", text):
        if out and len(out) + len(piece) > limit:
            break
        out += piece
    return out.strip()


def first_bullet_after(notes, heading):
    part = notes.split(heading, 1)
    if len(part) < 2:
        return ""
    m = re.search(r"^- (.+)$", part[1], re.M)
    return m.group(1).strip() if m else ""


def row_for(path):
    d = parse_draft(path)
    meta = d["meta_md"]
    cat_line = bullet(meta, "类别")
    category, _, region_part = cat_line.partition("｜")
    region = "海外" if "海外" in region_part else "国内"
    rec = bullet(meta, "收件人")
    m = re.match(r"\*\*(.+?)\*\*[，,]?\s*(.*)", rec)
    contact, role = (m.group(1), m.group(2)) if m else (rec, "")
    role = re.split(r"[。；]", role)[0].strip()
    fallback = "（兜底）" in meta.split("\n", 3)[1] if "收件人（兜底）" in meta else False
    if fallback or "兜底" in rec:
        role = (role + "（备选联系人，数据负责人未找到）").strip()
    conf_line = bullet(meta, "置信度")
    conf = next((c for c in conf_line if c in "高中低"), "中")
    # A fallback contact is at best 中 for "is this the right person".
    if (fallback or "兜底" in rec) and conf == "高":
        conf = "中"
    urls = URL.findall(block(meta, "来源")) or URL.findall(block(meta, "收件人")) or URL.findall(block(meta, "置信度"))
    urls = [u.rstrip(".。") for u in urls][:3]
    angle = first_bullet_after(d["notes_md"], "**切入点**")
    angle = re.sub(r"\*\*", "", angle)
    angle = URL.sub("", angle).strip("：:，, ")
    return [d["title"], category.strip(), region, contact, role, " ; ".join(urls) or "未找到", sentences(angle), conf]


def main():
    existing = set()
    with open(ROOT / "prospects.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            existing.add(r["公司"])
    rows = []
    for p in sorted((ROOT / "drafts").glob("*.md")):
        title = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        if title in existing:
            continue
        rows.append(row_for(p))
    for r in rows:
        print(" | ".join(r))
        print()
    if "--write" in sys.argv:
        with open(ROOT / "prospects.csv", "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)
        print(f"appended {len(rows)} rows")


if __name__ == "__main__":
    main()
