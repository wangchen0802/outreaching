# 海外 VC 分段（vc-overseas）调研笔记

调研日期 2026-09-26。所有信息来自公开搜索结果；网页基本无法直接打开，绝大多数条目是通过搜索摘要看到的，明细见 `vc-overseas-funds.csv`（63 行：机构与天使）和 `vc-overseas-deals.csv`（71 笔交易）。CSV 的置信度按来源类型打分，并标注"搜索摘要"；对外引用前建议打开原文核对。

## 一、最值得先接触的 15 家（按优先级）

1. **HRT Ventures（Hudson River Trading）**：量化机构本身，2026 年先后跟投 Vals AI 和 Gray Swan 两家评测/红队公司，团队背景最契合；具体负责人未查到，需从官网渠道找。
2. **General Catalyst，Yuri Sagalov**：专做种子，2026-08 领投企业 RL 沙箱公司 Arga，公开说"可复现的沙箱环境对 agent 比对人更重要"；需回应其与 Mercor 的深度关系。
3. **a16z，Martin Casado 和 Jennifer Li**：公开表示"RL 环境正成为 AI 栈的下一个关键层"；Deeptune 被 Mercor 收购后，a16z 在这一方向留有空位；另外跟投过前 Citadel 量化团队创办的 Moment。
4. **Index Ventures**：两次领投前 Citadel Securities 量化团队创办的 Moment，并领投过 Adaptive ML 的后训练种子轮；美欧双中心。
5. **Chemistry，Mark Goldberg**：写过投资论文《RL Reigns Supreme》，领投 Datacurve A 轮；Datacurve 联合创始人被 36Kr 报道为华人，说明该基金对中国籍团队友好。
6. **Kleiner Perkins，Leigh Marie Braswell**：曾在 Scale AI 工作，领投 Applied Compute；Applied Compute 同时是 SimReal 的潜在客户，可形成组合协同。
7. **Lightspeed，Faraz Fatemi**：2026 年先后领投 Origin Lab（训练数据）和 Judgment Labs（评测）的种子轮；投过华人创始的 Pika。
8. **Scribble Ventures，Elizabeth Weil 和 Stu Smith**：领投 Proximal（编码 RL 环境）的种子轮；单笔小、决策快，适合做种子锚定。
9. **Menlo Ventures，Deedy Das**：持续整理训练数据与 RL 环境的市场图谱，对赛道最熟；但已投 Fleet 和 Mercor 两家竞品。
10. **Susquehanna（SIG）**：量化做市机构，跟投了人类数据公司 Deccan AI 的 A 轮。
11. **Conviction，Sarah Guo**：种子基金，关注 agent 部署后的持续学习；投过 HeyGen。
12. **Wing VC，Peter Wagner**：发表 RL 环境市场研究，认为瓶颈在"验证"，正对应 SimReal 的验证器卖点；但已投 Bespoke Labs。
13. **Elad Gil**：投资覆盖后训练（Applied Compute）、评测（Braintrust）和数据策展（DatologyAI），适合做信号型天使。
14. **Standard Capital，Dalton Caldwell**：领投 HUD 的 A 轮，定位 AI 原生的 A 轮基金，可作为下一轮储备。
15. **Jane Street（战略）**：团队前东家之一，已有以机构名义领投 AI 种子轮的先例（Numerata），同时是金融 RL 环境的潜在客户；需处理好前雇主关系。

**需谨慎的机构**：
- Khosla：Vinod Khosla 公开表示"永远不会在中国"。
- Founders Fund：合伙人公开嘲讽 Benchmark 投资 Manus 被审查一事。
- Benchmark：领投 Manus 后遭美国财政部 OISP 审查。
- Altos、Felicis、01 Advisors、Bezos Expeditions：分别深度绑定 AfterQuery、Mercor、micro1、Toloka。

## 二、近 12 个月（2025-10 至 2026-09）的融资节奏和估值

- **种子轮**：通常 300 万–1000 万美元。例如 Arga 1000 万美元（GC 领投）、Origin Lab 800 万美元（Lightspeed 领投）、Bespoke 种子 825 万美元（8VC 领投）、Scorecard 375 万美元、Poindexter 200 万英镑。
- **A 轮**：通常 1500 万–4500 万美元，估值 3 亿–7 亿美元。例如：
  - Deeptune 4300 万美元（a16z 领投）
  - Fleet 4500 万美元，估值 7.25 亿美元，约为年化收入 6000 万美元的 12 倍
  - Vals 4000 万美元，估值 4 亿美元
  - AfterQuery 3000 万美元，估值 3 亿美元，当时年化收入约 1 亿美元
  - HUD 1600 万美元
- **头部估值快速拉升**：
  - AfterQuery 5 个月内估值从 3 亿美元涨到 32 亿美元
  - micro1 估值 40 亿美元
  - Snorkel 估值 35 亿美元
  - Applied Compute 从 13 亿美元涨到约 32.5 亿美元（洽谈中）
  - Prime Intellect 估值 10 亿美元
  - Mercor 洽谈估值约 200 亿美元
- **整合加速**：
  - Mercor 收购 Sepal AI 和 Deeptune
  - Datadog 收购 Adaptive ML
  - Google 与 Mechanize 达成逾 15 亿美元的人才与授权交易
  - NVIDIA 此前已收购 Gretel
- **退出信号**：收购方是数据巨头、大厂和可观测性平台，RL 环境团队本身就是被收购的对象。

## 三、对 SimReal 融资叙事的建议

- **定位**：主打"金融领域可验证的 RL 环境与验证器"，别讲成又一家专家数据商。呼应 Wing 的"瓶颈在验证"和 a16z 的"环境是 AI 栈下一层"。
- **团队**：把 Citadel、Millennium、Jane Street 背景讲成"能构造真实交易与风控任务、能写出自动判分的验证器"；对标同为前 Citadel 团队的 AfterQuery 和 Moment。
- **证明**：用实验室付费试点和年化收入证明需求；本赛道 A 轮估值约为年化收入的 3–12 倍。
- **中国问题**：主动说明是美国实体、团队在美、不训练前沿模型、数据不出境。优先接触 Lightspeed、Chemistry、Conviction、SV Angel、Elad Gil，暂缓 Khosla、Founders Fund。
- **竞品**：对投过竞品的机构，主动列出其组合中的竞品，用"金融垂直 + 验证器"讲清差异化。
