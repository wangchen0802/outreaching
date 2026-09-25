# 阿里巴巴 通义千问 Qwen

- 类别：国内大模型公司｜地区：国内（杭州）
- 收件人：**郑楚杰（Chujie Zheng）**，Qwen 团队 member of technical staff，方向是 RL scaling：带 OPD 团队做后训练整合，此前牵头大规模 RL 训练的研究，搭建并维护 RL/OPD 基础设施；GSPO 第一作者
- 置信度：高。本人主页写明 "Leading the OPD team for post-training consolidation"、"Led RL research for large-scale RL training"、"Initiated and maintaining the RL/OPD infrastructure"，项目列表里有 2026-08 的 Qwen3.8，说明是近期更新的（已读原文）。
- 来源：
  - 本人主页：https://chujiezheng.github.io/ （源文件 https://github.com/chujiezheng/chujiezheng.github.io/blob/master/_pages/about.md ；站点配置里的名字是 "Chujie Zheng 郑楚杰"，描述是 "Research engineer @Qwen"：https://github.com/chujiezheng/chujiezheng.github.io/blob/master/_config.yml ）
  - GSPO 论文（Qwen3 用的 RL 算法），第一作者：https://arxiv.org/abs/2507.18071
- 备选：
  - **周浩**：后训练负责人。晚点 LatePost 2026-03-04 报道，郁博文离职后，后训练工作"将由今年初加入阿里通义实验室的前 DeepMind 高级资深研究员周浩接任"，向周靖人汇报（经 GitHub 上的推文存档看到）：https://github.com/artxgj/chinese-study/blob/main/twitter/hanzi-cards/Qwen.md 。量子位 2026-03-05 也说他"将负责千问的后训练"，此前在 Google DeepMind 做 Gemini 的后训练（经 GitHub 上的 RSS 存档看到，原文 https://mp.weixin.qq.com/s/pR65T4hzAjeQxNZ9YjlGMQ ）。置信度中：有两家媒体，但都是 3 月的消息，之后没有看到新的公开信息；英文名不确定，也没法在 Qwen 论文里核对。
  - **刘大一恒（Dayiheng Liu）**：2026 年多个 Qwen 项目的资深作者，包括 E-Commerce Bench（2026-08，末位作者）、Confident Decoding、FlashQLA、Qwen-VLA、Qwen-Drive 和 RecreationWorld（已读各 README 的引用信息）。具体头衔没有核实，个人主页停在 2021 年：https://github.com/QwenLM/E-CommerceBench 。置信度中。
  - **周靖人**，通义负责人（高管，只作为兜底）。据二手资料，2026-04 执掌通义大模型事业部，6 月升任阿里集团首席科学家：https://github.com/xbtlin/ai-berkshire/blob/main/reports/中国大模型六强横向研究-20260721/02-阿里Qwen-通义.md
- 数据 / 标注 / 数据采购负责人：**未找到**。
- 2026 年离职：
  - **林俊旸**，原 Qwen 负责人：个人主页现在写的是 "Independent researcher"（已读原文：https://github.com/justinlin610/justinlin610.github.io ）。据报道 2026-03-04 宣布卸任（二手）。
  - **郁博文**，原后训练负责人：据 LatePost，同日离职（推文存档，同上）；二手资料称他去了字节 Seed。他的个人主页还写着 "leading Qwen's post-training"，但内容停在 2024 年，已经过时。
  - **惠彬原**，原 Qwen Coder 负责人：据二手资料同期离开，未核实。他的主页还写着 Qwen，但新闻停在 2025-01。
- 称呼用"郑老师"：中文名由本人站点配置确认。

## 调研备注

**最近发布**（以下来自 QwenLM 各仓库 README，已读原文）
- **Qwen3.8**（2026-08-12 开源 Qwen3.8-2.4T-A95B，08-14 开源 Qwen3.8-27B）："For the first time, Qwen3.8 brings a Qwen-Max-class model to open release"，并且 "delivers substantial gains across coding, professional work, research, and long-horizon agentic tasks"。博客标题是 "Qwen3.8-Max: A New Bar for Coding and Cowork"：https://github.com/QwenLM/Qwen3.8
- **Qwen3.8-Flash-Next**（2026-08-26）：Qwen4 架构的预览。主模型 125B，另有 51B 的 N-gram embedding，每个 token 激活 6B；训练成本约为 Qwen3.7-Plus 的 1/9：https://github.com/QwenLM/Qwen3.8-Flash-Next
- **Qwen3.7**（据二手资料 2026-05-20 发布）：只在云端提供，没有开源权重；Qwen3.8 又回到开源（二手，出处同上 ai-berkshire 报告）。
- **Qwen3.5 / 3.6**（2026-02 / 04）：README 写着 "Reinforcement learning scaled across million-agent environments with progressively complex task distributions"。
- **E-Commerce Bench**（arXiv 2608.30730，仓库 2026-08-26）：agent 用 10 万元本金经营最多 4 家网店，连续 365 天。需求模型基于脱敏的真实电商平台数据，6,886 个商品；576 个供应商里有 152 个是欺诈的，谈判价格由确定性内核决定。Qwen3.8-Max 年末平均资产 47.2 万元，GPT-5.6 Sol 是 143.1 万元：https://github.com/QwenLM/E-CommerceBench
- **RecreationWorld**（arXiv 2609.22000，仓库 2026-09-18）：面向 computer-use agent 的可扩展、可验证环境，覆盖五个平台；RecreationBench 有 250 个留出任务，用程序断言和视觉断言打分：https://github.com/QwenLM/RecreationWorld
- **Qwen-AgentWorld**（2026-06-24）：语言世界模型 35B-A3B，外加覆盖 7 个领域的 AgentWorldBench：https://github.com/QwenLM/Qwen-AgentWorld
- **RationaleRM**（arXiv 2602.04649，2026-02）：要求奖励模型不只是结论和人一致，推理过程也要和人类判断理由一致；用 MetaJudge 把人类理由拆成原子单元做匹配：https://github.com/QwenLM/RationaleRM
- **组织**：2026-06 合并成立 Token Foundry 事业部，由吴泳铭直管（二手资料，出处同上）。部分仓库的署名已经是 "Alibaba Token Hub, Alibaba Group"：https://github.com/QwenLM/Omnilingua-Bench

**JD 里的数据需求**
- 招聘页 talent.alibaba.com 在本环境打不开，没有找到 JD 原文。
- 二手整理：2026 年校招开放 25 类岗位，"密度最高的是后训练、Agent、奖励与评测、自进化相关方向"（没有 JD 原文和链接）：https://github.com/adongwanai/AgentGuide/blob/main/docs/06-research-frontiers/README.md
- 建议手动看一下阿里招聘页里 Qwen 后训练、奖励模型和评测相关的岗位。

**切入点**
- 专业工作（professional work）的 RL 环境和专家数据：Qwen3.8 把它和长程 agent 任务列为主要提升方向。金融（Xitadel 交易、财务结账和会计）、法律都能对上。
- 长程商业环境：E-Commerce Bench 说明他们在做基于真实市场数据的长程经营环境，Xitadel 也是在真实市场数据上跑的交易环境，可以作为训练环境或留出评测来谈。
- 奖励模型和评分标准：RationaleRM 用的是人类判断理由，可以由金融、法律、医疗专家写带理由的评审和评分标准。
- OPD 团队合并的是各领域的专家模型，新增金融或法律专家模型就需要对应的 RL 环境和验证器。
- 见面时可以提：SimReal 在开源的 Qwen3.8-27B 上跑过交易环境 Xitadel，在没见过的真实市场数据上提升 12%。这一点不放进邮件开头。

**风险**
- 人员变动大：林俊旸、郁博文 2026-03 离职，后训练改由周浩负责，6 月又做了组织调整。联系人和决策链可能还在变。
- 自建倾向强：AgentWorld、WebWorld、RecreationWorld、E-Commerce Bench 都是自己搭的环境和世界模型。要卖的是"难以合成"的部分：专家评分标准、带理由的评审、留出评测集。
- 阿里是大公司，走采购流程可能慢；没有查到外部数据供应商的公开信息。
- 合规：本次没能核实阿里是否在美国相关限制名单上，发送前请确认。

**核实说明**：郑楚杰和林俊旸的主页，以及 QwenLM 各仓库 README，读的是原文。周浩的职务来自 LatePost 和量子位的 GitHub 存档；Qwen3.7、组织调整和离职去向来自 GitHub 上的二手研究报告，原始链接没打开。

---

## 邮件

主题：SimReal｜通义千问 后训练专家数据

郑老师您好，

看到 8 月开源的 Qwen3.8 把专业工作和长程 agent 任务列为主要提升方向，想请教一下这类任务的 RL 环境和专家数据是怎么来的。

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖金融、会计、法律、软件工程等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

郑老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？
