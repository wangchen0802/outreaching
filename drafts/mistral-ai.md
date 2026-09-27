# Mistral AI

- 类别：frontier lab｜地区：海外（法国）
- 收件人：**Albert Q. Jiang**，Research Scientist，负责推理团队（reasoning team）；Magistral 作者之一
- 置信度：中。本人主页写到在 Mistral "works on the science and infrastructure of reasoning"，多个来源说他 "leads the reasoning team"，但没有官方页面确认（搜索摘要）
- 来源：https://albertqjiang.github.io/
- 备选：**Guillaume Lample**，联合创始人兼 Chief Scientist，负责科学团队：https://ainowsummit.com/speakers/guillaume-lample/
- 数据 / 人类数据负责人：**未找到**。Technical Program Manager, Human Data Annotation 岗位还在招人。岗位入职后，这个人才是最直接的采购方。

## 调研备注

**最近发布**
- **Forge**（2026-03-18）：企业用自己的数据训练模型，包括 "post-training via supervised fine-tuning and reinforcement learning pipelines"，Mistral 派科学家驻场：https://mistral.ai/products/forge/ 、https://www.datacamp.com/blog/mistral-forge
- **Mistral Medium 3.5**（2026-04 底）：把 Magistral（推理）和 Devstral（代码）合并进一个模型：https://winbuzzer.com/2026/05/02/mistral-medium-3-5-unified-flagship-chat-reasoning-code-xcxwbn/
- 金融客户：HSBC（2025-12）https://www.hsbc.com/news-and-views/news/media-releases/2025/hsbc-and-mistral-ai-join-forces-to-accelerate-ai-adoption-across-global-bank ；BNP Paribas 续约（2026-05）https://group.bnpparibas/en/press-release/bnp-paribas-and-mistral-ai-extend-their-partnership-to-support-the-next-phase-of-generative-ai-deployment-within-the-group ；ABN AMRO（2026-08）https://www.abnamro.com/en/news/abn-amro-and-mistral-enter-strategic-partnership-to-strengthen-european-ai-innovation

**JD 里的数据需求**
- Technical Program Manager, Human Data Annotation：负责 "the human data operation for model development, from eval to training"，要 "managing… contractor teams and vendor relationships… data collection campaigns with subject matter experts"。https://jobs.lever.co/mistral/5102591a-0533-4160-9b44-bb24494b9d1e
- 同类岗位的代码方向：TPM, Human Data Annotation (Code)。https://jobs.lever.co/mistral/ca5ae045-5425-42fd-a8f3-c9b3d807a540
- Lead AI Scientist, Finance (Mistral Science)："identify critical challenges in finance"，和领域专家一起工作。https://jobs.lever.co/mistral/96aff642-c48a-44ec-81d4-654d1dbc615a
- Research Engineer – Cybersecurity (RL Environments)：把领域专家的知识做成可复现的环境和数据集（搜索摘要）。https://freehire.me/jobs/research-engineer-cybersecurity-rl-environments-mistral-ai-l4b3s6bu

**切入点**
- 最匹配的是金融。银行客户多（HSBC、BNP、ABN AMRO），在招金融方向负责人，Forge 也有 RL 流水线，所以 Xitadel、财务结账环境和金融专家写的评分标准都用得上。
- 对专家 SFT、偏好数据和评测，人类数据 TPM 岗位明确要向外部供应商采购领域专家的数据采集任务。
- 代码方向有专门的人类数据岗位，可以切入软件工程环境。
- 网络安全 RL 环境是他们在招的方向，但不在我们现有领域里，先不提。

**风险**
- 自研文化强：Magistral 论文说训练 "relying solely on their own models and infrastructure"：https://arxiv.org/abs/2506.10910
- 巴黎有内部标注团队。
- 主打欧洲主权 AI，非欧洲供应商可能会被问到数据驻留。
- 没有查到供应商相关的公开报道。

**核实说明**：本环境的网络策略不允许直接打开 mistral.ai 和 Lever，以上内容来自搜索结果摘要。岗位描述在多个招聘聚合站上一致。发送前建议打开链接，确认岗位还在招。

---

## 邮件

Subject: RL environments and expert data for Mistral AI

Hi Albert,

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training.

Our founders are quants with backgrounds at Jane Street, Citadel, D. E. Shaw, Millennium and Optiver. Our trading environment, Xitadel, improved Qwen3.8-27B's trading performance by 12% on unseen market data, reproduced across independent runs; every environment is red-teamed before release, and our puzzle benchmark has held against 400 reward-hacking attempts. 7,000+ experts have signed up with us, and through 21 partner universities we can reach 200,000+ professionals.

Saw Mistral is hiring a finance lead and a program manager for expert data campaigns, and we'd like to support the finance side of that work. I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. We can start with a small paid pilot.

Open to 20 minutes next week?

Best,
[Your name]
Co-founder, SimReal
business@simreal.co | simreal.co

---

## 跟进 1（第 4 天）

Hi Albert,

Following up on my note below. If it helps, we can scope a small paid pilot around one domain you're short on and deliver within weeks. Worth 20 minutes?

Best,
[Your name]

---

## 跟进 2（第 10 天）

Hi Albert,

Last note from me. If post-training data sits with someone else at Mistral AI, I'd be grateful for a pointer. If it isn't relevant, just reply and I won't follow up again.

Best,
[Your name]
