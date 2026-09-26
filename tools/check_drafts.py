"""Check every draft against ops/templates.md: only the per-company fills may differ."""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import templates  # noqa: E402

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BANNED = ["verified expert", "已验证", "融资", " TS", "投资人", "github"]

t = templates.load()
pats = {k: templates.pattern(v) for k, v in t.items()}
bad = 0
for f in sorted(glob.glob("drafts/*.md")):
    s = open(f, encoding="utf-8").read()
    email = s.split("## 邮件\n\n", 1)[1].split("\n\n---", 1)[0].strip()
    key = "en" if email.startswith("Subject") else "zh"
    ok = bool(pats[key].match(email))
    line = f"{f} EMAIL template match: {ok}"
    if key == "zh":
        wx = s.split("## 微信版（引荐后）\n\n", 1)[1].strip() if "## 微信版（引荐后）" in s else ""
        m = pats["wechat"].match(wx)
        line += f" | WECHAT match: {bool(m)}"
        ok = ok and bool(m)
    found = [b for b in BANNED if b.lower() in email.lower()]
    if found:
        line += f" | banned: {found}"
        ok = False
    bad += not ok
    print(line)
print("all match" if not bad else f"{bad} draft(s) do not match")
sys.exit(1 if bad else 0)
