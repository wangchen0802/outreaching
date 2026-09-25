# 分段 overseas-rl：海外中小型 RL 环境 / 验证器 / 评测 / 专业数据公司

调研日期：2026-09-25。本分段共用 182 次搜索（发现 30 次，逐家调研约 152 次）。官网和新闻站点基本都被网络策略拦截，大部分证据来自搜索摘要，已在“原文证据”中标注“（搜索摘要）”，置信度也相应下调。能直接读原文的只有 GitHub 上的 README：OpenThoughts、Curator、FrontierSWE、DeepSWE、hud-python、WebBench、BenchFlow、Cua。

## 覆盖范围
- 供应商 45 家，关系 282 行。其中客户、合作、共建基准等 210 行，投资方 72 行。
- 置信度分布：高 87，中 116，低 79。
- 起点名单 20 家全部覆盖。新发现 25 家：
  - 评测与红队：Andon Labs、Irregular（原 Pattern Labs）、Gray Swan AI、Haize Labs、LMArena、Apollo Research
  - 编码与 RL 环境：Proximal、Calaveras、Vmax、Habitat、Refresh、Andromede、General Reasoning、BenchFlow、Cua、Arga Labs、Good Start Labs、Huzzle Labs
  - 数学与专家数据：Sciloop、hillclimb、Poindexter Labs、Realset AI/Flatkey
  - 规模较大的参照：Applied Compute、Snorkel AI、Toloka
- 未收录：Scale、Surge、Mercor、Turing、Handshake、Micro1、Invisible 等大型人类数据公司，按分工由其他分段负责。

## 没查到或只查到未具名客户
- 零条关系：Plato、Habitat、Realset AI/Flatkey。
- 只有“未具名 frontier labs”或只有投资方：Fleet、Matrices、Veris AI、Preference Model、Calaveras、Refresh、Vmax、Andromede、Sciloop、Arga Labs、Poindexter Labs、Deeptune。
- 小型 RL 环境公司普遍不公开客户名，只说“top labs”，有的还签了独家合同（Preference Model）。所以本分段点名客户的关系，多数来自评测和红队公司（系统卡会公开致谢第三方测试方）以及融资稿。

## 关键发现
1. **买家高度集中。** 直接点名 OpenAI、Anthropic、Google/DeepMind 的供应商各有 14 家，点名 Meta 的有 6 家，点名 xAI、Amazon、NVIDIA 的各 4 家。Anthropic 在 SemiAnalysis 口中是“first-mover”，同时用十几家环境供应商。
2. **评测和安全是公开关系最多的领域。** METR、Apollo Research、Irregular、Gray Swan、Andon Labs 出现在 OpenAI 和 Anthropic 的系统卡里。
   - 2026 年 Irregular 的网络安全评测沙箱误连公网，OpenAI、Anthropic、Meta、Google 四家实验室都受到影响，Anthropic 随后暂停了外部网络安全评测。
   - 这说明实验室很在意评测环境的隔离性和可审计性。
3. **并购密集，Mercor 在整合环境供应商。**
   - Mercor 收购了 Deeptune（2026-07）和 Sepal AI（2026-02），还是 Applied Compute 的客户兼数据合作方。
   - 其他并购：Datadog 收购 Adaptive ML，Beacon 收购 Haize Labs，Google 与 Mechanize 达成逾 15 亿美元的人才加技术授权交易。
4. **没想到的买家。**
   - 企业和中型 AI 公司：Ramp、Zapier（经 Prime Intellect），DoorDash、Cognition（经 Applied Compute），Legora、Motif Technologies（经 AfterQuery），AT&T、Manulife、SK Telecom（经 Adaptive ML），Kore.ai（经 Collinear）。
   - 律所：Reed Smith 等参与 Vals AI 的法律基准。
   - 政府：美国联邦政府（经 Snorkel），UK AISI 和 US CAISI（经 Gray Swan）。
   - 开源实验室：Nous Research（经 hillclimb）。
   - NVIDIA 同时以客户、合作方或投资方的身份出现在 4 家供应商中。
5. **增长快、估值高。** 按媒体报道：
   - AfterQuery 年化收入超 1 亿美元，据报估值约 32 亿美元。
   - Fleet 在 2026-04 达到约 6000 万美元年化收入。
   - Prime Intellect 年化收入超 1 亿美元。

## 对 SimReal 的建议
- **先主攻 Anthropic 和 OpenAI 的采购与评测团队。** 两家同时向十余家供应商采购，愿意多供应商并行，新供应商有进入空间。
- **把“隔离、可审计、可复现”做成卖点。** Irregular 事故之后，沙箱安全和验证器可靠性是实验室最在意的差异点，交付物最好附带隔离说明和奖励作弊（reward hacking）检测报告。
- **第二梯队客户已经形成。** 包括 NVIDIA、Cognition、DoorDash、Ramp、Legora、韩国 Motif 这类中型模型或应用公司，以及电信、保险企业。它们采购门槛更低，名字也更可能公开，适合做首批案例。
- **垂直领域优先金融和法律。** AfterQuery、Halluminate、Vals、Applied Compute 都在往这两个方向转，需求已经得到验证。
- **注意 Mercor 的整合趋势。** 它既是潜在的渠道或合作方，也在吞并独立环境商。与其正面竞争，不如差异化：做中文和多语种环境，以及国内实验室也能用的通用格式（Environments Hub、OpenReward、Tinker）。
