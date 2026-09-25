# buyer-side 分段笔记（买方反推）

调研日期：2026-09-25。共用约 117 次搜索，另外通过 GitHub raw 和 storage.googleapis.com 直接读了部分原文（Gemini 2.5 报告、Gemini 3 Pro FSF 报告、Gemma 2/3 报告、Llama 4 模型卡、NVIDIA-NeMo/Nemotron 仓库、Kimi K2/k1.5、DeepSeek-R1、Qwen3、MiniMax-M1 技术报告）。
产出：`buyer-side-claims.csv` 94 条关系，`buyer-side-vendors.csv` 23 家其他分段可能漏掉的供应商。

## 覆盖情况

**有收获的买方**：OpenAI（16 条）、Anthropic（11）、NVIDIA（8）、Google/DeepMind（12）、Meta（7）、Microsoft（4）、Cohere、IBM、Apple、Amazon、xAI/SpaceX、AI21、Mistral、Perplexity、Harvey、Cognition、Applied Compute、Upstage，以及腾讯、阿里、蚂蚁、字节、月之暗面、智谱。

**查了但基本没有结果**：
- 国内实验室（DeepSeek、Qwen、Kimi、MiniMax、GLM、Step、混元、Seed）的技术报告和 README 都不点名供应商。智谱和 MiniMax 的港股招股书只披露前五大供应商占比（智谱 2025H1 为 50.2%，MiniMax 主要是云），不披露名称；港交所原文读不到。国内实验室和美国供应商的关系几乎都来自 Forbes（2026-08）和 SemiAnalysis。
- Llama 3、Phi-4、Gemma 3、Tülu 3、Apple AFM 2025 的原文或摘要里没有点名供应商；Llama 4 和 Amazon Nova 只写了“our vendors / third-party vendor”。
- Perplexity、Cursor、Cognition 没有公开的外采声明。Cursor 的 Composer 2 报告说 RL 环境是自建的（Anyrun 沙箱）；Cognition 的 SWE-1.5 也用自建的 otterlink 环境，只在基准上和 Mercor 共建了 APEX-SWE。DeepSeek 自招“数据百晓生”，偏向自建。
- 没找到银行、保险等传统企业公开外采 RL 环境的案例，只有供应商自己做的保险核保等示例环境。
- HuggingFace、arXiv 以及各实验室的 CDN 都被拦截；NVIDIA 数据卡的供应商信息只能通过第三方 GitHub issue 的搜索摘要看到（置信度低）。

## 最有价值的发现

1. **最大的买家是 Anthropic 和 OpenAI，而且都同时用多家供应商。** Anthropic 同时和十几家 RL 环境公司签约，讨论过年投入超过 10 亿美元，并且常常是新供应商的第一个客户。OpenAI 有多份七位数的环境和数据合同，官方口径是“专家由第三方供应商招募和付费”，点名的有 Mercor 和 Handshake。
2. **Meta 投资 Scale 之后的迁移是最清楚的客户变动。** Google（原计划约 2 亿美元）、OpenAI、xAI、Microsoft 都撤出了 Scale，业务流向 Surge、Mercor 和 Handshake。2026-04 Mercor 数据泄露后，Meta 又暂停了和 Mercor 的合作。买方对“供应商中立性”和“数据安全”非常敏感。
3. **NVIDIA 是被低估的买家。** 它向 Scale、Translated 买标注，购买了 Mercor 的 SWE-AgentsV1、Patronus 的对话记忆数据、“undisclosed purchased” 数学包和类 Terminal-Bench 任务，还有供应商整理的搜索难题，另外收购了 Gretel。它的开源模型要靠外采数据来补足能力。
4. **中国大厂在直接买美国数据。** 头部 6 家每年约 5 亿美元，点名的有：腾讯←Surge/Mercor，阿里←AfterQuery/Mercor，蚂蚁←AfterQuery，字节←Turing，月之暗面和智谱←Surge 的 RL 环境。这方面有政策风险。国内另一条路是自建专家平台（Xpert、晓天睿士、企鹅标注），再加上字节公开招标垂类（医疗、法律、教育）供应商。
5. **意外的买家和形态：**
   - 买破产企业的真实工作流数据来做环境：Google 花 1000 万美元买下 Spirit Airlines 的数据，Mercor 和 micro1 参与了竞价，SpaceX 也在讨论同类收购。
   - 主权 AI 项目：Upstage 和 Flitto。
   - 评测外包给咨询和安全公司：Deloitte、CrowdStrike、Signature Science。
   - Microsoft 请 Surge 做发布用的盲测。
6. **需求最集中的领域**：编码/终端类智能体任务、计算机和浏览器使用、专业知识工作（投行、法律、医疗）、安全/CBRN 评测、多语言。

## 对 SimReal 的建议（≤400字）

1. 首攻多供应商采购、预算最大的 Anthropic 和 OpenAI，其次是 NVIDIA。NVIDIA 公开买环境和任务包，而且开源叙事需要“可披露的供应商”，SimReal 可以主动提供可署名、可审计的数据包。
2. 把“中立 + 安全”做成卖点。Scale 的客户流失和 Mercor 泄露事件都说明，买方会因为股权冲突或安全事故立刻暂停合作。建议准备 SOC2、数据隔离方案，并明确不接受实验室的股权投资。
3. 产品上优先做终端/编码、企业工作流（可以用授权或破产企业的真实数据来填充环境）和专业知识工作三类环境，配上验证器和评分 rubric。
4. 次级市场：Microsoft AI、Cohere、Upstage 这类主权模型、Harvey 这类垂直 AI，以及用 Mercor 数据做后训练的 Applied Compute 这类新实验室。
5. 中国客户要谨慎：与国内大厂合作已经引起美国舆论和政策关注，需要先评估出口管制和声誉风险。
