# Balyasny Asset Management（Applied AI 团队）

- 类别：金融机构 AI 团队｜地区：海外（美国）
- 收件人：**Charlie Flanagan**，Chief AI Officer
- 置信度：高。Anthropic 2026-09-17 发布的访谈直接写明他是 BAM 的 Chief AI Officer，内容是他本人讲 BAM 怎么评测模型、怎么搭 agent 平台（已读原文）。
- 来源：https://claude.com/blog/working-at-the-frontier-how-balyasny-asset-management-evaluates-and-governs-claude-fable-5
- 备选：**未找到**。访谈里提到 Chief Economist 自己配置了 agent 工作流，但没写名字。Applied AI 团队的其他成员没能查到（原因见核实说明）。
- 数据 / 评测负责人：**未找到**。从访谈看，评测体系归 Chief AI Officer 管，先发给他本人。

## 调研备注

**最近发布**
- **Anthropic 访谈**（2026-09-17，已读原文）：BAM 管理约 380 亿美元，约 2,000 名投资和支持人员。要点：
  - 评测："We test new models on thousands of real-world financial tasks with verifiable outcomes, across equities, macro, and commodities"。既测模型本身，也测模型在他们自己的 agent 环境里（同样的工具、文件和要求）的表现。专门盯几类失败：数值错误、覆盖遗漏、结论没有依据、检索出错。
  - 结果：Fable 5 在相关子集上 89.4%，之前的生产模型 86.1%。有一组经济学题以前没有模型做对过，Fable 第一次做对；他们重跑了评测，也单独检查了题目和打分逻辑。
  - 并购套利 agent：交易宣布后，agent 估算交易完成的概率和耗时，提取关键经济和法律条款，列出条件和里程碑。3–5 天的工作缩到 1 天以内，单次运行约 30 分钟，结果都要人工审核。
  - **BAMAgent**：内部 agent 平台，开发了约 6 个月，支持数千个自主 agent 全天运行，有的团队跑着 300 多个 agent。能做公司研究包、财报和宏观事件准备、把新信息转成财务情景。
  - 其他例子：一个 agent 在 9 万张数据库表里找到共同基金持仓，做了避税亏损收割（tax-loss harvesting）分析；首席经济学家把央行分析从约 2 天缩到约 30 分钟。
  - "most of the infrastructure is built in-house at BAM, including the execution harness, data access, and review controls"。
- OpenAI 客户案例：BAM 官网的新闻稿（搜索摘要）标题是 "Balyasny Applied AI Team Featured in OpenAI Customer Story"：https://www.bamfunds.com/news-and-insights/balyasny-openai-feature 。MIT CSAIL 演讲仍未核实。

**JD 里的数据需求**
- 未检索到。bamfunds.com 和招聘网站在本环境无法打开，搜索额度也已用完。发送前建议查一下 BAM 官网上 Applied AI、AI Evaluation 相关的在招岗位。

**切入点**
- BAM 不训练模型，用前沿模型加自研 harness，所以卖点不是 SFT 或原始后训练数据，而是评测和验证器。
- 可验证结果的金融任务：他们评测的核心就是 "thousands of real-world financial tasks with verifiable outcomes"。我们可以提供带自动验证器的新任务，覆盖股票、宏观、大宗商品，并按他们在意的失败类型（数值、覆盖、依据、检索）设计。
- 预测类任务：并购套利 agent 要估算交易完成概率和时间，我们的预测环境可以提供结果已知的历史交易题，用来回测和打分。交易条款提取可以配法律加金融专家写的评分标准。
- 长流程 agent 评测：他们要测 agent 在带工具和文件的环境里能不能规划、纠错、交付。Xitadel 和财务结账环境属于这一类，可以作为 BAMAgent 的测试环境。
- 专家评审：宏观、经济学、会计方向的专家可以给 agent 的研究包和模型打分，补充内部人工审核。

**风险**
- 不训练模型，后训练数据的需求基本没有，只能谈评测、验证器和专家评分。
- 评测体系"years ago"就开始建，基础设施大多自研，内部还有约 2,000 名投资人员可以出题，外采意愿不确定。
- 对冲基金数据保密要求高：外部专家接触不到内部数据，任务只能基于公开数据。
- SimReal 团队来自 Citadel、Millennium，这些是 BAM 的直接竞争对手。这一点可能加分，也可能引起保密或竞业方面的顾虑，沟通时要说清楚不涉及前雇主的任何信息。
- Chief AI Officer 级别高，冷邮件可能被转给团队成员处理。

**核实说明**：
- 本次复核（2026-09-25）：
  - 联系人：BAM 官网 leadership 页面（https://www.bamfunds.com/about-us/leadership/charlie-flanagan ，搜索摘要）写他是 Chief AI Officer、Management Committee 成员，2022 年从 Google 加入；theorg、Hedgeweek 等搜索结果一致。搜索摘要还提到，BAM 的中央 AI 团队由他负责，2026 年 3 月约 20 名研究员。没有查到离职的报道。
  - 开场白："thousands of real-world financial tasks with verifiable outcomes, across equities, macro, and commodities" 和 BAMAgent 都出自 Anthropic 访谈原文，搜索结果里的原文片段一致。开场白不变。
  - 之前没能核实的 OpenAI 客户案例，这次在 BAM 官网新闻里找到（搜索摘要）：https://www.bamfunds.com/news-and-insights/balyasny-openai-feature 。BAM 也在用 OpenAI 的工具，所以不是 Anthropic 的独家客户。
  - 来源里没有 GitHub 副本。
- 之前的记录：Anthropic 访谈读的是原文，以上事实大多来自这篇。bamfunds.com、openai.com 和 MIT CSAIL 在本环境无法打开，MIT CSAIL 演讲和 Applied AI 团队其他成员仍未核实。发送前建议补查在招的 AI 岗位。

---

## 邮件

Subject: Expert data for Balyasny's post-training

Hi Charlie,

Saw BAM tests every new model on thousands of verifiable financial tasks — curious how you keep that task set growing as BAMAgent takes on longer work.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across investment research, trading, economics, accounting and law. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
