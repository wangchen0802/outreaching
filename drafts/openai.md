# OpenAI

- 类别：frontier lab｜地区：海外（美国）
- 收件人：**Phoebe Thacker**，Global Head of Data Research Programmes 兼 London Site Lead。之前的职位是 Head of Human Data Operations，从 Google DeepMind 加入 OpenAI
- 置信度：中。2026-04 OpenAI 宣布伦敦永久办公室时，多家媒体引用了她的话并写明现职（搜索摘要）。LinkedIn 标题是 "Head of Human Data Ops @ OpenAI"（搜索摘要）。没有读到官方页面原文
- 来源：https://www.cnbc.com/2026/04/13/openai-london-office-sam-altman-uk-stargate.html 、https://tech.eu/2026/04/13/openai-to-move-to-first-permanent-london-office-with-capacity-to-more-than-double-headcount/ 、https://www.startuphub.ai/people/phoebe-thacker 、https://humancapitalist.substack.com/p/movers-shakers-and-money-makers-826 （均为搜索摘要）
- 备选：**Nick Turley**，VP、ChatGPT 负责人。他的团队和 Morgan Stanley、Evercore 一起设计了 ChatGPT for Financial Services（搜索摘要）：https://www.cnbc.com/2026/09/10/openai-chatgpt-for-financial-services-targets-work-of-junior-bankers.html 、https://fortune.com/2026/09/10/openai-courts-wall-street-with-chatgpt-for-financial-services-developed-with-morgan-stanley/ 。他管产品，不管数据采购，只适合从金融业务这条线切入
- 数据 / 人类数据负责人：就是收件人。日常对接的人更可能是 Human Data 团队的 Research Program Manager（Human Data Campaigns），以及 Agent Post-Training 下 Artifacts、Frontier Evals & Environments 方向的研究员。这些人的名字没有找到
- 人员变动：没有查到她在 2026 年离职。最近一条公开的职位信息是 2026-04 的，发送前再确认

## 调研备注

**最近发布**
- **GPT-5.5**（2026-04-23）："Frontier model for coding, research, computer use, documents, spreadsheets, and long-running work"（GitHub 时间线 README，已读原文）：https://github.com/jqueryscript/chatgpt-timeline
- **GPT-5.6 Sol / Terra / Luna**（2026-06-27 开始有限预览）：https://techcrunch.com/2026/07/09/openai-launches-its-new-family-of-models-with-gpt-5-6/
- **GPT-6 Astra**（2026-09-03）：OpenAI 说它在网络安全、专业工作、软件工程和科学上是 "generational leap"（搜索摘要）：https://openai.com/index/gpt-6-astra/ 、https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html 。Artificial Analysis 等测出 Astra 在 GDPval-AA v2 上比 GPT-5.6 Sol 低约 45–80 Elo（搜索摘要）：https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra 。Anthropic 的 Opus 5.5 发布页也说，Opus 5.5 默认档在 GDPval-AA v2.1 上就超过了 Astra 最高档（竞品口径，已读原文）
- **ChatGPT for Financial Services**（2026-09-10）：基于 GPT-6 Astra，先做投行和股票研究（公司研究、估值、LBO 建模、pitchbook）。Morgan Stanley 和 Evercore 参与设计，接入了 Daloopa、PitchBook、LSEG、Crunchbase 的数据：https://openai.com/index/introducing-chatgpt-financial-services/ 、https://venturebeat.com/data/openai-launches-chatgpt-for-financial-services-with-integrated-data-sources-it-pulls-research-cites-it-and-builds-decks-in-minutes 。Turley 说，OpenAI 单独做行业产品的领域目前是金融、网络安全和软件工程（搜索摘要）
- **GPT-6 Sol / Luna**（2026-09-22）：训练方法和 Astra 相关，在专业工作、事实可靠性、代码和 computer use 上有改进（时间线 README，已读原文）：https://openai.com/index/introducing-gpt-6-sol-and-luna/

**JD 里的数据需求**（岗位原文读的是 GitHub 上的招聘存档 marcus-crane/hirint-ai-adjacent，下面给的是 Ashby 原始链接）
- Program Manager, Human Data（2026-08-19）：团队职责 "spans bespoke data campaigns, scalable synthetic data generation, and product-embedded signals"，这个岗位是 "a key interface between our external vendors and AI trainers"。https://jobs.ashbyhq.com/openai/932c9cc1-c542-4f67-8d0d-443de87b8213
- Research Program Manager, Human Data Campaigns（2026-07-21）："a key interface between our research roadmap, external vendors, AI trainers, and the Human Data engineering team"。https://jobs.ashbyhq.com/openai/5edd5a13-2fc9-427c-ad88-2b67c97a0afe
- Agent Post-Training, Artifacts Research（2026-06-26）：训练模型产出 "documents, spreadsheets, slide decks, dashboards, reports"，要求 "domain judgment, correctness"，工作覆盖 "RL, data pipelines, graders, reward signals, evals"。https://jobs.ashbyhq.com/openai/6897d024-88c1-43ed-adb8-5d2fc5eec984
- Agent Post-Training, Frontier Evals and Environments Research（2026-06-26）："Create ambitious RL environments to push our models to their limits"。这个方向之前做过 GDPval 和 SWE-bench Verified。https://jobs.ashbyhq.com/openai/9d72171e-2630-4347-83a1-263178644282

**切入点**
- 投行和股票研究 OpenAI 已经自己覆盖了（见风险）。我们能补的是它金融产品还没做到的两块：
  - 交易和市场：Xitadel 覆盖执行、做市和风控，P&L 可以用程序验证
  - 财务结账和会计：对账、分录、结账清单，结果能不能对平可以直接检查
- Artifacts 团队在训练模型做表格和财务模型，需要打分器。我们能交付两样东西：检查公式和勾稽关系的 verifier，以及专家写的评分标准。
- Frontier Evals & Environments 团队做 GDPval 这类评测，我们可以供交易和会计方向的 RL 任务和评测集。
- 专家这边，我们能补的是没有投行背景的金融专家，比如买方、风控、会计师和财务总监。
- 比较现实的路径是先通过 Human Data 团队（收件人）进供应商名单，用一个小的交易环境或结账环境做试点，再请 Artifacts 团队的一位研究员做技术对接。

**风险**
- OpenAI 已经在直接招金融专家。2025-10 Bloomberg 报道了 "Project Mercury"：100 多名前投行分析师按每小时 150 美元给 OpenAI 做财务模型（https://www.bloomberg.com/news/articles/2025-10-21/openai-looks-to-replace-the-drudgery-of-junior-bankers-workload 、https://sherwood.news/tech/openai-has-an-army-of-ex-investment-bankers-making-financial-models-to-train/ ）。产品上还有 Morgan Stanley、Evercore 做设计伙伴。只拿"金融专家数据"去谈，很难进去。
- 大供应商已经在里面。Surge 的客户包括 OpenAI，还成立了专门做 RL 环境的部门（https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/ ）。Mercor、Handshake、Turing 也开始卖 RL 环境了（搜索摘要，https://www.troveo.ai/resources/rl-environment-companies ）。
- Human Data 团队规模大、流程成熟，有专门的 PGM 和 RPM 管供应商。新供应商要过采购和安全审查，周期可能比较长。
- 收件人的职位来自 2026-04 的媒体报道和 LinkedIn 搜索摘要，原文没读到。

**核实说明**：本环境打不开 openai.com、Ashby 和新闻站。岗位原文读的是 GitHub 招聘存档里的副本，发布时间线读的是 GitHub README（jqueryscript/chatgpt-timeline）。其余内容来自搜索摘要，都用多个来源交叉核对过。发送前建议确认岗位还在招，以及收件人的现职。

---

## 邮件

Subject: Expert data for OpenAI's post-training

Hi Phoebe,

Saw OpenAI launched ChatGPT for Financial Services on GPT-6 Astra this month, starting with investment banking and equity research work — curious how your team is sourcing finance expertise for the post-training and evals behind it.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, accounting, law, medicine and software engineering. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
