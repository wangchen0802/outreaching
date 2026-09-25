# Thinking Machines Lab

- 类别：frontier lab｜地区：海外（美国）
- 收件人：**Tianle Li**，Member of Technical Staff，负责后训练下的 Code & Autoresearch 团队；Inkling 和 Inkling-Small 的发布负责人（release DRI）
- 置信度：高。本人主页写明："release DRI for the Inkling and Inkling-Small models and led post-training model integration. I currently lead the Code & Autoresearch team within Post-training."（已读原文）
- 来源：https://codingwithtim.github.io/
- 备选：
  - **John Schulman**，联合创始人兼 Chief Scientist。2026-07 在 X 上发帖说 "a small team built up the coding, reasoning, and agentic training"（搜索摘要）：https://x.com/johnschulman2/status/2077460227327467982
  - **Soumith Chintala**，CTO（2026-01 上任，搜索摘要）：https://x.com/miramurati/status/2011577319295692801
- 数据 / 人类数据负责人：**未找到**。Data Operations 岗位还在招人。
- 人员变动：2026 年 1 月 Barret Zoph、Luke Metz、Sam Schoenholz 去了 OpenAI（https://fortune.com/2026/01/16/mira-murati-thinking-machines-staff-defections-openai-zoph-metz-schoenholz/ ）；2026 年 7 月 Lilian Weng 离职（https://techcrunch.com/2026/07/29/thinking-machines-co-founder-lilian-weng-left-the-company-citing-health-reasons-then-joined-openai/ ）。发邮件前再确认一下收件人是否还在职。

## 调研备注

**最近发布**
- **Inkling**（2026-07-15）：约 1T 参数（975B 总参数，41B 激活），开源权重，多模态，1M 上下文。模型卡写到，后训练的大部分算力用于 RL，"large-scale RL on synthetic and human-created environments"，超过 3,000 万次 rollout：https://thinkingmachines.ai/model-card/inkling/ 、https://thinkingmachines.ai/news/introducing-inkling/
- 用 Tinker 和 OpenEnv 做后训练（Hugging Face 博客，已读原文）：https://huggingface.co/blog/thinkingmachines-inkling
- 同一篇博客的评测表里，Inkling 的专业领域 agent 任务分数偏低：Tau 3 Banking 23.7%（GPT 5.6 Sol 33.0%），GDPVal-AA v2 1233（Claude Fable 5 1760）。数学已经很强：AIME 2026 97.1%。
- **Inkling-Small**（2026-07-30）：从 Inkling 做 on-policy 蒸馏，再加两周 agentic coding RL：https://thinkingmachines.ai/news/inkling-small/
- 训练框架 tinker-cookbook 定义了 `Env` / `EnvGroupBuilder` 接口，也有 rubric 打分的示例。我们的环境可以直接按这个格式交付：https://github.com/thinking-machines-lab/tinker-cookbook

**JD 里的数据需求**
- Research, Post-Training Data："combining human feedback, preference data, and synthetic examples"。https://job-boards.greenhouse.io/thinkingmachines/jobs/5002056008
- Data Operations："scoping well-run data labeling or collection campaigns"，并负责供应商管理。https://jobs.ashbyhq.com/ThinkingMachines/28e2d71f-dabd-4745-9903-9b363979f0aa
- Research, Coding Agents："owns the full coding post-training stack including RL environments and sandboxes, reward and grading design"。https://jobs.ashbyhq.com/ThinkingMachines/71c91050-688e-45e9-b98e-891b82d693e8
- Research, Post-Training Evals：要为后训练建内部评测。https://jobs.ashbyhq.com/ThinkingMachines/602f2a99-34eb-4fde-9eec-b4945ee4aab6

**切入点**
- 收件人团队最直接相关的是软件工程和 AI 研究的 RL 环境与打分器。
- 金融和专业工作类环境（Xitadel、财务结账），对应 Tau 3 Banking 和 GDPVal 上的差距。
- 专家写的评分标准和评测集，对应 Post-Training Evals 岗位。
- 数学不是优先项，他们在这方面已经很强。

**风险**
- 内部工具链完整（Tinker、OpenEnv），SFT 用开源教师模型生成的合成数据，还在 OpenRouter 上免费开放模型来收集 agent 数据，控制成本的倾向明显。
- 没有查到供应商相关的公开报道。
- 人员流动大（约三分之一创始成员已离开，https://americanbazaaronline.com/2026/05/14/one-third-of-thinking-machines-lab-founding-team-exits-480782/ ）。

**核实说明**：Tianle Li 的主页和 Hugging Face 博客读的是原文，其余来自搜索结果摘要，并经过交叉核对。

---

## 邮件

Subject: Expert data for Thinking Machines Lab's post-training

Hi Tianle,

Saw that most of Inkling's post-training compute went to RL on synthetic and human-created environments — curious how you're sourcing the human-created ones for code and autoresearch.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across software engineering, machine learning research, finance and mathematics. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
