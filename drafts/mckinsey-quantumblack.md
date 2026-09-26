# McKinsey – QuantumBlack

- 类别：咨询公司 AI 团队｜地区：海外（美国）
- 收件人：**Tomás Lajous**，Senior Partner，QuantumBlack Labs 全球负责人。Labs 是 QuantumBlack 的研发和软件开发中心，负责自研工具和资产。
- 置信度：中。AI Magazine 2026 年的报道引用他的话时，头衔写的是 "Senior Partner and Global Leader of QuantumBlack Labs"；McKinsey 官网 Labs 页面出现在同一组搜索结果里；他本人的 LinkedIn 帖子写 "I am excited to join QuantumBlack Labs as Global Leader"（约 2025-01，搜索摘要）。以上原文都没有打开。他是否直接负责模型评测或微调，没有查到。
- 来源：
  - McKinsey 官网个人页，搜索摘要写他是纽约的 Senior Partner、QuantumBlack Labs 全球负责人（搜索摘要）：https://www.mckinsey.com/our-people/tomas-lajous
  - https://aimagazine.com/news/quantumblack-a-global-force-in-agentic-ai-transformation （搜索摘要）
  - https://www.mckinsey.com/capabilities/quantumblack/labs （搜索结果）
  - https://www.linkedin.com/posts/tomaslajous_i-am-excited-to-join-quantumblack-labs-as-activity-7287499245123715074-7hRQ （搜索摘要，仅作佐证）
- 备选：
  - **Alex Singla**，Senior Partner，QuantumBlack 全球（联席）负责人（搜索摘要）：https://www.mckinsey.com/our-people/alex-singla
  - **Alexander Sukharevsky**，Senior Partner，QuantumBlack 全球联席负责人。能找到的最新来源是 2025-06，没有查到离职消息，也没有 2026 年的在职确认：https://www.mckinsey.com/our-people/alexander-sukharevsky
  - Lilli 方向：**Kitti Lakner**，Associate Partner，官网简介写她负责 Lilli 的开发（搜索摘要，日期不详）：https://www.mckinsey.com/our-people/kitti-lakner
- 模型评测 / 微调负责人：**未找到**。调研中途 WebSearch 额度用完，这一项没能单独检索。

## 调研备注

**最近发布**
- **McKinsey Google Transformation Group**（2026-04-22，Cloud Next '26）：QuantumBlack 技术人员和 Google 的 forward-deployed engineers 一起做客户用例，联合团队做行业 agent。据新闻稿，Google DeepMind 会向 McKinsey 提前开放 Gemini 等前沿模型，McKinsey 的反馈用于改进这些模型（搜索摘要）：https://www.googlecloudpresscorner.com/2026-04-22-McKinsey-and-Google-Cloud-Launch-the-McKinsey-Google-Transformation-Group-to-Scale-Enterprise-Impact-for-the-AI-era 、https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-and-google-cloud-launch-the-mckinsey-google-transformation-group-to-scale-enterprise-impact-for-the-ai-era
- **OpenAI Frontier Alliance**（2026-02-23）：合作方是 McKinsey、BCG、Accenture 和 Capgemini。McKinsey 的说法是，QuantumBlack 的 forward-deployed 团队会在客户部署和 OpenAI 之间 "create a tight feedback loop"（搜索摘要）：https://openai.com/index/frontier-alliance-partners/ 、https://mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-and-openai-scale-ai-driven-transformations-with-new-frontier-alliance
- **AppliedAI（Opus）合作**（2026-05-21）：面向受监管行业，用 agentic AI 改造中后台运营：https://www.opus.com/news/mckinsey-may-2026
- **Agents at Scale 产品套件**（2025-06 在 VivaTech 发布）：包括重构后的流程库、现成 agent 和自研开发工具：https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinsey-at-vivatech-introducing-our-agents-at-scale-product-suite
  - 配套开源的 ARK（Agentic Runtime for Kubernetes）。README 写它 "codifies patterns and practices developed across dozens of agentic application projects"，可以在 OpenAI、Anthropic、Google、Azure 和 Ollama 之间切换模型（已读原文）。2026-09 仍在活跃更新：https://github.com/mckinsey/agents-at-scale-ark
  - QuantumBlack 在 Medium 上写到，Agents at Scale 平台是在给头部金融机构做项目的过程中搭起来的（搜索摘要）：https://medium.com/quantumblack/creating-a-future-proof-enterprise-agentic-platform-architecture-c21fc48406a5
- **Lilli**：2026-03，安全公司 CodeWall 用自主 agent 攻破 Lilli，第三方博客称暴露了 4,650 万条聊天记录（搜索摘要）：https://neuraltrust.ai/blog/agent-hacked-mckinsey 。另有二手报道称，Lilli 2026 年中每月约 50 万次提问，Sternfels 说公司约有 2.5 万个 AI agent（来源质量一般，只作背景）：https://futurefactors.ai/mckinsey-25000-ai-agents-workforce-2026/

**JD 里的数据需求**
- **未找到**。搜索额度用完，没有检索招聘信息。建议手动查 McKinsey 招聘页里 QuantumBlack 和 "evaluation"、"LLM"、"AI quality" 相关的岗位。

**切入点**
- 最匹配的是客户 agent 的验收评测。他们给金融机构和受监管行业做中后台 agent（Agents at Scale、AppliedAI 合作），可以提供专家写的评分标准和领域评测集，按业务流程做验收测试。
- 财务结账和会计环境可以直接用作中后台 agent 的测试环境。Xitadel 对资本市场客户有用，优先级低一些。
- 和 OpenAI、Google 之间有 FDE 反馈循环。如果要把客户场景里的失败案例结构化地反馈给模型方，适合的形式是专家标注的失败案例集和偏好数据。
- 他们不训练基础模型，所以大批量 SFT 和 RL 任务不作为主推。

**风险**
- 买的更可能是评测和验收，量不会大。预算通常挂在具体客户项目下，由合伙人决定，采购和安全审查周期都长。
- Lilli 3 月出过安全事件，外部供应商接触数据时会被审得更严。
- 自有专家资源多（顾问和行业专家网络），我们可能被当作分包商，而不是数据伙伴。
- 收件人层级高，不一定直接管评测。更理想的对象（Labs 下的评测或 AI 质量负责人）没找到。
- 没有查到供应商相关的公开报道。

**核实说明**：本环境打不开 mckinsey.com、PR Newswire、Medium 和招聘站。ARK 的 README 读的是原文，其余来自搜索结果摘要。WebSearch 额度在调研中途用完（McKinsey 部分约 13 次搜索），JD 和评测负责人都没查。开头一句用的 Google 合作事实，在 Google Cloud Press Corner、McKinsey 官网博客、PR Newswire 和 Yahoo Finance 的搜索结果里说法一致。

本次复核（2026-09-25，3 次 WebSearch，mckinsey.com 仍打不开，均为搜索摘要）：
- 联系人：McKinsey 官网个人页（mckinsey.com/our-people/tomas-lajous）、AI Magazine 高管页和报道都写他是 Senior Partner、QuantumBlack Labs 全球负责人。没有查到离职或调岗消息，但也没有带 2026 年日期的官方确认，置信度维持中。补了官网个人页链接。
- 开头一句：Google Cloud Press Corner 新闻稿（2026-04-22）、McKinsey 官网博客、PR Newswire、Yahoo Finance 的搜索摘要都写 "McKinsey's QuantumBlack technologists will collaborate with Google's forward deployed engineers (FDEs) to work on challenging client use cases"。开头一句不改。
- 来源链接里没有 GitHub 转载的新闻；ARK 的 GitHub 仓库是 McKinsey 自己的项目原文，保留。

---

## 邮件

Subject: Expert data for QuantumBlack's post-training

Hi Tomás,

Saw QuantumBlack now builds client agents alongside Google's engineers — curious what expert-built evals those agents have to pass before they ship.

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across finance, accounting, insurance, law and medicine. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal
