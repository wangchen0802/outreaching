# 九坤投资 Ubiquant（AI 研究团队 IQuest Research）

- 类别：金融机构 AI 团队｜地区：国内（北京）
- 收件人：**Bryan Dai**，九坤 AI 研究团队（IQuest Research，GitHub 组织原名 UbiquantAI）的资深研究负责人。具体头衔未找到。
- 置信度：中，依据是论文署名。他横跨推理 RL、代码、医疗三条线，多数论文里是通讯作者或末位作者；但没有找到官方页面或本人主页写明头衔。
  - One-shot EM（2505.20282）和 URM（2512.14693）的通讯作者，署名单位 Ubiquant
  - Logic-RL（2502.14768，与微软亚洲研究院合作）的作者
  - Scaling Laws for Code（2512.13472，单位 Ubiquant）、Fleming-R1、Fleming-VL 的末位作者
  - 2026-09 ModularRSI 的近末位作者
- 来源：
  - URM README（已读原文）：https://github.com/UbiquantAI/URM
  - One-shot EM README（已读原文）：https://github.com/UbiquantAI/one-shot-em
  - ModularRSI README（已读原文，署名 IQuest Research）：https://github.com/IQuestLab/ModularRSI
  - Fleming-R1 README（已读原文；仓库在 IQuestLab 名下，模型链接仍指向 UbiquantAI）：https://github.com/IQuestLab/Fleming-R1
  - 论文首页署名"Bryan Dai* Ubiquant"：arXiv 在本环境打不开，这是在 GitHub 上第三方转录的论文首页文本里看到的：https://arxiv.org/abs/2512.14693 、https://arxiv.org/abs/2505.20282
  - ICML 2026 录用列表里，One-shot EM 的 Bryan Dai 单位写的是 Ubiquant（第三方整理）：https://icml.cc/virtual/2026/poster/66725
- 备选：
  - **Yizhi Li**，IQuest Research 研究员，方向是代码大模型、终端 agent、递归自我改进和面向 LLM 的 RL。本人主页写明 "researcher at IQuest Research, UbiQuant"（已读原文）。他是 ModularRSI 的作者之一，适合技术层面对接，但不是负责人：https://github.com/yizhilll/yizhilll.github.io
  - **Joey Zhou**，Ubiquant，Logic-RL、One-shot EM、URM 的共同作者，职务未找到（低）。
  - **王琛**，九坤联合创始人、CEO，创始人级别，只作兜底。来源是一份第三方 GitHub 汇编，它引用了中证报 2022-07 的报道（二手）：https://www.cs.com.cn/tzjj/jjks/202207/t20220725_6286624.html
- 数据 / 标注负责人：**未找到**。
- 称呼：Bryan Dai 的中文名没有找到（2026-09-25 用中英文专门搜了"九坤 / IQuest / 至知创新研究院 + Bryan Dai"和研究院负责人，公开报道里没有出现他的中文名），邮件里继续用"Bryan Dai"。如果引荐时拿到中文名，再改成"X老师"。

## 调研备注

**最近发布**
- **ModularRSI**（arXiv 2609.14857，2026-09；仓库 2026-08-28 创建；已读 README）：https://github.com/IQuestLab/ModularRSI
  - 把 agent 的 harness 拆成五个可演化模块，对比成功和失败的轨迹来改进 harness，只有通过验证门控的改动才会合入。
  - 演化数据集共 2,000 个任务：1,000 个终端任务，1,000 个软件工程任务。
  - 用 DeepSeek-V4-Flash-Preview 时，Terminal-Bench 2.0 从 47.57% 提到 52.43%；改进能迁移到 SWE-Bench Verified，也能迁移到 GLM-5.2 等其他模型。
- **OTE**（arXiv 2606.13710，2026-06；已读 README）：面向开放任务 agent 的 proposer–solver–judge 协同进化框架，先用在 deep research 场景，同时发布了 HOTE-8B：https://github.com/IQuestLab/ote
- **IQuest-Coder-V1**（已读 README 和技术报告）：https://github.com/IQuestLab/IQuest-Coder-V1
  - 2026-01-01 首发 40B；2026-03-02 更新 7B、14B、40B-Thinking 和 40B-Loop-Thinking，针对工具调用和 CLI agent（Claude Code、OpenCode）做了优化。
  - README 写的成绩：SWE-Bench Verified 76.2%，LiveCodeBench v6 81.1%。
  - 后训练分两条路线：Thinking 走推理 RL，Instruct 走通用指令。
  - 社区讨论里出现过 SWE-Bench 81.4% 的说法，和 README 不一致，不要引用。
- **ClawGym**（arXiv 2604.26904，2026-05；已读 README）：合成了 13.5K 个可执行任务，每个任务配模拟工作区和混合验证，另有 24.5K 条训练轨迹。和人大 AI Box 合作，模型发布在 RUC-AIBOX 名下：https://github.com/IQuestLab/clawgym
- **TMAS**（arXiv 2605.10344，2026-05）：数学推理的多智能体 test-time scaling，配混合奖励 RL：https://github.com/IQuestLab/tmas
- **医疗和生命科学线**：Fleming-R1（2025-09，医疗推理 RL，7B/32B）、Fleming-VL、UniReason-Med（2026-06，SFT + GRPO）、UBio-ARCK（2026-06，生命科学 LLM 评测框架）、UBio-MolFM（2026-01）。
- **早期推理工作**：URM（2025-12），ARC-AGI 1 pass@1 53.8%，ARC-AGI 2 16.0%（已读 README）；One-shot EM 已被 ICML 2026 录用；Logic-RL（2025-02）是和微软亚洲研究院合作的规则奖励 RL（已读 README）：https://github.com/Unakar/Logic-RL
- **组织**：
  - IQuestLab 名下的 Fleming-R1 README 仍然链接到 UbiquantAI 组织，两个研究员的个人主页也写的是"IQuest Research, Ubiquant"，可以判断是同一个团队。
  - IQuest Research 就是"至知创新研究院"：中证报 2026-01 报道"九坤投资创始团队成立至知创新研究院，发布开源代码大模型"，称它是"由九坤投资创始团队发起设立的、独立于量化投研体系的全新平台"（搜索摘要）：https://jnzstatic.cs.com.cn/zzb/htmlInfo/112783.html ；证券时报同期报道：https://www.stcn.com/article/detail/3568306.html 。2026-06 和上海交大共建多模态大模型联合实验室（原文未读）：https://finance.sina.cn/stock/jdts/2026-01-01/detail-inheumpq8476135.d.html 、https://news.sjtu.edu.cn/jdyw/20260615/223771.html
- 公开发布里没有金融或交易方向的模型和数据集。

**JD 里的数据需求**
- 正式 JD：**未找到**。招聘页打不开，搜索额度也用完了。
- 实习生本人主页里的信号（已读原文）：
  - "Ubiquant iQuest, Post-Training Team — Agentic RL Intern, 2026.06 - Present — Scaling agentic RL systems, including auto-research, search, and code agents."：https://github.com/RTkenny/RTkenny.github.io
  - "IQuest Research, Ubiquant … LLM algorithm intern"，2026-04 入职，医疗方向（Medical Track）：https://github.com/cenweizhang/cenweizhang.github.io
- 由此看，他们有专门的后训练团队，在做 auto-research、搜索、代码三类 agent 的 RL；医疗是单独一条线。

**切入点**
- 交易和预测环境：他们公开的 RL 环境集中在代码、终端、数学和 deep research，没有金融。Xitadel 和预测环境可以作为代码以外的长程可验证环境；如果对方有顾虑，也可以只作留出评测、不进训练。
- 专家校准的 judge 和验证器：他们的路线是自动合成任务加自动验证（OTE 用 judge，ModularRSI 用验证门控，ClawGym 用混合验证）。最缺的是合成做不好的部分，也就是金融、医疗的专家评分标准、隐藏验证器和留出评测集。
- AI research 环境：后训练团队在做 auto-research agent，SimReal 的 AI research 环境可以直接对上。
- 医疗线（Fleming、UniReason-Med）需要医生写的推理评测和评分标准，可以作为第二个切入点。

**风险**
- 自建和自合成倾向很强：几乎所有工作都在用合成任务、自我演化或无监督后训练（One-shot EM）来减少对人工数据的依赖。要卖的是难以合成的东西，不是量。
- 交易数据和策略是九坤的核心机密，对方未必愿意让外部团队参与交易相关的训练。SimReal 团队的量化背景也可能引起竞争方面的顾虑。金融环境要强调通用，不碰对方的策略。
- IQuest Research 和九坤投资的法律主体关系不清楚（媒体称是创始团队新设的研究院），合同主体需要确认。
- 合规：量化私募受证监会和中基协监管，程序化交易的监管在收紧。数据出境和美国籍专家参与是否受限需要确认。是否在美国实体清单上没有核实。

**核实说明**：2026-09-25 复核：Bryan Dai 的中文名没有找到，称呼保持英文名。开头一句的 ModularRSI 数字（Terminal-Bench 2.0 从 47.57% 到 52.43%）重新读了 README 原文，一致，保留。至知创新研究院的来源换成中证报和证券时报的原始报道。这份草稿里没有新闻类的 GitHub 镜像链接（GitHub 链接都是一手的仓库 README 或个人主页）。以下为原调研说明。GitHub README（IQuest-Coder-V1、ModularRSI、OTE、ClawGym、TMAS、URM、One-shot EM、Fleming-R1、Logic-RL）、IQuest-Coder 技术报告 PDF 和三个个人主页读的是原文。Bryan Dai 的单位来自第三方转录的论文首页和 ICML 2026 列表，头衔未找到。至知创新研究院、上海交大联合实验室和王琛的信息来自第三方 GitHub 汇编，属于二手。

---

## 邮件

主题：SimReal｜九坤 后训练专家数据

Bryan Dai 您好，

看到 IQuest Research 9 月发布的 ModularRSI，用终端和软件工程任务演化 agent harness，把 Terminal-Bench 2.0 从 47.57% 提到 52.43%，想请教一下这类可验证任务和验证器往代码以外、比如交易和预测场景扩展时，是怎么搭建的。

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖金融、量化交易、医疗、软件工程等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

Bryan Dai 您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？
