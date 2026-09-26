# Anthropic

- 类别：frontier lab｜地区：海外（美国）
- 收件人（兜底）：**Jared Kaplan**，联合创始人兼 Chief Science Officer。官方页面写他 "heads its technical research efforts"
- 置信度：职位是高，官方 leadership 页面写明，已读原文。但他不直接管数据采购，作为对接人只能算低
- 来源：https://www.anthropic.com/company/leadership
- 备选：**Sam McCandlish**，联合创始人兼 Chief Architect，"leading pretraining, research productivity, and RL infrastructure"（同一页面，已读原文）
- 数据 / 人类数据负责人：**未找到**。实际对接的是两个团队，负责人名字都没有公开：
  - Domain Scaling 团队：负责金融、医疗、法律方向的 RL 环境，也管这些方向的数据供应商
  - Human Data 团队：负责外部领域专家项目

  两个团队都在招人。Human Data 供应商的合同由 R&D Operations 下的采购岗负责。
- 人员变动：没有查到。

## 调研备注

**最近发布**
- **金融 agent 模板**（2026-05-05）：一共 10 个模板。其中 "Finance and operations" 一组有 Month-end closer（"runs the close checklist, prepares journal entries, and produces close reports"）、General ledger reconciler、Statement auditor 和 Valuation reviewer。同时公布 Opus 4.7 在 Vals AI Finance Agent 上以 64.37% 领先：https://www.anthropic.com/news/finance-agents （已读原文）
- **Claude Fable 5.1 / Mythos 5.1**（2026-09-01）：
  - 发布页引用了 Jane Street 量化研究负责人的话，说 Fable 5.1 "achieves state of the art on trading intuition"。
  - Samaya 的 FrontierFinance 按评分标准打分，Fable 5.1 得 55.9%，Fable 5 是 49.2%。
  - 页面还写到，Mythos 5.1 的 reward hacking 比例比 Mythos 5 低。

  来源：https://www.anthropic.com/claude-fable-and-mythos-5-1 （已读原文）
- **Claude for Financial Advisors**（2026-09-14）：面向财富顾问，提供连接器和工作流技能：https://claude.com/blog/claude-for-financial-advisors （已读原文）
- **Claude Opus 5.5**（2026-09-22）：
  - 发布页拿一个测试展示金融能力：先在 Excel 里搭并购模型，再做成管理层汇报。Opus 5.5 用了 63 分钟，Opus 5 用了 93 分钟。
  - Optiver 说，它在一个交易台的 trading-support 测试集上拿到了 "the highest score we've recorded"。
  - Hebbia 说，在 "end-to-end finance workflows graded against expert rubrics" 上，Opus 5.5 得 86.6%，Opus 5 是 60.3%。
  - GDPval-AA v2.1 得 1846 Elo。

  来源：https://www.anthropic.com/claude-opus-5-5 （已读原文）
- 完整发布列表见官方新闻页：https://www.anthropic.com/news

**JD 里的数据需求**（岗位原文读的是 GitHub 招聘存档 marcus-crane/hirint-ai-adjacent 里的副本，下面给的是 Greenhouse 原始链接）
- Research Engineer, Domain Scaling（2026-06-19 发布，2026-09-07 的招聘页快照里还在，快照为 GitHub 上的副本：https://github.com/bojieli/ai-infra-book/blob/main/references/interviews/2026-09-07/second-pass/anthropic-jobs.txt ；原始岗位页见下方 Greenhouse 链接）：
  - "make Claude world-class at real-world knowledge work in domains like finance, healthcare, and legal"
  - "own the end-to-end process of creating RL environments… managing vendor relationships"
  - "Develop and improve QA frameworks to catch reward hacking"

  https://job-boards.greenhouse.io/anthropic/jobs/5271380008
- Program Operations Manager, Human Data（2026-04-21，招聘存档显示已关闭）：团队 "partners with external domain experts — clinical pharmacists, securities lawyers, physicists, philosophers"，岗位要负责 "data integrity across our vendor partner"。https://job-boards.greenhouse.io/anthropic/jobs/5194302008
- Data Operations Manager, Human Data（2026-06-03）："Drive strategic vendor partnerships and build scalable frameworks for technical data collection at scale"。https://job-boards.greenhouse.io/anthropic/jobs/5238460008
- Strategic Sourcing Business Partner, R&D Operations（2026-08-19）：JD 说 Human Data Operations 是 R&D 外包里最大的一块，指 "vendors that supply the human-generated data, evaluations, and expert feedback"。目标是 "most deals start on our paper rather than the vendor's"。https://job-boards.greenhouse.io/anthropic/jobs/5394993008
- Research Engineer, Virtual Collaborator：RL 环境覆盖 "from navigating internal knowledge to creating financial models"（搜索摘要）。https://job-boards.greenhouse.io/anthropic/jobs/4822955008

**切入点**
- Domain Scaling 团队最对口。
  - 金融是它写明的方向。这个岗位自己做 RL 环境、管外部供应商，还要防 reward hacking。
  - 我们的财务结账、对账和报表审计环境，结果可以用程序验证：借贷是否平衡、余额是否对得上。
  - 这正好对应 Anthropic 5 月发布的 Month-end closer、GL reconciler 和 Statement auditor 三个模板。
- 交易环境（Xitadel）。Anthropic 现在的交易类评测来自 Jane Street、Optiver 这类早期测试客户，它们是评测集，不是能大规模跑 RL 的环境。我们的差异点是可训练、结果可验证的交易模拟环境。
- 专家供给。Human Data 的外部专家项目里已经有证券律师这类人，我们可以补会计师、财务总监、买方和交易从业者。
- 比较现实的路径是先通过 Human Data 或 R&D Operations 的供应商渠道进入，拿一个结账或对账环境做小批量试点。
  - 发邮件给 Jared Kaplan 只是兜底。
  - 更好的办法是找引荐人，直接联系 Domain Scaling 团队的研究员。

**风险**
- Anthropic 是 RL 环境的大买家。2025-09 的报道说，它讨论过一年在 RL 环境上花 10 亿美元以上（https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/ ）。它和十几家环境公司合作，常签独家合同（搜索摘要，https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science ）。所以竞争对手多，买方议价能力也强。
- 专家项目已经有固定的供应商合作方，JD 原文写的是 "our vendor partner"。Surge 也长期给 Anthropic 做 RLHF 数据（https://surgehq.ai/blog/anthropic-surge-ai-rlhf-platform-train-llm-assistant-human-feedback ）。
- 采购流程很正规：合同要用 Anthropic 自己的模板，还要过安全审查和第三方风险审查。早期公司走完这套流程会比较慢。
- 收件人是兜底联系人，冷邮件的回复概率低。

**核实说明**：
- 本次复核（2026-09-25）：
  - 联系人：官方 leadership 页面、Hertz Foundation 页面和 Wikipedia（搜索结果）都写 Jared Kaplan 仍是联合创始人兼 Chief Science Officer，没有查到 2025–2026 离职的报道。
  - 开场白：Opus 5.5 发布页（https://www.anthropic.com/claude-opus-5-5 ）里的 Excel 并购模型测试（63 分钟 vs 93 分钟）和 Optiver "the highest score we've recorded"，在官方页面和两个独立来源里一致（https://www.vellum.ai/blog/claude-opus-5-5-benchmarks-explained 、https://www.technology.org/2026/09/23/anthropic-claude-opus-5-5-launch-pricing-benchmarks/ ）。开场白不变。
  - 来源：第三方 GitHub 时间线换成了官方新闻页；招聘页快照标注为副本，原始链接是 Greenhouse。
- 之前的记录：
  - 读的是原文：anthropic.com 和 claude.com 上的发布页，以及 leadership 页面。
  - 读的是副本：Greenhouse 在本环境打不开，岗位原文读的是 GitHub 招聘存档里的副本。
  - 来自搜索摘要：供应商和花费相关的内容。

发送前建议确认 Domain Scaling 岗位还在招。

---

## 邮件

Subject: Expert data for Anthropic's post-training

Hi Jared,

Saw Opus 5.5 was tested on Excel merger models and trading-desk tasks — curious how you source the finance experts and environments behind that.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, accounting, law, medicine and engineering. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
