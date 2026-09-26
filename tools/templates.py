"""Load the outreach templates from ops/templates.md (the single source of truth)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = {"en": "## 海外邮件（英文）", "zh": "## 国内邮件（中文）", "wechat": "## 国内微信版（引荐后）"}
# Filled per company; everything else in brackets is left for the sender.
FILLS = {"[Company]", "[Name]", "[Hook]", "[公司名]", "[称呼]", "[合作句]"}


def load():
    text = (ROOT / "ops" / "templates.md").read_text(encoding="utf-8")
    out = {}
    for key, head in SECTIONS.items():
        body = text.split(head, 1)[1]
        body = re.split(r"\n## ", body, maxsplit=1)[0]
        out[key] = body.strip()
    return out


def render(template, values):
    for k, v in values.items():
        template = template.replace(k, v)
    return template


def pattern(template):
    """Regex matching a rendered template: per-company fills are wildcards, the rest literal."""
    out = ""
    for part in re.split(r"(\[[^\]]*\])", template):
        out += "(.+?)" if part in FILLS else re.escape(part)
    return re.compile("^" + out + "$", re.S)
