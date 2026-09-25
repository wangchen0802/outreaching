# 分段 overseas-large：海外大中型人类数据 / 专家网络 / 标注公司

调研日期：2026-09-25。WebSearch 约 115 次。官网、arXiv、HF、SEC 全文都打不开，大部分证据来自搜索摘要和媒体转述，置信度按 brief 标注。

## 覆盖范围（30 家，106 条声明）
- **声明多的**：Scale AI（17 条）、Mercor（12）、Surge AI（11）、Innodata（7）、Appen（6）、Turing、Labelbox（各 5）、Handshake AI、TELUS Digital（各 4）。
- **只有 1–3 条**：Invisible、micro1、Snorkel、Toloka、Sama、Prolific、iMerit、Uber AI Solutions、SuperAnnotate、Pareto.AI、Centific、Welocalize、Encord、Deccan AI、TaskUs、LXT、RWS TrainAI、AfterQuery。起点名单之外新增了 TaskUs、LXT、RWS TrainAI、AfterQuery 四家。
- **没有点名客户**：CloudFactory、Revelo、Defined.ai 只有泛泛的客户描述，没写进 claims。Snorkel、Labelbox、Handshake 融资稿通常只写"frontier labs"，不点名。
- **没查到**：Scale 诉 Mercor 案的起诉书只写了 "Customer A"，没有公开客户名；没找到和解或判决。Appen、TELUS 近两年的财报不再按客户名披露。Innodata 的新前沿实验室客户也没有具名。

## 最有价值的发现
1. **买家高度集中**。Mercor 2026 H1 总收入 6.14 亿美元，超过 90% 来自 OpenAI、Anthropic、Google DeepMind 三家。Innodata 2025 年最大客户（普遍推测为 Meta）占收入 58%，2026 Q2 降到 37%，另一家大厂客户从 17% 升到 34%。TaskUs 的最大客户 Meta 占 26%。
2. **Meta 投资 Scale 之后的迁移**：
   - Google（原约 2 亿美元/年）、OpenAI、xAI、Microsoft 都减少或退出了 Scale。
   - 承接这些业务的主要是 Surge、Mercor、Turing、Handshake、Labelbox。
   - Meta 自己的 TBD Lab 也偏好 Surge 和 Mercor。
   - Scale 的新重心是国防（CDAO 合同上限 5 亿美元）和主权 AI（卡塔尔）。
3. **供应商风险也会让客户流失**。Mercor 2026.4 因 LiteLLM 供应链攻击泄露数据，Meta 无限期暂停合作。
4. **没想到的买家**：
   - **NVIDIA**：为 Nemotron 向 Mercor 付了数千万美元，同时从 Scale、Turing 采购。
   - **中国大厂**：据 Forbes，每年约 5 亿美元流向美国数据商（腾讯→Surge/Mercor、阿里→Mercor/AfterQuery、字节→Turing、蚂蚁→AfterQuery）。另外，Appen China 年化收入超 1.75 亿美元，来自中国大厂出海的 LLM 需求。
   - **Cohere**：同时用 Invisible 和 Appen。
   - **Palantir**：用 Innodata。
5. **需求在往哪里走**：专业领域专家数据（法律、金融、医疗）、智能体和电脑操作的 RL 环境（Innodata、Surge 的 EnterpriseBench、Mercor 收购 Sepal）、专家编写的评分细则（rubric）和基准（AdvancedIF、APEX、GIM、HLE）。

## 对 SimReal 的建议
- **优先找什么买家**：OpenAI、Anthropic、GDM 是所有供应商的共同大买家，而且都在多家采购。可以用"可验证的 RL 环境加验证器"切入，作为 Mercor 和 Surge 之外的补充供应商。
- **二线机会**：NVIDIA（开源 Nemotron，需要可公开的数据和环境）、Meta（刚暂停 Mercor，Scale 数据又被嫌质量差）、Microsoft/Amazon（micro1、Toloka、Invisible 的客户）。
- **渠道合作**：Innodata、Appen、TELUS、TaskUs 这类上市 BPO 手里有大客户，但缺 RL 环境能力，可以谈"白标环境加验证器"。
- **卖点**：强调中立（不被任何实验室持股）和数据安全，这正是 Scale 和 Mercor 丢客户的两个原因。
- **合规**：中国买家的需求真实存在，但有出口和声誉风险，要提前定好政策。
