# Follow-up brief: verify drafts and finish the last three companies

You are a follow-up research session for SimReal's first outreach batch. An earlier session drafted 28 companies but ran out of web-search budget, so part of the evidence comes from search snippets or GitHub copies of articles. Your job: (1) verify the drafts assigned to you and fix what is wrong, (2) research and draft the new companies assigned to you. The repository is already checked out; work in it.

Your assignment is in the message that started this session (which drafts to verify, which companies to add, your report file name).

## Task 1: verify each assigned draft
For each draft:
1. Contact: confirm the person is still in the stated role in 2026 (company page, own homepage, recent talk or article). If they left or the title is wrong, fix the header and the email's [Name]/[称呼]; if no better contact exists, say so in 核实说明 and lower 置信度 as the brief defines it.
2. Opening line: confirm every fact in it with a primary source or two independent sources. If a fact is wrong or unverifiable, rewrite the opening line with a verified hook (same style rules as below). Nothing else in the email may change.
3. Sources: where a source link is a GitHub copy or mirror of a news article or web page, find and substitute the original publisher's URL (keep the mirror only if no original can be found, labelled as a copy).
4. Update the draft's 核实说明 to say what you checked and how. Keep the rest of the notes unless they are wrong.
5. Run `python3 tools/check_drafts.py` — every email and WeChat version must still report `match: True`.

## Task 2: new companies
Research and write drafts/<slug>.md from scratch following everything below. Partial research from the earlier session is in your assignment message; verify it before using it. If after research the contact or a verified opening line is still missing, still write the file but put 未找到 where needed, set 置信度 低, and explain in 风险.

## Report file
Write ops/<your report name>.md with one section per company: status (verified unchanged / fixed / new / could not verify), a bullet list of what changed and why with source URLs, and for every company the prospects.csv row as one line of pipe-separated fields: 公司|类别|地区|联系人|职位|来源链接（多个用 " ; " 分隔）|切入点（一句）|置信度. Then commit (drafts + report only) and push to your branch.


## Context
SimReal (simreal.co) is an early-stage AI infrastructure company selling RL environments, verifiers and expert (human) data for LLM post-training. Team is ex-Citadel, Millennium, Jane Street. Existing environments: trading (flagship "Xitadel"), financial close / accounting, software engineering, math proofs, logic reasoning, AI research, forecasting. Expert supply: via 21 partner universities + corporate networks it can reach 200,000+ professionals (PhD students to senior practitioners) across finance, law, medicine, engineering etc.; 7,000+ have signed up to its expert waitlist. Goal: learn each prospect's post-training data needs and push toward a small paid pilot.

Today is 2026-09-25. Your training knowledge is stale — verify with WebSearch.

## Environment limits (important — don't waste calls)
- WebSearch works. WebFetch / curl to most sites is BLOCKED by the network policy (company sites, Lever/Ashby/Greenhouse/Feishu job boards, arXiv, news sites, HKEX all refused).
- What DOES work: `curl -sSL https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>` (e.g. model READMEs, tech-report PDFs in GitHub repos, personal homepages hosted on github.io — fetch their source from raw.githubusercontent.com). For PDFs: `python3 -m venv /tmp/v && /tmp/v/bin/pip install -q pymupdf`, then read them with `import pymupdf`.
- This session has its own budget of 200 WebSearch calls. Plan for about 6 per company you verify and about 20 per company you research from scratch; stop searching at 190. Search in English for overseas companies, Chinese + English for Chinese companies.

## What to find per company
1. Contact: the person who leads post-training / data / human data / data partnerships / RL environments (for suppliers: expert network / supply / partnerships lead; for vertical AI and financial institutions: head of AI / applied AI / ML). Up to 3 candidates. Name, current title, source URL(s), date, confidence 高/中/低 (高 = official page / own homepage / own recent talk states the role; 中 = reputable press or paper authorship implies it; 低 = indirect or possibly outdated). Check for 2025–2026 departures. If none found: write "未找到" and give a clearly-labelled fallback (founder/CTO/head of AI).
2. Recent model releases / papers / product launches (last ~9 months) with dates + URLs.
3. Job postings revealing data needs, with URL and short quoted lines (from search snippets is OK — say so).
4. Entry points for SimReal (domains + formats: SFT, preference data, rubrics, RL tasks/environments, evals), grounded in evidence.
5. Caveats (in-house data, known vendors, compliance e.g. US Entity List for Chinese firms, sovereignty, weak fit).

## Hard rules
- Public professional info only. Never guess names/titles/emails. Do NOT search for or output emails, phone numbers, WeChat IDs, addresses.
- Every contact needs a source URL you opened or saw in a search result; mark snippet-only facts.
- Do NOT log in to or interact with LinkedIn, 脉脉, WeChat, 即刻 or any social platform. A LinkedIn/脉脉 URL seen in search results may be cited only as supporting evidence ("搜索摘要") and cannot alone justify 高.
- Do not send anything to anyone. Only edit the draft files assigned to you, plus your report file. Do not edit prospects.csv, README.md, approval/ or tools/.
- The opening line's facts MUST be verified by a primary source you read (e.g. a GitHub README / report) or by ≥2 independent search results. If you can't verify a hook, pick a different hook.

## Draft file format: drafts/<slug>.md
Reference files (structure and tone):
- English (overseas): drafts/mistral-ai.md and drafts/thinking-machines-lab.md
- Chinese (domestic, email + 微信版): drafts/zhipu.md and drafts/moonshot-ai.md
The metadata and 调研备注 sections are written in Chinese for all companies (plain, concise, declarative). Sections: header bullets (类别｜地区, 收件人, 置信度, 来源, 备选, 数据负责人 未找到 if applicable, 称呼 note for Chinese), then `## 调研备注` with **最近发布** / **JD 里的数据需求** / **切入点** / **风险** / **核实说明**, then `---`, `## 邮件`, and for domestic companies `---` + `## 微信版（引荐后）`.
Category labels: frontier lab / 国内大模型公司 / 人类数据供应商 / 垂直 AI（法律|医疗|金融） / 金融机构 AI 团队 / 咨询公司 AI 团队. 地区: 海外（国家） / 国内（城市）.

## Email templates
Use the templates in ops/templates.md (version 2) — copy them VERBATIM. Only these fills change per company: [Company], [Name], [Hook] in English; [公司名], [称呼], [合作句] in Chinese; in the WeChat version only [称呼]. Leave [Your name], [姓名], 微信/电话：[ ] and [介绍人] exactly as they are.
Easiest: write the draft file with any email section, put {"<slug>": "<hook sentence>"} in a JSON file and run `python3 tools/render_drafts.py hooks.json <slug>`; it rewrites the email (and WeChat) section from the template.

The hook ([Hook] / [合作句]) is ONE sentence: something the company recently did (verified, per the rules above) + where we would like to work with them. English ≤ 30 words, e.g. "Saw Gemini 3.8 Flash lead on Vals Finance Agent and Harvey's legal benchmark, and we'd like to support the finance and legal data behind the next step." Chinese ≤ 50 字, e.g. "看到 K3 用独立验证器训练量化因子挖掘、税务审计这类任务，希望在金融环境和验证器上和贵司合作。" No flattery, no stacked facts, no section numbers.

Fill conventions:
- [Company] in the English subject: the company's usual name + 's (e.g. "Scale AI's"), never change the "'s".
- [Name]: first name. [称呼]: 创始人/高管 → "X总"; 研究员/技术负责人 → "X老师" (surname only; only if the Chinese surname is verified — otherwise use the name as published and say so in the note).
- For 人类数据供应商 (Scale/Surge/Mercor/海天瑞声/数据堂): the pitch is expert-supply partnership — the hook references their expert-hiring demand (e.g. domains they recruit experts for) and offers our experts as supply.
- For vertical AI / financial institutions / consulting: hook on their domain model or agent work.
- Never mention SimReal's funding, term sheets, investors, or any GitHub link in the email. Never write "200,000 verified experts" / "20 万已验证专家".

