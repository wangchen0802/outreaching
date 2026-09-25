# Reflection AI

- 类别：frontier lab｜地区：海外（美国）
- 收件人：**Jessica Hamrick**，Skills Research Lead（Member of Technical Staff），负责后训练的推理和 agentic RL
- 置信度：中。职责写在本人主页上；"Skills Research Lead"这个头衔来自 alphaXiv，未在官方页面看到
- 来源：
  - 本人主页："Member of Technical Staff at Reflection AI… reasoning and agentic RL for post-training"：https://www.jesshamrick.com/
  - alphaXiv 主页（Skills Research Lead）：https://www.alphaxiv.org/@jessica-b-hamrick
- 备选：**Ioannis Antonoglou**，联合创始人兼 CTO，此前在 DeepMind 负责 Gemini 后训练：https://www.sierraventures.com/ascend/ioannis-antonoglou-cto-co-founder-reflection-ai
- 数据 / 人类数据负责人：**未找到**。对应岗位 Data Partnerships & Initiatives Manager 还在招人，这个位置可能空着。

## 调研备注

**最近动态**
- 截至 2026 年 8 月还没有发布基础模型。公司说今年内发布第一个开源权重模型：https://www.layer3labs.io/guides/reflection-ai-explained 、https://futuresearch.ai/reflection-ai-forecast/
- 数据策略：预训练的设计目标是"maximize downstream RL"；数据集和训练流水线不开源（CTO 访谈，2026-03）：https://www.krasa.ai/news/reflection-ai-pentagon-frontier-model-tens-trillions-tokens
- 客户集中在政府和主权 AI：美国能源部 Genesis Mission（Axios，2026-05-22）https://www.axios.com/2026/05/22/reflection-ai-genesis-mission-energy-partnership ；沙特 HUMAIN https://www.prnewswire.com/news-releases/humain-and-reflection-announce-strategic-ai-collaboration-at-leap-2026-302866134.html
- 算力：Nebius 10 亿美元协议（2026-07-14）：https://techcrunch.com/2026/07/14/reflection-inks-1b-compute-deal-with-nebius/

**JD 里的数据需求**
- Data Partnerships & Initiatives Manager：职责包括 "evaluating suppliers, negotiating agreements, and verifying deliverables"；这些数据将 "shape how our models perform on… agentic tool use, long-horizon reasoning and robust safety alignment"。https://jobs.ashbyhq.com/reflectionai/f5b95a9f-4ecf-42b2-8932-f01d48d051c0
- MTS, Data Quality Engineer (Post-training)：要为后训练和评测的大规模数据采集定义数据质量标准。https://jobs.ashbyhq.com/reflectionai/c567de5a-a599-42f7-8f74-602fab95fd17
- MTS, Post-Training："data generation pipelines, reward models, reinforcement learning algorithms"。https://jobs.ashbyhq.com/reflectionai/13e02dca-e042-4ad0-bbbe-be6b09a98211
- MTS, Evaluations："from synthetic evals to human feedback and real-world interaction data"。https://jobs.ashbyhq.com/reflectionai/075f746b-df26-4738-a44a-82e6d1d615dc

**切入点**
- 针对 agentic tool use 和 long-horizon reasoning 的 RL 环境与验证器：软件工程、AI 研究、交易（Xitadel）、预测。
- 数学证明和逻辑推理环境，对应 Hamrick 负责的推理 RL。
- 评分标准和评测集，对应数据质量和评测两个岗位。

**风险**
- 创始团队出自 Gemini 后训练，内部 RL 能力强，也在用合成数据；不过 JD 说明他们确实在找外部供应商。
- 没有查到他们和 Scale、Surge、Mercor 合作的公开报道。
- 政府和主权客户可能对专家所在地和数据安全有要求。
- 首个模型在赶发布，可能急着采购，也可能冻结与发布无关的采购。

**核实说明**：本环境的网络策略不允许直接打开大部分网页，以上内容来自搜索结果摘要，其中职位和岗位信息经过至少两次独立搜索核对。发送前建议打开来源链接复核一遍，确认岗位还在招。

---

## 邮件

Subject: Expert data for Reflection AI's post-training

Hi Jessica,

Saw Reflection is hiring a data partnerships lead to source data for agentic tool use and long-horizon reasoning ahead of your first open-weight release — curious how you're sourcing expert-built RL environments for those skills.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across software engineering, finance, mathematics, law and medicine. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
