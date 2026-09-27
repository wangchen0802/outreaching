"""Re-render the email sequence of drafts from ops/templates.md.

Usage:
  python3 tools/render_drafts.py                 re-render every draft, keeping each one's fills
  python3 tools/render_drafts.py HOOKS.json      also replace hooks; HOOKS.json maps id -> hook sentence
  python3 tools/render_drafts.py --migrate-v2    one-off: convert version-2 customer drafts to version 3

Draft ids: customers use the slug ("openai"), partners "p-<slug>", investors "v-<slug>".
Everything above the first '---' (title, header, notes) is kept as is.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import drafts  # noqa: E402
import templates  # noqa: E402

PREFIX = {"customer": "", "partner": "p-", "investor": "v-"}


def v2_fills(email):
    """Company, name and hook from a version-2 customer email."""
    subject, body = email.split("\n", 1)
    paras = body.strip().split("\n\n")
    if subject.startswith("Subject:"):
        company = re.match(r"Subject: Expert data for (.+)'s post-training", subject).group(1)
        name = re.match(r"Hi (.+),$", paras[0].strip()).group(1)
        hook = paras[3].split(" I'd like to understand", 1)[0].strip()
        return "en", company, name, hook
    company = re.match(r"主题：SimReal｜(.+) 后训练专家数据", subject).group(1)
    name = re.match(r"(.+)您好，$", paras[0].strip()).group(1)
    hook = paras[3].split("想了解贵司", 1)[0].strip()
    return "zh", company, name, hook


def main():
    args = sys.argv[1:]
    migrate = "--migrate-v2" in args
    args = [a for a in args if a != "--migrate-v2"]
    hooks = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8")) if args else {}
    t = templates.load()
    n = 0
    for track, path in drafts.all_paths():
        d = drafts.parse(path)
        email = d["parts"].get("email", "")
        draft_id = PREFIX[track] + path.stem
        if migrate and track == "customer":
            lang, company, name, hook = v2_fills(email)
        else:
            lang = drafts.lang_of(email)
            f = drafts.fills_of(track, d, t)
            if f is None:
                raise SystemExit(f"{path}: email does not match the {track}/{lang} template; fix it by hand first")
            company, name, hook = f
        hook = hooks.get(draft_id, hook)
        parts = templates.render_all(track, lang, company, name, hook, t)
        drafts.write(path, d["head"], track, lang, parts)
        n += 1
    print(f"rendered {n} drafts")


if __name__ == "__main__":
    main()
