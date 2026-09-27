"""Read and write draft files (drafts/, drafts/partners/, drafts/investors/).

A draft is: '# title', header bullets, '## 调研备注', then sections separated by
'\n---\n': '## 邮件', '## 跟进 1（第 N 天）', '## 跟进 2（第 N 天）', and
'## 微信版（引荐后）' (Chinese) or '## 短消息（LinkedIn，手动发）' (English partners).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import templates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACK_DIRS = {"customer": ROOT / "drafts", "partner": ROOT / "drafts" / "partners", "investor": ROOT / "drafts" / "investors"}
HEADS = {"email": "## 邮件", "wechat": "## 微信版（引荐后）", "dm": "## 短消息（LinkedIn，手动发）"}


def fu_head(part, track):
    n = 1 if part == "fu1" else 2
    return f"## 跟进 {n}（第 {templates.FOLLOWUP_DAYS[track][n - 1]} 天）"


def all_paths():
    for track, d in TRACK_DIRS.items():
        for p in sorted(d.glob("*.md")):
            yield track, p


def parse(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    meta_md = text.split("\n", 1)[1].split("## 调研备注", 1)[0].strip()
    rest = text.split("## 调研备注", 1)[1]
    chunks = rest.split("\n---\n")
    notes_md = chunks[0].strip()
    parts = {}
    for c in chunks[1:]:
        c = c.strip()
        head, _, body = c.partition("\n")
        body = body.strip()
        if head == HEADS["email"]:
            parts["email"] = body
        elif head == HEADS["wechat"]:
            parts["wechat"] = body
        elif head == HEADS["dm"]:
            parts["dm"] = body
        elif head.startswith("## 跟进 1"):
            parts["fu1"] = body
        elif head.startswith("## 跟进 2"):
            parts["fu2"] = body
    return {"title": title, "meta_md": meta_md, "notes_md": notes_md, "parts": parts, "head": text.split("\n---\n", 1)[0]}


def lang_of(email):
    return "en" if email.startswith("Subject:") else "zh"


def extract_fills(track, email, t=None):
    """Recover {placeholder: value} from a rendered first email by matching its template."""
    t = t or templates.load()
    lang = lang_of(email)
    tpl = t[(track, "email", lang)]
    m = templates.pattern(tpl).match(email)
    if not m:
        return None
    names = [p for p in re.split(r"(\[[^\]]*\])", tpl) if p in templates.FILLS]
    out = {}
    for ph, val in zip(names, m.groups()):
        out.setdefault(ph, val)
    return out


def write(path, head, track, lang, parts):
    """head = title + header bullets + 调研备注 (everything before the first '---')."""
    out = head.rstrip() + "\n\n---\n\n## 邮件\n\n" + parts["email"] + "\n"
    for p in ("fu1", "fu2"):
        out += "\n---\n\n" + fu_head(p, track) + "\n\n" + parts[p] + "\n"
    if lang == "zh" and "wechat" in parts:
        out += "\n---\n\n" + HEADS["wechat"] + "\n\n" + parts["wechat"] + "\n"
    if lang == "en" and "dm" in parts:
        out += "\n---\n\n" + HEADS["dm"] + "\n\n" + parts["dm"] + "\n"
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(path).write_text(out, encoding="utf-8")


def fills_of(track, d, t=None):
    """(company, name, hook) of a parsed draft; the company falls back to the title
    because the investor email itself never names the fund."""
    f = extract_fills(track, d["parts"].get("email", ""), t)
    if f is None:
        return None
    company = f.get("[Company]") or f.get("[公司名]") or d["title"]
    name = f.get("[Name]") or f.get("[称呼]")
    hook = f.get("[Hook]") or f.get("[合作句]") or f.get("[投资句]")
    return company, name, hook
