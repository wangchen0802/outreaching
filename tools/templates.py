"""Load the outreach templates from ops/templates.md (the single source of truth)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (track, part, lang) -> section heading in ops/templates.md
SECTIONS = {
    ("partner", "email", "en"): "## 渠道伙伴邮件（英文）",
    ("partner", "email", "zh"): "## 渠道伙伴邮件（中文）",
    ("partner", "dm", "en"): "## 渠道伙伴短消息（英文，LinkedIn 等手动发）",
    ("partner", "wechat", "zh"): "## 渠道伙伴微信版（引荐后）",
    ("partner", "fu1", "en"): "## 渠道伙伴跟进 1（英文，第 4 天）",
    ("partner", "fu2", "en"): "## 渠道伙伴跟进 2（英文，第 10 天）",
    ("partner", "fu1", "zh"): "## 渠道伙伴跟进 1（中文，第 4 天）",
    ("partner", "fu2", "zh"): "## 渠道伙伴跟进 2（中文，第 10 天）",
    ("investor", "email", "en"): "## 投资人邮件（英文）",
    ("investor", "email", "zh"): "## 投资人邮件（中文）",
    ("investor", "fu1", "en"): "## 投资人跟进 1（英文，第 5 天）",
    ("investor", "fu2", "en"): "## 投资人跟进 2（英文，第 12 天）",
    ("investor", "fu1", "zh"): "## 投资人跟进 1（中文，第 5 天）",
    ("investor", "fu2", "zh"): "## 投资人跟进 2（中文，第 12 天）",
    ("customer", "email", "en"): "## 客户邮件（英文）",
    ("customer", "email", "zh"): "## 客户邮件（中文）",
    ("customer", "wechat", "zh"): "## 客户微信版（引荐后）",
    ("customer", "fu1", "en"): "## 客户跟进 1（英文，第 4 天）",
    ("customer", "fu2", "en"): "## 客户跟进 2（英文，第 10 天）",
    ("customer", "fu1", "zh"): "## 客户跟进 1（中文，第 4 天）",
    ("customer", "fu2", "zh"): "## 客户跟进 2（中文，第 10 天）",
}
# Days after the first email when each follow-up is due.
FOLLOWUP_DAYS = {"partner": (4, 10), "investor": (5, 12), "customer": (4, 10)}
# Filled per recipient; everything else in brackets is left for the sender.
FILLS = {"[Company]", "[Name]", "[Hook]", "[公司名]", "[称呼]", "[合作句]", "[投资句]"}


def load():
    text = (ROOT / "ops" / "templates.md").read_text(encoding="utf-8")
    out = {}
    for key, head in SECTIONS.items():
        body = text.split(head + "\n", 1)[1]
        body = re.split(r"\n## ", body, maxsplit=1)[0]
        out[key] = body.strip()
    return out


def fills(track, lang, company, name, hook):
    if lang == "en":
        return {"[Company]": company, "[Name]": name, "[Hook]": hook}
    key = "[投资句]" if track == "investor" else "[合作句]"
    return {"[公司名]": company, "[称呼]": name, key: hook}


def render(template, values):
    for k, v in values.items():
        template = template.replace(k, v)
    return template


def render_all(track, lang, company, name, hook, t=None):
    """Every part of one recipient's sequence: {part: text}."""
    t = t or load()
    v = fills(track, lang, company, name, hook)
    return {part: render(body, v) for (tr, part, lg), body in t.items() if tr == track and lg == lang}


def pattern(template):
    """Regex matching a rendered template: per-recipient fills are wildcards, the rest literal."""
    out = ""
    for part in re.split(r"(\[[^\]]*\])", template):
        out += "(.+?)" if part in FILLS else re.escape(part)
    return re.compile("^" + out + "$", re.S)
