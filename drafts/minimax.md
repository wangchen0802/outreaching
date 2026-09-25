# MiniMax 稀宇科技

- 类别：国内大模型公司｜地区：国内（上海）
- 收件人：**程威宇**，MiniMax 算法工程师、通用模型后训练负责人（2026-01 时的公开头衔）
- 置信度：中。头衔来自讲座组织方青稞 Talk 在 GitHub 上维护的讲座列表：2026-01-06 他以"MiniMax算法工程师、通用模型后训练负责人"的身份讲了《MiniMax M2.1：Agent 后训练经验与认知》（已读原文。条目 2026-01-04 加入，列表最近一次更新是 2026-09-12，条目仍在）。这不是本人主页或官方页面，英文名和 M3 之后的分工都没有查到。
- 来源：
  - 青稞 Talk 讲座列表（README 第 81 行）：https://github.com/qingkelab/qingketalk
  - 讲座视频（列表里的链接，没打开）：https://bilibili.com/video/BV1H8iCBEEgT 、https://youtu.be/HzUmDxDLOoQ
  - 讲座对应的官方文章 "MiniMax M2.1: Post-Training Experience and Insights for Agent Models"（搜索结果标题，作者未核实）：https://www.minimax.io/news/post-training-experience-and-insights-for-agent-models
- 备选：
  - **Olive Song**，高级研究员，方向是 RL 和模型评测。AI Engineer 大会讲者页称她是 MiniMax 的 RL research lead，负责包括 M3 在内的模型的 RL 研究（搜索摘要，2026-09 复核）：https://ai.engineer/speakers/olive-song 。来源是 Turing Post 2026-01 的访谈和 Cognitive Revolution 播客（搜索摘要）：https://www.turingpost.com/p/olive 、https://www.cognitiverevolution.ai/intelligence-with-everyone-rl-minimax-with-olive-song-from-aie-nyc-inference-by-turing-post/ 。另有一条搜索摘要和一份 GitHub 上的韩文笔记称她是 MiniMax 的 "RL research lead"（二手，头衔未核实）。她在 AI Engineer World's Fair 2026 上以 M3 为例讲过训练和部署：https://www.youtube.com/watch?v=AVMr9PMINyo 。中文名没有查到。
  - **闫俊杰**，创始人兼 CEO（只作为兜底；来源是第三方研究笔记转引的业绩会内容，二手）：https://github.com/xbtlin/ai-berkshire/tree/main/reports/MINIMAX
- 数据 / 标注 / 数据采购负责人：**未找到**。
- 称呼用"程老师"：中文名来自讲座列表，他是技术负责人。如果改发 Olive Song，因为中文名未核实，直接用"Olive"。

## 调研备注

**最近发布**
- **MiniMax M3**（2026-06-01 发布，技术报告 arXiv 2606.13392；已读 README 和榜单图）：https://github.com/MiniMax-AI/MiniMax-M3
  - 规格：约 428B 总参数、23B 激活，1M 上下文，原生多模态，用 MiniMax Sparse Attention。README 写 "M3 achieves frontier-level performance across long-horizon agentic benchmarks, excelling in both coding and cowork"。
  - 榜单里 Cowork 组和 M2.7 的对比：BankerToolBench 从 63.9 到 76.1（Opus 4.7 是 81.3，GPT 5.5 是 70.0），GDPval rubrics 从 66.4 到 74.8，Apex-Agents 从 5.6 到 27.7。另外 OfficeQA Pro 得 45.1，SpreadSheetBench-v1 得 89.4。
  - 其他分数：SWE-Bench Pro 59.0，OSWorld-Verified 75.2，PostTrainBench 从 13.1 到 37.1。
  - 技术报告的内容（搜索摘要，不确定出自 M3 报告还是 M2 系列报告）：agent 数据管线覆盖 agentic coding、cowork、reasoning 和 general knowledge 几类任务，"each task is accompanied by its corresponding static/runtime environments, verifiable rewards, or credible feedback signals"；SFT 数据覆盖 chat、reasoning、code、cowork 四个领域。
  - 媒体称 M3 在 12 小时内无人干预完成了 4 个基座模型的后训练（腾讯新闻 2026-06-01，搜索摘要）：https://news.qq.com/rain/a/20260601A05BUS00
- **MiniMax-M2 系列技术报告**（arXiv 2605.26494，2026-05）："The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence"（只看到搜索结果标题）。
- **M2.7**（已读 README；发布日期此前写的是 2026-04，搜索摘要显示是 2026-03-18，以后者为准）：https://github.com/MiniMax-AI/MiniMax-M2.7
  - 定位是 "our first model deeply participating in its own evolution"：开发过程中让模型 "build dozens of complex skills for RL experiments"。
  - GDPval-AA 的 ELO 是 1495。
- **M2.5**（2026-02-13，已读 README）：https://github.com/MiniMax-AI/MiniMax-M2.5
  - RL 环境规模："Most of the tasks and workspaces that we perform in our company have been made into training environments for RL. To date, there are already hundreds of thousands of such environments"。编程方向用了 "more than 200,000 real-world environments"。
  - 办公场景的专家合作："we engaged in thorough collaboration with senior professionals in fields such as finance, law, and social sciences. They designed requirements, provided feedback, participated in defining standards, and directly contributed to data construction"。
  - 内部评测：Finance Modeling 是 "financial modeling problems constructed by industry experts … scored using expert-designed rubrics"；RISE 用的是 "real questions from human experts"；GDPval-MM 用 LLM-as-a-judge 做两两比较。
  - RL 框架是自研的 Forge，算法用 CISPO 加过程奖励。
- 其他：MiniMax H3（2026-07/08，视频加音频生成，和文本后训练关系不大）；开源终端 coding agent minimax-code（2026-06）。

**JD 里的数据需求**
- **未找到**。招聘页在本环境打不开，WebSearch 额度也在调研中途用完了，没能检索后训练、RL 环境、数据和评测岗位。建议手动看 MiniMax 飞书招聘页里的"后训练""数据策略""评测"岗位。

**切入点**
- 最直接的是金融、投行类的 cowork 任务。M3 把 BankerToolBench、GDPval rubrics、Apex-Agents 放进了主榜；M2.5 时已经在和金融、法律、社科的资深从业者一起建数据、定标准；内部还有专家出题、按专家评分标准打分的 Finance Modeling 评测。SimReal 的金融和会计专家、财务结账环境、Xitadel 都能对上。
- 专家写的评分标准和留出评测集：GDPval-MM 靠 LLM-as-judge，可以用领域专家来校准。
- RL 环境：他们已经把公司内部的大部分任务做成了环境，缺的应该是公司外部的专业工作流，比如交易、会计结账、法律。交付形式是能接进 Forge 的环境加验证器。
- 预测环境可以作为补充。AI 研究类任务（PostTrainBench、PaperBench 这类）他们内部自用得很深，不建议优先推。

**风险**
- 自建倾向强：Forge 是自研的，公司内部任务都做成了环境，M2.7 起还让模型自己搭 RL 实验的 skills。静态数据的需求可能会下降，卖点要放在公司内部没有的专业工作流和专家校准上。
- 已经有专家合作渠道（见 M2.5 README），可能已有供应商或直接雇专家。供应商名称没有查到。
- 上市公司，有成本压力。第三方研究笔记称 MiniMax 于 2026-01-09 在港交所上市（00100.HK），2025 年研发开支约 2.53 亿美元，前五大供应商占采购额 57.5%，最大单一供应商（阿里云）占 23.3%（转引年报和招股书，原文没读）：https://github.com/xbtlin/ai-berkshire/tree/main/reports/MINIMAX 。没有找到标注或数据服务支出的单独披露。
- 合规和声誉：没有查到 MiniMax 被列入实体清单的记录（清单原文在本环境打不开）。2026-09-08 NSA、CISA、FBI 联合发布通报，点名 DeepSeek、Moonshot AI、阿里、MiniMax、阶跃星辰和 Z.ai（智谱）对美国前沿模型做工业级蒸馏（搜索摘要，通报页和 ExecutiveGov 报道一致）：https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a 、https://www.executivegov.com/articles/nsa-fbi-cisa-warn-china-ai-distillation-attacks 。这不是制裁或实体清单，但会加重美国籍专家和合作高校的顾虑。同一份第三方笔记还提到 2026-02-23 Anthropic 指控 MiniMax 大规模蒸馏 Claude（仍是指控，本次未核实），可能会影响海外专家和合作高校的参与意愿，发送前请确认。

**核实说明**：2026-09-25 复核：程威宇的头衔重新读了青稞 Talk 列表原文（第 81 行），条目仍在；用中文搜他的名字没有其他公开来源，也没有离职报道，置信度维持中。Olive Song 补了 AI Engineer 讲者页（RL research lead）。开头一句：M3 的 BankerToolBench 76.1 除了 README 榜单图，MiniMax 官网博客、Qubrid、OfficeChai 的搜索摘要都能对上；M2.5 和金融、法律等资深从业者一起建数据、定标准，重新读了 README 原文，一致，保留不改。M2.7 发布日期更正为 2026-03-18（搜索摘要）。补充了 2026-09 蒸馏通报。以下为原调研说明。M3、M2.7、M2.5 的 README 和 M3 榜单图读的是原文，引文已逐条对照。程威宇的头衔来自青稞 Talk 的 GitHub 列表原文。Olive Song、发布日期和技术报告细节来自搜索摘要。上市和财务信息来自 GitHub 上的第三方研究笔记，是二手资料。本次 WebSearch 额度中途用完，JD 没能查。

---

## 邮件

主题：SimReal｜MiniMax 后训练专家数据

程老师您好，

看到 M3 的发布榜单里 BankerToolBench 从 M2.7 的 63.9 提到了 76.1，M2.5 时也提到在和金融、法律等领域的资深从业者一起建数据、定标准，想请教一下 M3 这类投行和办公任务的专家数据和 RL 环境，现在主要是怎么采集和搭建的。

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖金融、会计、法律、软件工程等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

程老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？
