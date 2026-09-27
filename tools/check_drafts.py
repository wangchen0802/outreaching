"""Check every draft against ops/templates.md: only the per-recipient fills may differ,
and every part of a sequence must use the same fills as its first email."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drafts  # noqa: E402
import templates  # noqa: E402

BANNED = ["verified expert", "已验证", " TS ", "term sheet", "github.com", "20 万已验证", "200,000 verified"]

t = templates.load()
bad = 0
for track, path in drafts.all_paths():
    d = drafts.parse(path)
    email = d["parts"].get("email", "")
    lang = drafts.lang_of(email)
    problems = []
    f = drafts.fills_of(track, d, t)
    if f is None:
        problems.append("email does not match template")
    else:
        company, name, hook = f
        want = templates.render_all(track, lang, company, name, hook, t)
        for part, text in want.items():
            if d["parts"].get(part) != text:
                problems.append(f"{part} differs from template")
    for part, text in d["parts"].items():
        found = [b for b in BANNED if b.lower() in text.lower()]
        if found:
            problems.append(f"{part} banned: {found}")
    if problems:
        bad += 1
        print(f"{path.relative_to(drafts.ROOT)}: " + "; ".join(problems))
n = sum(1 for _ in drafts.all_paths())
print(f"all {n} drafts match" if not bad else f"{bad} of {n} draft(s) have problems")
sys.exit(1 if bad else 0)
