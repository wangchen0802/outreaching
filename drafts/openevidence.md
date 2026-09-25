# OpenEvidence

- 类别：垂直 AI（医疗）｜地区：海外（美国）
- 收件人：**Samuel (Sam) Finlayson**，SVP of Medical AI。医生（儿科和临床遗传学）兼 ML 研究者，Harvard/MIT MD-PhD，NEJM AI 副主编，同时在 Seattle Children's 出诊
- 置信度：高。本人主页写明 "SVP of Medical AI at OpenEvidence"，"he helps lead work spanning AI product development, clinical data science, strategy, and partnerships"（已读原文）
- 来源：https://sgfin.github.io/ （通过 raw.githubusercontent.com/sgfin/sgfin.github.io 读的源码）
- 称呼：主页上他自称 "Sam Finlayson"，邮件用 Sam
- 备选：
  - **Zachary (Zack) Ziegler**，联合创始人兼 CTO，Harvard ML 博士背景，负责技术和模型（搜索摘要）：https://research.contrary.com/company/openevidence 。第三方竞品报告（2026-07-25）也写他是 co-founder/CTO
  - **Ania Bilski, MD**，VP of Clinical AI，急诊医生。头衔出自 PYMNTS 2026-05 的 Voice Mode 报道（经 Machine Herald 转引，未见原文）：https://www.pymnts.com/healthcare/2026/openevidence-brings-hands-free-medical-ai-to-860000-clinicians/ 。另一份第三方报告（2026-05-25）引用 About 页，把她列为 medical advisor（UCSF & Kaiser）
- AI / ML 负责人：没找到单独的 Head of ML 或 Head of Research，纯技术方向兜底找 CTO Ziegler。数据 / 人类数据负责人：**未找到**。
- 其他：据第三方报告转引，About 页还列出 CMO **Travis Zack**（未见原文）。
- 公司变动：2026-09 有报道说 OpenEvidence 以 150 亿美元估值低调融了 2.5 亿美元，创始人在考虑出售（Business Insider，经新闻摘要转引）：https://github.com/prajwalgajakesari/the-vault-ai/blob/main/editions/2026/09/24/stories/02-openevidence-250m-15b-valuation-sale-talks.md 。另一份摘要说这条消息还没有确认：https://github.com/guzus/ai-research-arm/blob/main/research/digest/2026-09-25-digest.md

## 调研备注

**最近发布**
- **Series D**（2026-01-21）：以 120 亿美元估值融 2.5 亿美元，Thrive 和 DST 领投。新闻稿说 OpenEvidence 协调 "an orchestra" 个自研的医学专科模型，每个模型负责一个子专科，由一个 "conductor" 把问题分给最合适的模型（第三方竞品报告转引）：https://www.businesswire.com/news/home/20260121029132/en/OpenEvidence-Raises-$250-Million-to-Build-Medical-Superintelligence-for-Doctors 。Nadler 在 JPM26 上说 "the lion's share" 会投到训练新模型和算力（经新闻摘要转引 Fierce Healthcare）：https://www.fiercehealthcare.com/ai-and-machine-learning/jpm26-openevidence-makes-case-ai-powered-medical-superintelligence
- 2026 上半年的官方公告（标题和日期来自官方公告页的 GitHub 镜像，https://github.com/api-evangelist/openevidence/tree/main/blogs ）：
  - 2026-01-20 "45 Rwandan Clinicians Are Helping Shape Medical AI for Low-Resource Settings"：请当地临床医生参与塑造模型
  - 2026-03-25 Coding Intelligence（医疗编码）；2026-04-07 DotFlows（自然语言自定义工作流）；2026-04-27 接入 NCCN 肿瘤治疗路径
  - 2026-02-11 Sutter Health、2026-03-31 Mount Sinai（嵌入 Epic）
  - 2026-05-20 和 Cedars-Sinai 合作做 "Patient-Aware Clinical Intelligence With Agentic Clinical AI"，同一天上线 Voice Mode。患者数据只用于当次会话，不存储、不用于训练（Machine Herald 汇总 Cedars-Sinai 新闻稿和 HIT Consultant）：https://www.openevidence.com/announcements/openevidence-partners-with-cedars-sinai-to-create-patient-aware-clinical-intelligence-with-agentic-clinical-ai
- **EvidenceGrade**（2026-07-10）：在每个 AI 回答下面，给引用的证据按 A–D 评级，单篇文献和整体证据都评，基于 GRADE 框架。据一篇案例分析转述，Finlayson 在公告里说正式的专家证据分级只能覆盖一小部分问题，EvidenceGrade 是把这套方法规模化，并会根据临床社区的反馈迭代：https://www.openevidence.com/announcements/openevidence-launches-evidencegrade-empowering-physicians-to-see-the-strength-of-cited-evidence-beneath-each-ai-answer 、https://www.techtarget.com/healthtechanalytics/news/366645822/OpenEvidence-adds-real-time-evidence-quality-grading-to-AI 、https://www.openevidence.com/blog/introducing-evidencegrade-grading-the-strength-of-medical-evidence-in-real-time
- 评测争议（2026-06）：Nature Medicine 上的一篇论文说通用大模型在医学 benchmark 上超过 OpenEvidence 等专科工具。OpenEvidence 公开反驳，说题目有污染、HealthBench 的评分标准偏文风、没有预留测试集，评测应该贴近真实临床使用的分布（出自一篇第三方博客的转述）：https://www.nature.com/articles/s41591-026-04431-5 、https://github.com/galsapir/sparse-thoughts/blob/main/_posts/2026-06-14-what-did-they-actually-measure.md
- 规模：2026-05 有 86 万名经过认证的美国临床医生在用，每天超过 100 万次提问（PYMNTS，经 Machine Herald 转引）。

**JD 里的数据需求**
- Research Scientist（Ashby）：岗位描述写 "We are a $12B company with a 30 person engineering team from MIT, Harvard, and Stanford"，强调评测和定量证明（来自两份第三方报告的引用，未见原文）：https://jobs.ashbyhq.com/openevidence/80ca886f-2c07-43b2-8978-07c37542a207
- Software Engineer, Data Infrastructure：https://jobs.thrivecap.com/companies/openevidence-2/jobs/81122458-software-engineer-data-infrastructure
- 2026-05-23 的快照里，Ashby 上 10 个岗位全是工程岗（第三方尽调报告）。没找到人类数据、标注或临床审核相关的岗位。

**切入点**
- 最直接的是专科医生写的评测集和校准集。EvidenceGrade 自己承认专家分级覆盖不了大部分问题；他们反驳 Nature Medicine 论文时也强调评测要贴近真实临床使用。可以按专科提供医生写的临床问题、参考答案和评分标准，覆盖引用是否准确、证据等级判断是否合理。
- 子专科模型的 SFT 和偏好数据：Series D 说模型按子专科拆分，每个子专科都需要对应的专科医生写示范答案、做偏好比较。
- agent 任务：DeepConsult 和 Cedars-Sinai 的 "agentic clinical AI" 需要多步的临床检索和综合任务，可以做成医生写评分标准的 RL 任务和评测。
- 医疗编码：Coding Intelligence 可以用编码和计费专家做数据和评测。
- 交易和财务环境和他们无关，不提。

**风险**
- 医生资源本身就很强：86 万名认证医生用户、很大的医学顾问网络、医生出身的管理层。他们自己招医生做审核并不难，外包的理由要落在速度、专科覆盖和量上。
- 产品只面向美国临床医生，数据需要熟悉美国指南和执业习惯的医生来做。发送前要确认我们在美国执业或美国受训医生上的供给。
- 核心是授权内容（NEJM、JAMA、NCCN、Wiley/Cochrane）加检索，后训练做了多少没有公开，没有模型卡。工程团队约 30 人。
- 合规要求严：HIPAA，患者数据不用于训练。外部专家只能用虚构或去标识化的病例。
- 对信息外泄很敏感：2025 年起诉 Doximity，指控对方冒充医生用 prompt 套取商业机密。
- 有出售传闻，采购决策可能暂停或换人。

**核实说明**：openevidence.com、Ashby、新闻网站在本环境都打不开，本次会话的搜索额度在调研 OpenEvidence 时只用了一次就耗尽。Finlayson 的主页读的是原文。其余信息来自 GitHub 上能读到原文的二手材料：官方公告页的镜像（只有标题和日期）、Machine Herald 的报道（2026-05-22，附来源列表）、一篇 EvidenceGrade 案例分析（https://github.com/archlizheng/AIPM-Wiki/blob/main/docs/03-case-studies/vertical/openevidence.md ）、一份 2026-07-25 的竞品报告（https://github.com/SONIC445-BYTE/Dissection/blob/main/All%20research%20report/dissection/workspace-019f9858-be62-7019-9698-2ca9db15e647/openevidence_ci/OpenEvidence_Competitive_Intelligence_Report_2026-07-25.md ），以及两份 2026-05 的第三方尽调报告（vibewatch）。开场白用的 EvidenceGrade，是由案例分析和竞品报告这两份互相独立的材料确认的，两份都引用了官方公告或官方博客。发送前建议打开 EvidenceGrade 的官方公告核对一遍。

---

## 邮件

Subject: Expert data for OpenEvidence's post-training

Hi Sam,

Saw OpenEvidence launched EvidenceGrade to grade the strength of the evidence beneath each answer — curious how you're sourcing the specialist physicians who calibrate and evaluate it.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across clinical medicine, pharmacy, nursing and biomedical research. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
