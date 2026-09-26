# Harvey

- 类别：垂直 AI（法律）｜地区：海外（美国）
- 收件人：**Niko Grupen**，Head of Applied Research。LAB（Legal Agent Benchmark）作者之一，Harvey 和 Applied Compute、Fireworks、Baseten 合作的几轮后训练都由他出面发布
- 置信度：高。Harvey 官方博客作者页写明 Head of Applied Research（搜索摘要，harvey.ai 在本环境打不开）。2026-09-08 他本人还在 X 上发 Harvey 的 RLM 后训练研究，说明仍在职
- 来源：
  - 官方作者页：https://www.harvey.ai/blog/author/niko-grupen
  - LAB 发布文章（作者 Niko Grupen、Gabe Pereyra、Julio Pereyra，2026-05-06，搜索摘要）：https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark
  - 本人 X 帖（2026-09-08）：https://x.com/nikogrupen/status/2097369705791307952
- 备选：
  - **Adam Sadovsky**，Chief Research Officer，2026-09 入职，负责 Harvey 全部研究。之前在 Microsoft AI 和 Google DeepMind 共同负责后训练，在 Microsoft AI 任 CVP 时参与 MAI-Thinking-1（搜索摘要）：https://www.harvey.ai/blog/harvey-appoints-adam-sadovsky-as-chief-research-officer 、https://www.benzinga.com/markets/private-markets/26/09/61827754/legal-ai-startup-harvey-hires-chief-research-officer-from-microsoft
  - **Julio Pereyra**，LAB 作者之一，负责任务设计，搭了一条文档和场景生成流水线来批量造任务（搜索摘要）。职位没查到：https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark
- 数据 / 人类数据负责人：**未找到**。律师出身的 Applied Legal Researcher 团队在做偏好数据和评分标准，没查到这个团队的负责人。
- 人员变动：2026-09 新设 Chief Research Officer，Niko 现在大概率向 Adam Sadovsky 汇报，研究方向可能会调整。

## 调研备注

**最近发布**
- **LAB**（2026-05-06）：开源的法律 agent benchmark。首版 1,200+ 个任务，覆盖 24 个执业领域，75,000+ 条专家写的评分标准，全部通过才算过（all-pass）：https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark 。GitHub README 现在显示 1,671 个任务、"24 + contracting" 个领域。每个任务是一个 `task.json`（指令、案卷文件、pass/fail 评分标准），由两个 LLM 裁判打分（默认 claude-sonnet-4-6 和 gpt-5.5）。贡献规则要求只用虚构的当事人和案情（已读原文）：https://github.com/harveyai/harvey-labs 。第三方榜单：https://artificialanalysis.ai/evaluations/harvey-lab-aa 、https://www.vals.ai/benchmarks/hlab
- **和 Applied Compute 合作的法律 agent**（2026-06-22 前后）：在 GLM-5.1 上后训练，评分标准通过率从 0.853 升到 0.913，all-pass 率从 0.059 升到 0.126，超过 Opus 4.8 Max 和 GPT-5.5 xhigh（搜索摘要）：https://www.harvey.ai/blog/training-a-legal-agent-with-applied-compute 、https://www.appliedcompute.com/case-studies/harvey 。2026-08-14 又宣布给 Review Tables 后训练了一个模型，成本降一半（搜索摘要）：https://x.com/harvey/status/2088322498001846668
- **Tenet**（2026-08-20）：Harvey 第一个自己后训练的模型，研究预览版。基座是 Kimi K3，和 Fireworks 用异步 RL 训练。Harvey 说训练语料是 "publicly available legal data, synthetic data, and human expert data simulating long-horizon legal work"，没用客户数据。相对基座，LAB all-pass 率提升 82%，LAB Contracts 提升 22%，成本不到头部模型的四分之一（搜索摘要）：https://www.harvey.ai/blog/post-training-update-harvey-tenet 、https://x.com/harvey/status/2090454750059958440 、https://fireworks.ai/blog/post-training-kimi-k3-with-harvey-for-long-horizon-legal-work 、https://www.marktechpost.com/2026/08/23/harvey-tenet-post-trained-kimi-k3-legal-agent-model/
- **M&A 尽调的 RLM agent**（2026-09-08，和 Baseten 合作）：整个数据室载入 Python REPL，由主 agent 分派子 agent。对 Qwen3.5-122B-A10B 做 RL 后，在 50 个预留的 LAB Diligence 数据室上，评分标准通过率从 29.9% 升到 63.0%（搜索摘要）：https://www.harvey.ai/blog/post-training-rlm-agents-for-m-and-a-diligence 。更早还有一篇 Baseten 合作文章：https://www.harvey.ai/blog/post-training-open-legal-agents-with-baseten-research
- 2026-09-09 宣布以 155 亿美元估值融资 5.5 亿美元，Diffusion 和 Lightspeed 领投（官方博客和 TechCrunch 在搜索结果里一致；Bloomberg 标题写 156 亿）：https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence 、https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/

**JD 里的数据需求**
- Applied Legal Researcher（搜索摘要，未见原文）：要做 "collection of human preference data, rubric-based evaluation, and golden data to build bespoke datasets for AI development"，还要 "building proprietary benchmarks and datasets to evaluate model performance"。https://jobs.ashbyhq.com/harvey/a35efd1c-e5ad-4556-bfa4-d2e13f8b7f1c 。这个岗位 2024-01 就在 LinkedIn 上发过，可能是常年招的岗位。
- Harvey Research 页面：研究方向是 "synthetic and human data, post-training, agent harness optimization, verification"（搜索摘要）。https://www.harvey.ai/research
- 没找到研究工程师或人类数据运营岗位的 JD。

**切入点**
- 最直接的是长程任务和评分标准。Tenet 明确用了 "human expert data simulating long-horizon legal work"。LAB 的任务格式是公开的，我们的律师可以直接按 `task.json` 格式写新任务和 pass/fail 评分标准，覆盖它们还薄的领域和法域。
- 并购尽调和财务：LAB 里有 QoE（盈利质量）对账这类任务，RLM 研究也是在尽调数据室上做 RL。财务结账和会计环境、会计和财务专家写的评分标准都能用上。
- 偏好数据和产出物评审：Applied Legal Researcher 岗位写明在收集人类偏好数据。可以提供按固定标准给备忘录、合同修订稿打分的执业律师。
- 税务和合规：Harvey 的定位是 "legal and professional services"，这两块可以作为扩展领域。
- Xitadel（交易）和他们关系不大，不提。

**风险**
- 内部律师多：Applied Legal Researcher 团队、来自顶级律所的 Legal Engineer，LAB 的评分标准也是内部专家写的。Julio Pereyra 那条场景生成流水线说明他们合成数据能力也强，外包需求可能只是扩量或补领域。
- 训练合作方（Applied Compute、Fireworks、Baseten）是算力和训练平台，不是数据供应商。没有查到数据供应商相关的公开报道。
- 专家门槛高：客户主要是大所，要有美国、英国等法域执业资格和大所经验的律师。发送前要确认我们在这类法律专家上的供给。
- 保密要求：只能用虚构案情，不能碰客户材料。
- 新 CRO 刚到，研究优先级和采购决策人可能会变。

**核实说明**：harvey.ai、新闻网站和招聘网站在本环境打不开。LAB 的 GitHub README、CONTRIBUTING 和评测方法文档读的是原文（raw.githubusercontent.com），其余来自搜索结果摘要，并经过交叉核对。X 帖子的日期是从帖子 ID 换算出来的。本次会话的搜索额度在调研中途用完，Julio Pereyra 的职位和 Applied Legal Researcher 岗位是否还在招都没能再查。发送前建议打开 Tenet 的博客原文，确认措辞。

本次复核（2026-09-25，4 次 WebSearch，网站仍打不开，均为搜索摘要）：
- 联系人：Harvey 官方作者页、Google Cloud Next 讲者页、The Org 都写 Niko Grupen 是 Head of Applied Research；搜索摘要显示他是 Tenet 发布文章的作者之一，2026-09 初还以 Harvey 身份点评 GPT-6 Astra（Artificial Lawyer 2026-09-07）。没有查到离职消息。
- 开头一句：Harvey 官方 X 帖原文是 "post-trained with @FireworksAI_HQ on a corpus of publicly available legal data, synthetic data, and human expert data simulating long-horizon legal work"，Harvey 博客、Fireworks 博客、MarkTechPost 的搜索摘要说法一致。开头一句不改。
- 融资：原备注写的"155 亿"对得上官方博客，补了官方链接和日期。
- 来源链接里没有 GitHub 转载的新闻，无需替换。

---

## 邮件

Subject: Expert data for Harvey's post-training

Hi Niko,

I'm [Your name], co-founder of SimReal (simreal.co), where we build RL environments, verifiers and expert data for post-training.

Professionals from Jane Street and Citadel support our work, and every environment is red-teamed before release: 400 reward-hacking attempts so far, none successful.

Saw Tenet was post-trained on expert data simulating long-horizon legal work, and we'd like to help supply that data as RL expands across practice areas. I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. We can start with a small paid pilot: high-quality data at a competitive price.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
