# Google DeepMind

- 类别：frontier lab｜地区：海外（英国/美国）
- 收件人：**Tulsee Doshi**，Senior Director，Gemini 模型产品负责人（Head of Product, Gemini Models）
- 置信度：中。职位来自搜索结果摘要（Google 官方作者页、Fast Company、CNBC）。2026-09-02 她还以这个身份就 Flash 模型接受 CNBC 采访，说明目前在职。她管产品，不直接管数据采购，更可能把邮件转给 Gemini Data 团队
- 来源：
  - Google 官方作者页（搜索摘要）：https://blog.google/authors/tulsee-doshi/
  - Fast Company 采访（搜索摘要）：https://www.fastcompany.com/91545807/google-deepminds-tulsee-doshi-says-says-ais-next-phase-depends-on-user-trust
  - CNBC 2026-09-02，引用她对 Flash 模型的评价（搜索摘要）：https://www.cnbc.com/2026/09/02/google-starts-september-with-ai-momentum-after-long-losing-streak.html
- 备选：
  - **Kalpesh Krishna**，Staff Research Scientist，在 Gemini 后训练团队做指令遵循和通用质量。本人主页写明 "Our team works on improving instruction following and general model quality of the Gemini models in the post-training phase"（已读原文，页面更新时间不明）：https://martiansideofthemoon.github.io/
  - **Koray Kavukcuoglu**，2026-08 起任 SVP，接管 Google DeepMind，负责 Gemini 模型开发（兜底联系人，级别太高）：https://www.cnbc.com/2026/08/12/google-deepmind-koray-kavukcuoglu.html
- 数据 / 人类数据负责人：**未找到**。Gemini 有独立的 Data 团队（Product Manager, Gemini Data 岗位描述里提到 "the core Data team"），还在招 Business Development Lead, Data for Gemini，负责第三方数据合作。实际采购对接人应该在这两个岗位所在的团队里，但没有查到具体名字。2023 年 Gemini 1.0 报告里署名的人类数据负责人是 Amelia Glaese，这个信息已经过时，不作为联系人。
- 人员变动：2026-08-05 Demis Hassabis 改任 Google DeepMind 董事长兼 Alphabet 首席科学家，Koray Kavukcuoglu 接管 Google DeepMind；Jeff Dean 同时离开 Google（https://www.cnbc.com/2026/08/05/google-chief-scientist-jeff-dean-leaving-company-after-27-years.html ）。Fortune 报道一个月内有四位资深研究员离开（https://fortune.com/2026/08/27/google-deepmind-losing-talent-to-rival-ai-labs-startups-new-data-show/ ）。

## 调研备注

**最近发布**
- **Gemini 3.8 Flash / 3.8 Flash Cyber**（2026-09-02）：官方博客写到，3.8 Flash "outperforms 3.7 Flash and other frontier models in benchmarks like Vals Finance Agent V2 and Harvey's Legal Agent Benchmark"，HLE-Verified 54.9%。3.8 Flash Cyber 通过 Fairwind Program 只开放给受信任的防御方：https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ 、模型卡 https://deepmind.google/models/model-cards/gemini-3-8-flash/
- **Gemini 3.7 Flash**（2026-08-13）和 **3.6 Flash**（2026-07-21，日期来自二手摘要）：六周内发了三版 Flash，3.7 Flash 的改进包括文档和业务流程类任务：https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/
- **Gemini 4 进入后训练**（2026-09-23/24）：Kavukcuoglu 在 The Information 的活动上说，Gemini 4 处于早期后训练阶段，计划尽快放出早期版本，"much earlier" than 年底：https://the-decoder.com/deepmind-was-built-to-chase-agi-but-its-new-chief-just-wants-gemini-4-out-the-door/ 、https://dataconomy.com/2026/09/25/deepmind-says-gemini-4-is-coming-much-earlier-than-expected/
- **Gemini Enterprise for Legal**（Google Cloud，2026-08 前后）：法律行业套件：https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-for-legal

**JD 里的数据需求**（均来自搜索摘要，发布日期不明，发送前确认是否还在招）
- Business Development Lead, Data for Gemini："sourcing and securing third-party data partnerships to power Google DeepMind's foundational AI models, particularly Gemini"，要 "translating research needs into data acquisition strategies"，维护 "a pipeline of data assets aligned with Gemini's Core Capability priorities"。https://www.google.com/about/careers/applications/jobs/results/86359363714720454-business-development-lead-data-for-gemini （另有 Principal Lead 级别：https://www.google.com/about/careers/applications/jobs/results/84341000473846470-business-development-principal-lead/ ）
- Product Manager, Gemini Data：属于 "the core Data team"，负责 "generating the necessary volume, types, and quality of data aligned with Gemini's priority capabilities"。https://job-boards.greenhouse.io/deepmind/jobs/6891840
- Senior Product Manager, Gemini Post Training：嵌入训练流程，要能 "engage in substantive training discussions regarding data quality and trade-offs with researchers"。https://careers.google.com/jobs/results/119310585912271558-senior-product-manager/
- Research Scientist, Agent Post-Training（只看到标题）：https://www.google.com/about/careers/applications/jobs/results/133175271845962438-research-scientist-agent-posttraining-deepmind

**切入点**
- Gemini 规模大，通用标注和大批量 RLHF 已经有长期供应商，SimReal 抢不了这块。现实的位置是金融这个窄领域：3.8 Flash 公开拿 Vals Finance Agent V2 当卖点，Xitadel、财务结账环境和金融专家写的评分标准可以直接对上金融 agent 的训练和评测。
- 法律是第二个方向：Harvey Legal Agent Benchmark 和 Gemini Enterprise for Legal 都说明在投入，可以提供律师写的评分标准和评测集。
- 形式：先做一个小批量金融 agent 任务集，带验证器，同时交付一份留出评测集，让他们自己跑分判断。
- 对接路径：邮件发给 Tulsee，请她转 Gemini Data 团队的 PM；同时关注 Data for Gemini BD 岗位，这个岗位的职责就是对接外部数据合作方。

**风险**
- 已有供应商：Gemini 的评分员外包给 Hitachi 旗下的 GlobalLogic（2024-12 报道：https://www.msn.com/en-us/news/technology/exclusive-google-s-gemini-is-forcing-contractors-to-rate-ai-responses-outside-their-expertise/ar-AA1w7FUT ）。二手行业文章说 Surge 是 Gemini 团队的首选供应商（https://www.teahose.com/guides/scale-ai-competitors ）。Google 曾是 Scale AI 最大的客户，Meta 入股 Scale 后撤出（CNBC 2025-06-14：https://www.cnbc.com/2025/06/14/google-scale-ais-largest-customer-plans-split-after-meta-deal.html ）。
- 越来越依赖自动化：3.8 Flash 的博客写到训练用了 "long-running agentic loops designed to recursively evaluate and refine the underlying models"。
- Google 的供应商准入流程重（安全和隐私审查），试点周期可能比创业公司长，这一点是推测。
- 组织在调整：8 月换帅，Jeff Dean 离职，人才流失有报道。SemiAnalysis 付费文章的二手摘要说 GDM 的 RL 工作"太分散"，还流失了 RL 人才（https://raw.githubusercontent.com/hczhu/stock-research/main/memos/2026-07-13-semianalysis-meta-superintelligence-1yr-update.md ，观点，非事实）。
- Data for Gemini BD 岗位偏数据授权（买现成数据集），不一定管专家服务，可能会被转来转去。

**核实说明**：本环境的网络策略不允许直接打开 blog.google、Google Careers 和新闻站。3.8 Flash 的博客原文是在 GitHub 上的全文镜像里读的（https://github.com/ia3andy/devoured/blob/main/templates/full-content/2026-09-03/ai-7.html ），和另外两个独立来源一致。Kalpesh Krishna 的主页读的是原文。其余联系人和岗位信息来自搜索摘要。会话的搜索额度已用完，没能进一步确认 Gemini Data 团队负责人的名字。

---

## 邮件

Subject: Expert data for Google DeepMind's post-training

Hi Tulsee,

Saw Google report that Gemini 3.8 Flash beat 3.7 Flash and other frontier models on Vals Finance Agent V2 and Harvey's Legal Agent Benchmark — curious how you're sourcing finance and legal expert data for Gemini post-training.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, accounting, law and software engineering. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
