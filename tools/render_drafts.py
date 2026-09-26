"""Re-render the email (and WeChat) section of drafts from ops/templates.md.

Usage: python3 tools/render_drafts.py HOOKS.json [slug ...]
HOOKS.json maps slug -> the one-sentence hook for that company. Company and
recipient names are taken from the draft's current subject and greeting.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import templates  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def names(email):
    subject = email.split("\n", 1)[0]
    greeting = email.split("\n\n")[1].strip()
    if subject.startswith("Subject:"):
        company = re.match(r"Subject: Expert data for (.+)'s post-training", subject).group(1)
        name = re.match(r"Hi (.+),$", greeting).group(1)
        return "en", company, name
    company = re.match(r"主题：SimReal｜(.+) 后训练专家数据", subject).group(1)
    name = re.match(r"(.+)您好，$", greeting).group(1)
    return "zh", company, name


def main():
    hooks = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    only = set(sys.argv[2:])
    t = templates.load()
    for slug, hook in hooks.items():
        if only and slug not in only:
            continue
        path = ROOT / "drafts" / f"{slug}.md"
        text = path.read_text(encoding="utf-8")
        head, _, rest = text.partition("## 邮件")
        email = rest.split("\n---\n", 1)[0].strip()
        lang, company, name = names(email)
        if lang == "en":
            body = templates.render(t["en"], {"[Company]": company, "[Name]": name, "[Hook]": hook})
            new = head + "## 邮件\n\n" + body + "\n"
        else:
            body = templates.render(t["zh"], {"[公司名]": company, "[称呼]": name, "[合作句]": hook})
            wechat = templates.render(t["wechat"], {"[称呼]": name})
            new = head + "## 邮件\n\n" + body + "\n\n---\n\n## 微信版（引荐后）\n\n" + wechat + "\n"
        path.write_text(new, encoding="utf-8")
        print(f"{slug}: {lang} · {company} · {name}")


if __name__ == "__main__":
    main()
