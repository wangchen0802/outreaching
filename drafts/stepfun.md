# 阶跃星辰 StepFun

- 类别：国内大模型公司｜地区：国内（上海）
- 收件人：**焦斌星（Binxing Jiao）**，联合创始人，数据负责人；曾任微软必应核心搜索团队负责人
- 置信度：中。"数据负责人"这个说法来自 2024 年的媒体报道（量子位、财联社，搜索摘要）。2026-02 的 Step 3.5 Flash 技术报告 arXiv 作者名单里有 Binxing Jiao（搜索摘要），说明他仍在阶跃，但 2026 年的具体分工没有查到公开说法。另外，2026-01 媒体报道的"1+3"核心决策层（印奇、姜大昕、张祥雨、朱亦博）里没有他。
- 来源：
  - 量子位（2024-04）：https://www.qbitai.com/2024/04/132306.html
  - 财联社（2024）：https://www.cls.cn/detail/1627876
  - Step 3.5 Flash 技术报告（arXiv 2602.10604，作者名单，搜索摘要）：https://arxiv.org/abs/2602.10604
- 后训练 / RL 负责人：**未找到**。GitHub 仓库里的技术报告 PDF 署名为 "StepFun Team"，没有写分工（已读原文）。
- 备选：
  - **张祥雨**，首席科学家，媒体描述他负责"算法与多模态底盘"（量子位 2026-01，搜索摘要）：https://www.qbitai.com/2026/01/373038.html
  - **姜大昕**，创始人兼 CEO，印奇出任董事长后他"继续全权主持技术研发与日常经营"（搜索摘要）：https://www.nbd.com.cn/articles/2026-01-27/4237592.html
- 称呼用"焦总"，因为他是联合创始人。如果是通过技术圈引荐，也可以改成"焦老师"。

## 调研备注

**最近发布**
- **Step 5 Preview**（2026-09-19/20）：600B 总参数、27B 激活的 MoE 模型，支持 1M 上下文。官方定位是 AI 编程、软件工程、专业知识工作和金融分析，计划 10-15 开源权重，AA 智能指数 44 分（搜索摘要）：https://news.qq.com/rain/a/20260920A06SE900 、https://www.sohu.com/a/1078596495_121948396 、https://www.marktechpost.com/2026/09/20/stepfun-launches-step-5-preview/
- **Step 3.7 Flash**（2026-05-28，GitHub 首次提交）：198B MoE 视觉语言模型。README 里写的场景包括 "parsing massive financial reports in one pass"。GDPVal-AA（45.8）和 Terminal-Bench 2.1（59.5）被他们自己列为 "clear areas for future optimization"（已读原文）：https://github.com/stepfun-ai/Step-3.7-Flash
- **Step 3.5 Flash 技术报告**（2026-02，arXiv 2602.10604；PDF 在 GitHub 仓库里，已读原文）：https://github.com/stepfun-ai/Step-3.5-Flash
  - 后训练流程：先做统一 SFT，再按领域做 RL，训出数学、代码、STEM、工具调用、长上下文、人类偏好、Agentic Reasoning 等专家模型，最后用自蒸馏加规模化 RL 合并成一个通用模型。
  - SFT 第二阶段注入了约 3 万条专家级化学轨迹（"∼30K expert-level chemistry trajectories"）。
  - 奖励设计：可验证任务用规则校验，STEM 任务用模型验证器；不可验证任务用 pairwise GenRM 加 MetaRM；研究报告用 rubric-based LLM judge 打分，并把"部分满足"映射成非对称的二值奖励，原因是中间档 "often misaligns with expert preferences"。
  - 代码环境：自建 5 万个可验证环境，覆盖 1.5 万个 GitHub 仓库。
  - 下一步方向（README 和报告原文）："the next frontier of agentic AI necessitates the application of RL to intricate, expert-level tasks found in professional work, engineering, and research"。
- 其他开源：Step Code（终端编程 agent，2026-06）；SteptronOss（自研的 SFT/RLVR 训练框架，2025-12）：https://github.com/stepfun-ai/SteptronOss
- 公司动态：2026-01 印奇出任董事长。2026-05 有报道称公司完成约 25 亿美元融资、拆除红筹架构，在推进港股上市（财新，搜索摘要）：https://m.caixin.com/m/2026-05-08/102442074.html

**JD 里的数据需求**（官方 MokaHR 招聘页在本环境打不开。以下摘自 GitHub 上的第三方岗位汇总表 https://github.com/coconight01/2027-North-America-New-Grad-Jobs/blob/main/data/china_jobs.csv ，日期是表里记录的发布日期，链接是表里给出的官方 MokaHR 地址）
- 大语言模型 post-train 算法研究员（2026-05-28）："涵盖数据循环体系的构建，以及在监督微调（SFT）与强化学习（RL）阶段中对数据使用策略的系统性探究"。https://app.mokahr.com/social-recruitment/step/94904#/job/a669b7dc-a9b5-416a-baa3-e0d765d7997e
- Personal/Working Agent 研究员（2026-02-28）："探索基于人机协同的高质量工作流数据挖掘与合成，构建多步骤、跨应用、长周期的复杂工作任务数据"，以及"构建WorkingAgent自动化评测体系与沙箱环境，覆盖真实办公场景的端到端任务评测"。https://app.mokahr.com/social-recruitment/step/94904#/job/2919ede2-f6e4-4745-8354-e4ce07958771
- Coding 评测工程师（2026-08-03）："为模型在特定方向上构建完整的任务完成环境"、"构建可抵御刷分的评测体系"、"持续迭代优化Rubric标准"。https://app.mokahr.com/social-recruitment/step/94904#/job/70035a78-ca37-417d-a86c-fce18376459e
- 算法工程师（金融大模型/AI Agent 方向）（表里记为 2025-05-30，状态仍是 Open）："负责金融领域大模型的SFT（有监督微调）和GRPO（强化学习优化）全流程"、"设计和实现行业数据的标注方案、训练策略和效果评估体系"，加分项包括"CFA、FRM等金融资质"。https://app.mokahr.com/social-recruitment/step/94904#/job/21ec72f3-da3d-4731-990e-866ffdff5c7c
- 另外还在招金融投研方向的 Agent 研发工程师（2026-07-03）和金融大模型方向的解决方案工程师（2026-09-03），可以看出金融是商业化重点。
- 没有找到数据采购或供应商管理岗位。

**切入点**
- 金融专家数据和环境：Step 5 Preview 主打金融分析，内部也在招做金融 SFT/GRPO 和标注方案的人。Xitadel 和财务结账环境，再加上 CFA、会计背景专家写的评分标准，匹配度最高。
- 专业工作的 RL 任务：他们自己写了下一步要把 RL 用到专业工作的专家级任务上；Working Agent 岗位要做跨应用、长周期的办公任务数据和沙箱评测。
- 专家校准的评分标准：研究报告的奖励靠 rubric judge 打分，报告里也承认中间档和专家偏好对不上，这是明确的缺口。
- 抗刷分的留出评测集：Coding 评测岗位原话要"可抵御刷分"。
- STEM 专家轨迹：报告里用了约 3 万条专家级化学轨迹，说明他们会用这类数据，可以问来源。
- 软件工程环境他们已经自建了 5 万个，不是优先切入点。

**风险**
- 自建倾向强：SFT 数据以开源、合成和用户回流为主，环境和训练框架（SteptronOss）都是自研的。融资主要花在算力上。
- 合规：没有查到阶跃被列入美国实体清单的记录，但本环境打不开 federalregister 原文，发送前请复核。
- 数据出境：如果涉及境外专家或数据存在境外，对方可能要求数据留在境内。
- 联系人信息偏旧："数据负责人"的说法来自 2024 年，需要请引荐人确认他现在是否还管后训练数据。
- 阶跃在准备港股上市。招股书如果披露前五大供应商，可以看到他们现在用哪些数据供应商。

**核实说明**：Step 3.5 Flash 技术报告 PDF，以及 Step 3.5 Flash、Step 3.7 Flash、SteptronOss 的 README 读的是原文，仓库日期来自 git 提交记录。Step 5 Preview、联系人和融资信息来自搜索摘要。JD 来自第三方 GitHub 汇总表，官方页面没有打开。

---

## 邮件

主题：SimReal｜阶跃星辰 后训练专家数据

焦总您好，

看到 Step 5 Preview 把金融分析和专业知识工作列为重点场景，Step 3.5 Flash 技术报告里也写到下一步要把 RL 用到专业工作中的专家级任务上，想请教一下这类金融任务的专家数据和 RL 环境目前是怎么来的。

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖金融、会计、法律、软件工程等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

焦总您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？
