# 字节跳动 Seed

- 类别：国内大模型公司｜地区：国内（北京）
- 收件人：**钟宛君（Wanjun Zhong）**，字节跳动 Seed 高级研究员、TopSeed 成员；本人主页写明她是"通用 Agent 优化的算法负责人之一"，参与了 Seed 2.1 到 Seed 1.5 各代模型，也是豆包专业版办公任务模式的算法负责人之一
- 置信度：高。本人主页写明："As one of the algorithm leads for general agent optimization, I contribute to the ByteDance Seed model series (e.g., Seed 2.1 to Seed 1.5)"；新闻栏写着 2026.06 发布 Seed 2.1，同月发布 "Office Task Mode of 豆包专业版 (Doubao Pro), where I was fortunate to contribute as one of the algorithm leads"；2026.04 发布 Agent-World（已读原文，主页源文件最后更新于 2026-08-05）。需要注意，她负责的是通用 Agent 这条线的算法，不是整个后训练或数据部门。
- 来源：
  - 本人主页：https://zhongwanjun.github.io/ （源文件 https://github.com/zhongwanjun/zhongwanjun.github.io/blob/master/_pages/includes/intro.md 和 news_en.md；中文名见 _config.yml："Wanjun Zhong (钟宛君)"）
  - Agent-World 论文（主页所列，本人为第四作者）：https://arxiv.org/abs/2604.18292
- 备选：
  - **焦方锴（Fangkai Jiao）**，Seed 技术成员。本人主页写 "working on general agent rl, including coding agent, search agent, MCP agent, and knowledge work"，并写 Seed 1.8 时 "I'm in charge of the post-training for agentic scenarios"（已读原文，主页更新于 2026-08-04）。他同时是 NTU 在读博士，职级可能不高：https://jiaofangkai.com （源文件 https://github.com/SparkJiao/SparkJiao.github.io/blob/master/_pages/about.md ）
  - **郁博文**，原阿里 Qwen 后训练负责人，2026-03 加入 Seed，据报道任视觉模型与多模态交互团队后训练负责人（二手：GitHub 上的新闻聚合转引 36氪和华尔街见闻，原文没打开）：https://36kr.com/p/3709827296440713 、https://wallstreetcn.com/livenews/3068592 。他的个人主页还停在 2024 年的 Qwen 职务。
  - **吴永辉**，Seed 负责人（只作为兜底）。第三方研究笔记称他从 2025-10 起是 Seed 唯一的"一号位"（转引 36氪、澎湃，二手）：https://github.com/xbtlin/ai-berkshire/blob/main/reports/中国大模型六强横向研究-20260721/01-字节Seed-豆包.md
- 数据 / 标注 / 数据采购负责人：**未找到**。
- 称呼用"钟老师"：中文名已在她主页核实，她在学术圈活跃，这个称呼比较常见。

## 调研备注

**最近发布**
- **Seed 2.1**（2026-06-24，火山引擎 FORCE 大会）：分 Pro 和 Turbo 两档，官方强调代码、长链路 agent 任务和多模态理解三方面的提升（搜索摘要）：https://datanorth.ai/news/bytedance-releases-seed-2-1-pro-and-seed-2-1-turbo 、https://llm-stats.com/models/seed-2.1-pro 。钟宛君主页列出的技术报告标题是 "Seed2.1: A Next-Generation Agent Foundation Model for Real-World Productivity"：https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity （本环境打不开）。
- **豆包专业版办公任务模式**（2026-06）：钟宛君是算法负责人之一（来源同上，本人主页）。
- **EdgeBench**（repo 创建于 2026-06-23，技术报告 arXiv 2607.05155，已读 README）：https://github.com/ByteDance-Seed/EdgeBench
  - 共 134 个"日级"真实任务，公开 51 个，分 6 类。"Recorded human expert effort averages 57.2 hours per task (up to 320 hours)"。
  - 评测框架 SForge 用 work 和 judge 两个容器，agent 看不到隐藏测试；agent 可以多次提交，拿到反馈后继续改。1.1.0 版支持 E2B 后端。
  - Knowledge 类里有金融任务，比如 cta_risk_budget_optimization、portfolio_risk_calibration。
  - 榜单只列了外部模型（Opus 4.8 在 12 小时档得 51.3，GPT-5.5 得 48.4），没有 Seed 自己的模型。
- **Agent-World**（2026-04，arXiv 2604.18292）："Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence"（只看到标题和作者，正文没读）。
- **Seed2.0 Model Card**（2026-02-14，已读 PDF）：https://github.com/ByteDance-Seed/Seed2.0
  - 报告自己承认两块短板："considerable gaps with Claude in terms of coding"；在长尾知识上 "relatively obvious gaps with Gemini"。
  - 原文还写："real-world knowledge is highly domain-specific and long-tailed; models strong in math and code often provide little value in specialized professional contexts"。
  - 内部评测里有 GDPVal-Verified（基于评分标准自动打分）和 XpertBench。做 HLE-Verified 时 "We hire domain experts to review and select only questions"。
- **CUDA Agent**（2026-08，Seed 和清华 AIR 合作）：用 agentic RL 在真实工具链里生成 GPU kernel（二手，来自 GitHub 上的新闻聚合）。

**JD 里的数据需求**
- **未找到**。jobs.bytedance.com 在本环境打不开，WebSearch 额度也在调研中途用完了，没能检索 Seed 的数据、专家标注和评测岗位。建议手动看招聘页里带"Seed"后缀的数据、评测和后训练岗位。
- 钟宛君主页写着团队在招研究实习生、在找学术合作（本人主页原文）。

**切入点**
- 办公和知识工作类 agent 需要专家任务和验证器：钟宛君负责办公任务模式，焦方锴做 knowledge work 方向的 agent RL；Seed2.0 自己承认专业长尾知识是短板，还专门做了 GDPVal-Verified、XpertBench 这类按评分标准打分的评测。财务结账、会计环境和金融专家写的评分标准可以直接对上。
- 长程可验证环境：EdgeBench 的做法（隐藏测试的 judge 容器、日级任务、专家工时基线）和 SimReal 的 RL 环境加验证器是同一类东西，而且里面已经有 CTA 风险预算、组合风险校准这类金融任务。Xitadel、预测环境可以作为补充任务，按 SForge 或 E2B 的格式交付。
- 专家审题和留出评测集：他们做 HLE-Verified 时已经在雇领域专家审题。
- 数学证明方面，他们有 Seed-Prover，EdgeBench 也有 Lean 形式化任务，内部实力强，不建议作为优先切入点。

**风险**
- 自建倾向强：第三方笔记称 Seed 仅数据团队就近千人（口径冲突，可信度低），并称 Seed 坚持不蒸馏现成模型（二手）。Agent-World 走的是合成环境路线。所以要卖的是难以合成的部分：专家基线、隐藏验证器、金融等专业工作流。
- 组织变动多：第三方笔记转引晚点等报道，称一年内约 70 名 Seed 技术人员离职，2025–2026 年多位负责人变动（二手）。联系前最好再确认一下对方的现职。
- 合规：本次没有单独核实字节跳动的出口管制状态。字节的数据跨境和美国监管都比较敏感，发送前请确认美国籍专家和合作高校的参与是否受影响。
- 大厂供应商准入流程通常比较长，小批量试点可能也要走采购流程（推断）。

**核实说明**：2026-09-25 复核：重新读了钟宛君主页源文件（intro.md、news_en.md），"one of the algorithm leads for general agent optimization"、2026.06 Seed 2.1 和豆包专业版办公任务模式、2026.04 Agent-World 都还在，开头一句的三个事实都对得上，保留不改。本次没有查到她离职的消息。这份草稿里 GitHub 上的第三方研究笔记和新闻聚合是转述，原始报道（36氪、华尔街见闻）的链接已经在正文里。以下为原调研说明。钟宛君和焦方锴的主页源文件、EdgeBench README、Seed2.0 Model Card 读的是原文。Seed 2.1 的发布日期来自搜索摘要。郁博文、吴永辉和组织变动的信息来自 GitHub 上的第三方新闻聚合和研究笔记，都是二手。本次 WebSearch 额度中途用完，JD 和数据负责人都没能查。

---

## 邮件

主题：SimReal｜字节跳动 Seed 后训练专家数据

钟老师您好，

看到 Seed 2.1 和豆包专业版的办公任务模式在 6 月上线，您参与的 Agent-World 也在做真实环境的规模化合成，想请教一下办公这类专业任务里，合成环境之外的专家数据和验证器目前是怎么来的。

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖金融、会计、法律、医疗等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

钟老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？
