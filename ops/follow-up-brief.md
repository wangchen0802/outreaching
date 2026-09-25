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

## Email templates — copy VERBATIM. Only change (a) the opening line and (b) these bracket fills: [Company]/[公司名], [Name]/[称呼], and the domain list [finance, law, medicine, engineering, ...]/[金融、法律、医疗、工程……] (fill in 3–5 domains relevant to this prospect, written without brackets, e.g. "finance, accounting, law and software engineering" / "金融、会计、法律、软件工程"). Leave these EXACTLY as they are, brackets included: [Your name], [姓名], [, and every expert is ID- and credential-checked before starting work], [，所有专家上岗前均完成身份与资质核验], 微信/电话：[ ], [介绍人]. In the WeChat version change ONLY [称呼].

Template 1 (overseas, English):
Subject: Expert data for [Company]'s post-training

Hi [Name],

[One line about them, e.g. "Saw [Company] just released [model] with a big jump on [domain] — curious how you're sourcing expert data for that."]

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across [finance, law, medicine, engineering, ...]. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal

Template 2 (domestic email, Chinese):
主题：SimReal｜[公司名] 后训练专家数据

[称呼]您好，

[一句关于对方的话，例如：看到贵司最近发布了[模型]，在[领域]上提升明显，想请教一下这类专家数据是怎么采集的。]

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖[金融、法律、医疗、工程……]等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

Template 3 (domestic WeChat, after an intro):
[称呼]您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？

Fill conventions:
- [Company] in the English subject: the company's usual name + 's (e.g. "Scale AI's"), never change the "'s".
- [Name]: first name. [称呼]: 创始人/高管 → "X总"; 研究员/技术负责人 → "X老师" (surname only; only if the Chinese surname is verified — otherwise use the name as published and say so in the note).
- Opening line: ONE sentence, declarative, specific, verifiable, about something they recently did (release, report, job posting), ending with a question-like clause about how they source expert data/environments ("— curious how you're sourcing …" / "，想请教一下……"). No flattery, no marketing words, no "impressive/amazing/久仰/钦佩".
- For 人类数据供应商 (Scale/Surge/Mercor/海天瑞声/数据堂): the pitch is expert-supply partnership — the opening line should reference their expert-hiring demand (e.g. domains they are recruiting experts for) and ask how they cover it; the body stays verbatim.
- For vertical AI / financial institutions / consulting: hook on their domain model/agent work; domain list matches their vertical.
- Never mention SimReal's funding, term sheets, investors, or any GitHub link in the email. Never write "200,000 verified experts" / "20 万已验证专家".

