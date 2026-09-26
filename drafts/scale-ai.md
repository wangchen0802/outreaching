# Scale AI

- 类别：人类数据供应商｜地区：海外（美国）
- 收件人：**Yuan Xue**（英文名 Emily），Head of Enterprise AI。CliniCARE-Bench 末位作者兼论文联系人（2026-08），论文贡献说明写她 "conceived the project, defined the vision and benchmark direction, led the manuscript effort, and supervised the work"（搜索摘要）
- 置信度：中。职位由本人主页写明（"I currently serve as the Head of Enterprise AI at Scale AI"，已读 GitHub 源文件，主页标注 last updated Oct 2025）；2026-08 的 CliniCARE-Bench 仍用 scale.com 邮箱署名，说明仍在职。但她管的是企业 AI 和医疗方向的基准，不是专家供给负责人，能否拍板供给合作不确定
- 来源：
  - 本人主页：https://yuanxue.github.io/ （源文件：https://raw.githubusercontent.com/yuanxue/yuanxue.github.io/master/index.md ）
  - Scale 博客 "Closing the Gap Between AI Promise and Enterprise Reality"（入职文章，搜索摘要）：https://scale.com/blog/why-i-joined-scale-yuan-xue
  - CliniCARE-Bench 论文（作者列表和联系人来自搜索摘要）：https://arxiv.org/abs/2608.07796
  - LinkedIn 标题 "Head of Enterprise AI @ Scale AI"（搜索摘要，仅作佐证）：https://www.linkedin.com/in/yuan-emily-xue-3483012/
- 备选：
  - **Xiaote Zhu**，Outlier General Manager（置信度低）。Scale 官方博客宣布她为 Outlier 首任 GM，此前是 Head of Generative AI Operations（2024-11，X 帖子）；Forbes 2025-03 仍称她为 Outlier GM。没有找到 2025 年中之后的在职证据：https://scale.com/blog/new-era-outlier 、https://x.com/scale_AI/status/1852368047245578552 、https://www.forbes.com/sites/richardnieva/2025/03/06/scale-ai-outlier-us/
  - **Francis deSouza**，CEO（置信度高），2026-08-10 起任，前 Google Cloud COO、前 Illumina CEO：https://scale.com/blog/scale-appoints-new-ceo 、https://www.axios.com/2026/07/30/scale-ai-google-cloud-coo-francis-desouza
- 专家供给 / 合作负责人：**未找到**。Human Frontier Collective（HFC）和 Outlier 在 2026 年没有查到公开的负责人；HFC 只看到 Specialist / Research Advisor 等岗位。
- 人员变动：Alexandr Wang 2025-06 随 Meta 投资去了 Meta；Jason Droege 2025-06 起任临时 CEO，2026-08-10 由 Francis deSouza 接任（Scale 官方新闻稿、Bloomberg、Axios 一致）。

## 调研备注

**最近发布**
- **CliniCARE-Bench**（arXiv 2026-08-07）：MIMIC-IV 真实病历上的临床审核 agent 基准，25 个 scenario × 30 名患者 = 750 个 Harbor 任务，除准确率外还评证据引用、政策依据、流程和该弃权时是否弃权（README 已读）：https://github.com/scaleapi/clinicare 、https://labs.scale.com/blog/clinicare-bench 、https://arxiv.org/abs/2608.07796 。论文摘要称 25 个 scenario 为 "clinician-validated"（搜索摘要）
- **DrugDiscoveryBench**（2026-06 底，和 Phylo 合作）：82 个 Harbor 格式的早期药物发现任务，"graded by an LLM judge against expert-authored rubrics"，评分标准放在 Hugging Face 的受限数据集里（README 已读）。最强模型也只解出约一半（搜索摘要）：https://github.com/scaleapi/DrugDiscoveryBench 、https://scale.com/blog/drugdiscoverybench 、https://huggingface.co/datasets/ScaleAI/DrugDiscoveryBench
- **RSI Bench**（2026）：评估 agent 做 AI 研发的能力，公开邀请社区 "contribute tasks in their domain of expertise"，前 50 个入选任务每个 2,000 美元并给论文署名（README 已读；奖励条款来自搜索摘要）：https://github.com/scaleapi/rsi-benchmark 、https://www.rsi-benchmark.com/contribute
- 企业客户：新闻稿提到 BP、Mayo Clinic 等企业客户，以及美国和海外政府业务扩大：https://scale.com/blog/scale-appoints-new-ceo
- 早先会话还提到 SWE-Atlas、SWE-Interact、MCP Atlas，本次没有复核，未写入邮件。

**JD 里的数据需求**
- Human Frontier Collective：邀请制 fellowship，招 STEM（CS、ML、物理、生物、化学、数学、人文等）PhD、博士后和教授，Medical Fellow 要 MD/DO 且有执照，另有法律和金融方向；US 和 UK 分别招（搜索摘要）：https://hfc.scale.com/ 、https://scale.com/careers/4574113005 、https://scale.com/careers/4591782005 、https://scale.com/careers/4612329005 、https://hfc.scale.com/fellows/finance-fellow-cambridge-social
- Research Advisor - Human Frontier Collective (US)（只看到标题）：https://scale.com/careers/4693078005
- 专家页：scale.com/experts 称网络覆盖 "verified PhDs, MDs, engineers, and domain experts"，"40+ subject domains"（搜索摘要）：https://scale.com/experts
- Outlier：官方称连接了数十万贡献者、累计支付数亿美元（搜索摘要）：https://scale.com/blog/new-era-outlier

**切入点**
- 医疗和生命科学：CliniCARE-Bench 和 DrugDiscoveryBench 都要临床医生、药物化学和生物学专家出题、写评分标准、做校验，HFC 也在单独招 MD。我们的高校博士网络和医疗从业者可以补这块。
- 金融和法律：HFC 有金融和法律方向；Xitadel、财务结账环境和金融专家写的评分标准可以做成 Scale 能转售或用于企业客户的环境。
- AI 研究：RSI Bench 在外部征集 AI 研发任务，可以对上我们的 AI 研究环境和 ML 博士生。
- 交付格式：Scale 这几个基准都用 Harbor 任务格式，我们的环境和验证器可以按同样格式交付。

**风险**
- Scale 本身就是最大的专家数据供应商，是直接竞争对手；对外采购专家供给不合常规，对方可能只把我们当成人才来源。
- Meta 2025-06 投资 143 亿美元、持股 49% 后，据 Reuters 报道 Google（最大客户）计划终止合作，OpenAI、Microsoft、xAI 也在收缩；2025-07 裁员约 200 名全职员工和 500 名承包商（CNBC、TechCrunch 等）：https://www.techmeme.com/250613/p23 、https://techcrunch.com/2025/06/14/google-reportedly-plans-to-cut-ties-with-scale-ai 、https://www.cnbc.com/2025/07/16/scale-ai-cuts-14percent-of-workforce-after-meta-investment-hiring-of-wang.html 。前沿实验室数据业务的需求可能不如以前，Scale 在转向企业和政府；同时，如果我们给前沿实验室供数，经 Scale 转手可能让客户有顾虑。
- CEO 刚换人（2026-08），组织和采购决策人可能还在调整。
- 收件人不是供给负责人，可能需要她转介；Xiaote Zhu 的 2026 在职情况未确认。
- 没有查到 Scale 向外部专家供应商采购的公开报道。

**核实说明**：本环境打不开 scale.com、arXiv 和招聘网站。DrugDiscoveryBench、clinicare、rsi-benchmark 三个仓库的 README 和 Yuan Xue 主页源文件读的是 raw.githubusercontent.com 原文；CEO 更替有 Scale 官方新闻稿、Axios、Bloomberg 等多处一致；Meta 投资后的客户流失有 Reuters（经 Techmeme）、TechCrunch、CNBC 多处一致；HFC 招募领域、Xiaote Zhu 职位和 CliniCARE-Bench 作者来自搜索摘要。早先会话记录的仓库创建日期（2026-06-26、2026-08-25、2026-07-30）因 GitHub API 不可用未能复核，上面用的是发布和论文日期。发送前请确认 Yuan Xue 仍在职，并考虑请她转介专家供给负责人。

---

## 邮件

Subject: Expert data for Scale AI's post-training

Hi Yuan,

I'm [Your name], co-founder of SimReal (simreal.co), where we build RL environments, verifiers and expert data for post-training.

Professionals from Jane Street and Citadel support our work, and every environment is red-teamed before release: 400 reward-hacking attempts so far, none successful.

Saw DrugDiscoveryBench and CliniCARE-Bench both run on expert-written rubrics, and we'd like to add clinical and life-science experts to your supply. I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. We can start with a small paid pilot: high-quality data at a competitive price.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
