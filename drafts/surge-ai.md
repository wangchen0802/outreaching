# Surge AI

- 类别：人类数据供应商｜地区：海外（美国）
- 收件人：**Sushant Mehta**，Surge AI 研究员，负责 RL 环境和专家基准。EnterpriseBench CoreCraft 论文第一作者（2026-02），也是 Riemann-bench、GDP.pdf、HANDBOOK.md、Chartography 的作者之一，署名一般排在 Edwin Chen 之前
- 置信度：中。职责是从论文署名推断的，没有找到本人主页或官方页面写明职位
- 来源：
  - CoreCraft 论文（作者：Sushant Mehta, Logan Ritchie, Suhaas Garre, Ian Niebres, Nick Heiner, Edwin Chen；搜索摘要）：https://arxiv.org/abs/2602.16179
  - Chartography 论文（2026-08，作者：Suhaas Garre, Chris Mutty, Sushant Mehta, Edwin Chen，Surge AI；读的是 GitHub 上的全文镜像）：https://arxiv.org/abs/2608.10677
  - HANDBOOK.md 论文（作者含 Suhaas Garre、Sushant Mehta、Edwin Chen）：https://arxiv.org/abs/2607.25398 ，论文笔记：https://github.com/lextoumbourou/notes/blob/master/notes/reference/papers/handbook-md-a-benchmark-for-long-context-agentic-instruction-following.md
- 备选：
  - **Edwin Chen**，创始人兼 CEO（置信度高）。Lenny's Podcast（2025-12-07）简介写 "founder and CEO of Surge AI"，节目里还说自己常和研究团队一起分析数据：https://www.youtube.com/watch?v=dduQeaqmpnI （文字稿：https://github.com/ChatPRD/lennys-podcast-transcripts/blob/main/episodes/edwin-chen/transcript.md ）
  - **Suhaas Garre**，研究员（置信度中）。Riemann-bench、GDP.pdf、Chartography 的第一作者：https://arxiv.org/abs/2608.10677
- 专家供给 / 合作负责人：**未找到**。Surge 没有公开的供给或合作负责人。公司人少（2025 年底不到 100 人），这类合作大概率要 CEO 拍板。

## 调研备注

**最近发布**
- **DAYJOB**（2026-09-23）：长周期职业 agent 基准系列，任务是 "realistic workplace requests that require professional judgment"，Harbor 格式，由 Claude Opus 4.8 做 agentic 评分：https://www.surgehq.ai/blog/dayjob 、https://github.com/surge-ai/dayjob （README 已读）
- 帮 Anthropic 的自动化对齐研究员项目做人类基线，包括 "researcher recruitment, structured submissions, quality control, and expert review"（2026-09-15，RSS 摘要）：https://www.surgehq.ai/blog/anthropic-automated-alignment-research
- 用 1,700 道 Surge agentic coding 任务后训练 Kimi K2.7，SWE-Marathon +20.0pp（2026-09-11，RSS 摘要）：https://www.surgehq.ai/blog/hill-climbing-swe-agent-kimi-k-2-7
- Tuesday Work Index 综合基准（2026-08-18）和几期模型评测：https://www.surgehq.ai/blog/tuesday-frontier-work-index
- **Chartography**（2026-07-16）：100 道专业图表题，每题由 "someone who reads these charts for a living" 编写，再由 "three additional experts" 独立核验。领域覆盖 STEM（含 5 个工程子领域）、金融/投资、制造/供应链、医疗（README 和论文全文已读）：https://github.com/surge-ai/chartography
- **HANDBOOK.md**（2026-06-25）：每个任务都是一个带内部工具和 MCP 服务的 RL 环境，政策手册由专家根据真实行业规范改写，领域是 Finance、Medical Billing、Insurance、Logistics、HR。没有前沿模型超过 25%（README 已读）：https://github.com/surge-ai/handbook
- 其他：GDP.pdf（2026-04，被 OpenAI GPT-5.6 和 Anthropic Fable 5 发布材料引用）、Riemann-bench（2026-03）、CoreCraft（2026-02）、Antidote 排行榜，后者由 "doctors, lawyers, and engineers" 评分（2026-05-21）。以上来自 Surge 博客 RSS（GitHub 镜像）：https://github.com/Olshansk/rss-feeds/blob/main/feeds/feed_blogsurgeai.xml

**JD 里的数据需求**
- HN "Who is hiring"（2026-07），Surge 员工发帖，招 Software Engineers 和 Strategic Project Lead，写到 "Our current focus is RL environments to help our clients ship agents that interact with the world"（读的是 GitHub 存档）：https://news.ycombinator.com/item?id=48753928
- RL Environments Architect（只看到搜索结果标题，没读到内容）：https://freehire.me/jobs/rl-environments-architect-surge-ai-bhoxfosl
- 专家端招聘：没有查到 Surge 自己名下的专家招聘页。有间接来源说 DataAnnotation.tech 等平台属于 Surge，Edwin Chen 未置可否（未核实）。

**切入点**
- 专家供给：Surge 的基准都要多名专家出题加复核（Chartography 每题 4 人），领域集中在金融、医疗账单/保险、工程、供应链、HR、数学。我们可以补高校博士生和资深从业者，重点是金融、会计、医疗、工程。
- 可转售的环境和验证器：CoreCraft、HANDBOOK.md、DAYJOB 都是企业模拟世界加专家评分标准，格式用 Harbor。Xitadel 和财务结账环境可以按同样格式交付，由 Surge 卖给实验室。
- AI 研究专家：Anthropic 项目需要招研究员做人类基线，可以对上我们的 AI 研究环境和博士生网络。
- 数学：Riemann-bench 需要顶尖数学专家，我们有数学证明环境。

**风险**
- Surge 本身就卖 RL 环境和专家数据，是直接竞争对手。对外采购专家供给不合常规，对方可能只把我们当成人才来源。
- 有自己的大规模专家众包平台（归属未公开确认），还自己训模型来验证数据效果（Kimi K2.7、Qwen3.5-122B、4B 模型），自研能力强。
- 公司没融过资、对外低调，没有公开的合作或供应商负责人，冷邮件回复率可能低。
- 没有查到 Surge 向外部供应商采购的公开报道。

**核实说明**：本环境打不开 surgehq.ai、arXiv 和招聘网站，WebSearch 额度在本次调研中途用完（全会话上限）。Chartography、HANDBOOK.md、DAYJOB 的 README 和 Chartography 论文全文读的是 GitHub 原文；博客列表和日期来自 GitHub 上的 Surge 博客 RSS 镜像；CoreCraft 作者来自搜索摘要，另有 GitHub 上 2026-02-19 的 arXiv 日报检索结果和一个引用 CoreCraft 的仓库，都显示 Sushant Mehta 是第一作者。Sushant Mehta 的具体职位和是否仍在职，发送前请在 LinkedIn 或 Surge 网站上人工确认。

---

## 邮件

Subject: Expert data for Surge AI's post-training

Hi Sushant,

Saw that each Chartography task was written by a working professional and then verified by three more experts, across engineering, finance, supply chain and healthcare — curious how you're sourcing that depth of expert review as your RL environment work grows.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, medicine, law, engineering and mathematics. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
