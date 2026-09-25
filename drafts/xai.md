# xAI (SpaceXAI)

- 类别：frontier lab｜地区：海外（美国）
- 收件人：**Jack Garabedian**，人类数据团队（human data team，也就是训练 Grok 的 AI tutor 团队）负责人。2026-06 接替 Diego Pasini，2021 年起在 SpaceX 做 Starlink 工程
- 置信度：中。Bloomberg（2026-06-09）报道他接管 xAI 的 human data team，路透快讯和其他几家媒体的转述一致（搜索摘要）。2026-09 关于 SpaceX 购买创业公司数据的报道又提到他在整顿这个团队（搜索摘要），说明 9 月仍在任。没有官方页面
- 来源：https://www.bloomberg.com/news/articles/2026-06-09/musk-s-xai-taps-starlink-staffer-to-run-grok-training-team 、https://www.tradingview.com/news/reuters.com,2026:newsml_FWN42G143:0-jack-garabedian-a-starlink-engineer-will-be-taking-over-the-human-data-team-at-xai-bloomberg-news/ 、https://tribune.net.ph/2026/06/09/xai-shakes-up-grok-leadership
- 备选：**Michael Nicolls**，SpaceXAI President，原 Starlink 副总裁。只在一条搜索摘要里看到，出处是同一组结果里的维基百科条目（https://en.wikipedia.org/wiki/XAI_(company) 或 https://en.wikipedia.org/wiki/SpaceXAI ，未能打开）。没有交叉核实，置信度低
- 后训练负责人：**未找到**。
- 公司结构：SpaceX 于 2026-02-02 以全股票方式收购 xAI（xAI 估值 2,500 亿美元），xAI 成为 SpaceX 全资子公司：https://www.dandodiary.com/2026/03/articles/director-and-officer-liability/the-spacex-xai-merger/ 。2026-07-06 xAI 在 X 上的账号改为 @SpaceXAI 并换了新 logo，Musk 5 月的说法是以后 "just be SpaceXAI, the AI products from SpaceX"（搜索摘要）。有的媒体写成 SpaceX 整体更名为 SpaceXAI，X 归属的说法也不统一：https://finance.yahoo.com/technology/ai/articles/xai-makes-rebrand-spacexai-complete-215010760.html 、https://www.lowyat.net/2026/397863/xai-spacexai-rebrand/ 。合并后重组为四个主要开发团队，有裁员，约一半联合创始人已离开（搜索摘要）。邮件里的公司名用 SpaceXAI。
- 人员变动：原人类数据负责人 Diego Pasini 在 2026-06 被替换（见上面的 Bloomberg 链接）。据报道，HR 处理不过来，导致一些 AI tutor 离开。

## 调研备注

**最近发布**
- **Grok 4.5**（2026-07-08）："built to excel at coding, agentic tasks, and knowledge work"，这是 SpaceXAI 第一次认真做企业市场：https://techcrunch.com/2026/07/08/spacexai-releases-grok-4-5-which-elon-describes-as-an-opus-class-model/ 、https://aibusiness.com/agentic-ai/grok-4-5-spacexai-s-first-real-entry-into-enterprise 。Snorkel 用约 2,000 个 GDPVal+ 专业任务测试，Grok 4.5 平均通过率 29%，法律 40%，医疗 35%：https://snorkel.ai/blog/grok-4-5-testing-results-how-spacexais-new-model-performs-on-real-professional-work/
- **Grok 4.6**（2026-08-12）：面向长时间运行的 agent。基座不变，加长了补充训练，重新生成 SFT 轨迹，在 agentic 环境里做 RL（搜索摘要）：https://www.marktechpost.com/2026/08/12/spacexai-releases-grok-4-6/ 。GDPval-AA v2 排第二，1,753 Elo：https://venturebeat.com/technology/spacexai-debuts-grok-4-6-overtaking-kimi-k3s-performance-and-matching-gpt-5-6-sol-for-worlds-third-best-on-artificial-analysis 。2026-08-19 在 Amazon Bedrock 上线。
- **Grok 4.7**（2026-09-21）：新的更大基座。"trained with a longer reinforcement learning run on a harder mix of tasks, weighted toward problems that take many hours to complete"。Terminal-Bench 4.0 从 20.3% 提到 38.0%，Harvey Legal Agent Benchmark 只有 19.6%：https://x.ai/news/grok-4-7 （搜索摘要）、https://www.datacamp.com/blog/grok-4-7 、https://thenewstack.io/grok-4-7-agent-stamina/ 、https://www.marktechpost.com/2026/09/21/spacexai-releases-grok-4-7/
- 数据来源在变：Musk 对 SpaceX 员工说要拿 SpaceX 的全部公司数据训练 Grok：https://fortune.com/2026/08/14/elon-musk-spacex-employees-grok-ai-training/ 。2026-09 有报道称，SpaceXAI 内部讨论过向倒闭的创业公司购买客户和运营数据。报道说，这偏离了他们以往只靠 X 的数据和内部 AI tutor 的做法：https://finance.yahoo.com/technology/ai/articles/spacex-discusses-buying-data-ai-154235416.html 、https://decrypt.co/378573/elon-musk-spacex-buy-startup-data-train-ai

**JD 里的数据需求**
- xAI 直接雇 AI tutor（远程合同工），不走外包。2025-09 裁掉约 500 名通用标注员，同时说要把 "Specialist AI tutor team" 扩大 10 倍，"hiring across domains like STEM, finance, medicine, safety"：https://x.com/xai/status/1966677385056841884
- 金融（2026-03，Bloomberg）：招银行家、投资组合经理、交易员和信用分析师进数据标注团队，教 Grok 做杠杆贷款银团、困境投资、MBS 和 CLO。要求金融相关硕士，最高 $100/小时：https://www.bloomberg.com/news/articles/2026-03-16/musk-s-xai-hiring-credit-experts-bankers-to-teach-grok-finance 、https://www.entrepreneur.com/business-news/elon-musk-xai-poaching-wall-street-paying-100-an-hour-teach-grok-finance
- 法律：Corporate Law and Securities Expert，$100–200/小时（招聘聚合站，搜索摘要）：https://jobs.dukecapitalpartners.duke.edu/companies/x-ai/jobs/66610958-corporate-law-and-securities-expert
- 第三方聚合站统计的当前在招岗位（搜索摘要）：31 个语言方向，STEM 13 个；医疗、金融、法律 $45–100/小时；另有软件工程、音频、视频方向：https://aitraining.jobs/platforms/xai 、https://job-boards.greenhouse.io/xai/jobs/5063490007
- **2026-06-03 暂停招专家 AI tutor**，涉及金融、法律、STEM 等方向。原因是 HR 被申请量压垮，报道说不是永久暂停：https://www.bloomberg.com/news/articles/2026-06-03/musk-s-xai-pauses-hiring-for-specialists-to-train-grok-chatbot 。没有查到恢复招聘的报道。
- 但 2026-09-11 挂出了 Expert Team Lead, Human Data Operations："leading a team of AI Tutors responsible for delivering high-quality training data and evaluations"（搜索摘要）：https://job-boards.greenhouse.io/xai/jobs/5234209007

**切入点**
- 最匹配的是金融。他们明确在找信用、银团和投资方面的专家，所以 Xitadel、财务结账环境和金融专家写的评分标准都用得上。Grok 4.x 主打知识工作和企业市场，也是同一个方向。
- 长程 RL 任务。Grok 4.7 的 RL 偏重"好几个小时才能做完"的任务，我们可以提供多步、带验证器的金融、会计和软件工程环境。
- 法律评测和评分标准。Harvey Legal Agent Benchmark 只有 19.6%，他们也在招公司法和证券专家。
- 专家供给本身就是卖点。他们自己招专家时 HR 被压垮，暂停过招聘，最近也开始考虑买外部数据。外部专家供给正好能补这个缺口，不占他们的招聘流程。

**风险**
- 自建文化强：AI tutor 都是直接雇用，标注团队曾有约 1,500 人。外部供应商可能只能做补充。
- 人员流动和重组都很频繁（人类数据负责人换人、一半联合创始人离开、重组成四个团队），对接人可能还会变。
- 现在是 SpaceX 的一部分，供应商准入可能更正式（安全审查、数据处理要求）。这一点没有公开信息，只是提醒。
- 本次没有检索到他们外部数据供应商的公开报道。

**核实说明**：本环境的网络策略不允许直接打开 x.ai、Greenhouse 和 Bloomberg，以上内容来自搜索结果摘要，并经过交叉核对。开头一句用的 Grok 4.7 训练描述，在官方页面摘要和 DataCamp、The New Stack、MarkTechPost 等多个独立来源里表述一致。调研中途整个会话的搜索额度用完了，所以两件事没来得及核实：Michael Nicolls 的职位；专家 tutor 招聘是否已经恢复。发送前建议确认 Jack Garabedian 是否仍负责 human data。

2026-09-25 复核（本次会话，WebSearch 5 次）：
- 联系人：Bloomberg、路透（TradingView 转载）、Dealroom、GuruFocus 都写 Jack Garabedian 接替 Diego Pasini 负责 human data team；2026-09 的 SpaceX 买数据报道（https://finance.yahoo.com/technology/ai/articles/spacex-discusses-buying-data-ai-154235416.html 、https://thenextweb.com/news/spacex-dead-startups-data-grok ，搜索摘要）提到他接手后在建流程、定训练数据目标，说明仍在任。
- 开头一句：x.ai 官方页面标题 "Introducing Grok 4.7 | SpaceXAI"，"trained with a longer reinforcement learning run on a harder mix of tasks, weighted toward problems that take many hours to complete" 在官方页面摘要、The New Stack、MarkTechPost 里一致（搜索摘要）。开头一句不改。
- 公司名：x.ai 官方页面署名 SpaceXAI，xAI 的 X 账号 2026-07-06 改为 @SpaceXAI（Yahoo Finance、Lowyat、Dataconomy 等，搜索摘要）。邮件用 SpaceXAI 是对的。部分媒体把 SpaceXAI 说成 SpaceX 合并后的整体名称，这一点说法不一，已在上面公司结构里注明。
- 来源链接：本稿没有 GitHub 镜像。TradingView 链接是路透快讯的转载，路透原文在本环境打不开，保留。

---

## 邮件

Subject: Expert data for SpaceXAI's post-training

Hi Jack,

Saw that Grok 4.7 was trained with a longer RL run weighted toward tasks that take many hours to complete — curious how your human data team is sourcing expert-built tasks for domains like finance and law.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, accounting, law, medicine and software engineering. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
