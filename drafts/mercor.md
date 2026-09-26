# Mercor

- 类别：人类数据供应商｜地区：海外（美国）
- 收件人：**Bertie Vidgen**，APEX 基准系列的主导作者。APEX-Agents 第一作者（2026-01），APEX-Accounting 末位作者（2026-07），对外发布过 APEX-SWE 和 Mercor Research Fellowship
- 置信度：中。他主导 APEX 系列，这一点是从论文署名推断的。职位没有官方页面确认：LinkedIn 标题（搜索摘要）写 "AI Researcher @ Mercor"，2026-09-25 复核时搜索摘要还提到他任 Strategic Project Lead、同时是牛津大学访问研究员；原备注里的 Head of Human Data 这次没有搜到佐证
- 来源：
  - Archipelago README 里的引用条目，第一作者（已读原文）：https://github.com/Mercor-Intelligence/archipelago
  - APEX-Agents 论文：https://arxiv.org/abs/2601.14242
  - APEX-Accounting 论文，末位作者（多个 arXiv 日报的作者列表一致）：https://arxiv.org/abs/2607.27189
  - LinkedIn 帖子 "Mercor Research Fellowship — APEX"（搜索摘要）：https://www.linkedin.com/posts/bertie-vidgen-001_mercor-research-fellowship-apex-activity-7498412932272173057-VQAq
- 备选：
  - **Robi Lin**，原 Sepal AI 联合创始人兼 CEO（置信度低）。Sepal 做 RL 环境和训练数据，2026-02 被 Mercor 收购，团队并入 Mercor。他在 Mercor 的现职未核实：https://www.orrick.com/en/News/2026/02/Mercor-Acquires-Sepal-AI 、https://www.linkedin.com/posts/robert-lin1_today-were-excited-to-share-sepal-ai-has-activity-7424897894354391040-nfiz （搜索摘要）
  - **Brendan Foody**，联合创始人兼 CEO（置信度高），也是 APEX-Agents 和 APEX-Accounting 的作者：https://conversationswithtyler.com/episodes/brendan-foody/ 、https://fortune.com/2026/07/09/ai-unicorn-mercor-acquires-deeptune-brendan-foody-investor-a16z-openai-anthropic/
- 专家供给 / 合作负责人：**未找到**。Head of Operations Planning 岗位在招（搜索摘要）：https://www.mercor.com/careers/8723bb7f-c0af-43cd-8c5a-a06eeb89bdde/
- 人员变动：Sundeep Jain（前 Uber CPO）2025-05 加入任 President（搜索摘要）。搜索额度用完，没能专门核查 2025–2026 年的离职情况，发送前请确认收件人仍在职。

## 调研备注

**最近发布**
- **SkyRL 训练指南和开源 recipe**（2026-09-01 前后）：用 1,928 道专家编写的 APEX-Agents 任务对 Qwen3.5-397B-A17B 做 RL，held-out 480 题的 Pass@1 从 16.11% 升到 27.29%；文中说算法选择的影响不如 "the quality of the expert data"。训练数据 "Due to license issues, we cannot open-source"：https://www.mercor.com/blog/training-frontier-knowledge-work-agents-a-397b-rl-training-guide-with-skyrl/ 、https://github.com/Mercor-Intelligence/ApexAgents-SkyRL-Recipe （README 已读）、https://www.zenml.io/llmops-database/scaling-reinforcement-learning-for-long-horizon-knowledge-work-agents
- **APEX-Agents 1.1**（2026-08，参考实现仓库 2026-08-15 创建）：https://www.mercor.com/blog/introducing-apex-agents-1-1 、https://github.com/Mercor-Intelligence/apex_loop_truncated_tools_agent
- **APEX-Accounting**（arXiv，2026-07-29）：和 Ramp 合作，160 题、10 个世界，"Every task was authored and solved by experts in accounting and bookkeeping, who also wrote grading rubrics"。闭源，可以按需给模型跑榜：https://arxiv.org/abs/2607.27189 、https://labs.ramp.com/apex-accounting 、https://www.mercor.com/apex/newsletter/introducing-apex-accounting-built-with-ramp/
- 收购 **Deeptune**（2026-07-09，agent 训练 / RL 环境公司）：https://www.mercor.com/blog/mercor-to-acquire-deeptune/ 、https://fortune.com/2026/07/09/ai-unicorn-mercor-acquires-deeptune-brendan-foody-investor-a16z-openai-anthropic/ 、https://siliconangle.com/2026/07/09/mercor-buys-deeptune-build-training-environments-ai-agents/
- **APEX-SWE**（2026-03）：集成和可观测性两类软件工程任务：https://github.com/Mercor-Intelligence/apex-swe
- 收购 **Sepal AI**（2026-02）：https://www.orrick.com/en/News/2026/02/Mercor-Acquires-Sepal-AI
- **APEX-Agents**（2026-01-21）：480 题、33 个模拟公司世界，由投行、管理咨询、公司法专家搭建。Archipelago 开源环境、agent 和评分框架，示例任务是投行的并购增厚/摊薄测算：https://www.mercor.com/blog/introducing-apex-agents/ 、https://github.com/Mercor-Intelligence/archipelago/blob/main/examples/hugging_face_task/README.md

**JD 里的数据需求**
- Research Engineer - Environments, Data and Post-Training："contribute directly to post-training and RLVR, synthetic data generation, and large-scale evaluation workflows"（搜索摘要）。https://www.mercor.com/careers/97b8c17e-e438-4b61-bab1-9ae18e2c3f34/
- Fullstack Engineer, RL Environments 和 Research Engineer, Real Environments（只看到标题）。https://www.mercor.com/careers/fa580f7f-8752-428c-bb6b-439fa72c76e7/ 、https://www.mercor.com/careers/44cf5f07-342d-4f64-9062-3617beb88b31/
- 专家端岗位（work.mercor.com，搜索摘要）：
  - Supply Chain Expert：招 "senior supply chain professionals to build evaluation tasks for AI systems operating in Fortune 500 enterprise supply chain contexts"，要求 5 年以上 F500 供应链经验。https://work.mercor.com/jobs/list_AAABn4KbhtGC4NFgQilL0JYa/supply-chain-expert
  - STEM PhD (AI Subject Matter Experts)：https://work.mercor.com/jobs/list_AAABmyREibkstKDp-ZtJt6NO/stem-phd-ai-subject-matter-experts
  - Legal Expert：https://www.mercor.com/jobs/list_AAABmKp5u6OLRyAhur1NUaEr/
- 规模：官网摘要说平台上有 "millions of domain experts"，每天向专家支付 400 万美元以上（搜索摘要）。

**切入点**
- 最对口的是会计和财务结账。APEX-Accounting 从出题、解题到评分标准全由会计和簿记专家完成，我们的财务结账环境和会计专家可以直接对上，做成他们能转售的环境，或者补专家。
- 金融：APEX-Agents 有投行世界，Xitadel 和金融从业者对得上。
- 交付格式：Mercor 训练用 Harbor 任务目录（instruction.md、task.toml，tests/ 下放 verifiers.json 评分标准和 golden responses），我们的环境和验证器可以直接按这个格式交付。
- 专家缺口：供应链、STEM 博士、法律岗位都在招。我们的高校博士网络适合 STEM，企业网络适合供应链和法律。

**风险**
- Mercor 本身就是专家网络，是直接竞争对手，可能直接招募我们的专家，存在渠道冲突。
- 通过收购 Sepal（自带 2 万+ 领域专家网络，搜索摘要）和 Deeptune 自建 RL 环境能力，外采动力可能不强。
- 数据许可：训练数据因许可问题不开源，转售我们的环境前要先谈清 IP 和使用范围。
- 没有查到 Mercor 向外部专家供应商采购的公开报道。

**核实说明**：本环境打不开 mercor.com、arXiv 和招聘网站，WebSearch 额度在本次调研中途用完（全会话上限）。Archipelago、SkyRL recipe、APEX-SWE、APEX-Agents 1.1 的 README 读的是 GitHub 原文；APEX-Accounting 摘要和作者在 GitHub 上多个 arXiv 日报里一致（CSQianDong、2shin0、dangerwolf、Luvata）；SkyRL 指南的数字在 TLDR AI（2026-09-02）和 ZenML 两处一致。Bertie Vidgen 的具体职位，发送前请人工确认。

本次复核（2026-09-25，5 次 WebSearch，mercor.com 仍打不开，均为搜索摘要）：
- 联系人：LinkedIn 标题（搜索摘要）仍是 "AI Researcher @ Mercor"，另有搜索摘要说他任 Strategic Project Lead；他是 2026-07 APEX-Accounting 的作者，没有查到离职消息。"Head of Human Data" 的说法找不到佐证，已从置信度说明里删掉。职位仍需人工确认，置信度维持中。
- 开头一句：APEX-Accounting 的 "Every task was authored and solved by experts in accounting and bookkeeping" 在 arXiv 摘要、Ramp Labs 页面、Mercor 官方 newsletter 的搜索结果里一致（Ramp 页还写到 40 多位会计专业人士、过半来自四大）；APEX-Agents 的任务由投行分析师、管理咨询顾问和公司律师编写，Mercor 官方博客和 Epoch AI 的搜索摘要一致。开头一句不改。
- 来源：Deeptune 收购原来标注为"GitHub 新闻简报转引"，已确认 Fortune 原文存在，并补上 Mercor 官方博客和 SiliconANGLE。APEX-Accounting 补了 Ramp 和 Mercor 的官方页面。其余 GitHub 链接都是 Mercor 自己的仓库，保留。

---

## 邮件

Subject: Expert data for Mercor's post-training

Hi Bertie,

I'm [Your name], co-founder of SimReal (simreal.co), where we build RL environments, verifiers and expert data for post-training.

Professionals from Jane Street and Citadel support our work, and every environment is red-teamed before release: 400 reward-hacking attempts so far, none successful.

Saw every APEX-Accounting task was written and solved by accountants, and we'd like to add our expert network to your supply as you build more worlds. I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. We can start with a small paid pilot: high-quality data at a competitive price.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
