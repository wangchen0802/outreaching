# C1 客户调研笔记（2026-09-27）

## 概况
- 共 42 行，seeds.json 的 C1 42 家全部保留，没有删除。WebSearch 用了 96 次（预算 190），原文只读到 GitHub raw 页面，其余依据是搜索摘要。
- 公开的个人邮箱：0 个。有官方备用渠道的 7 家：SSI（comms@ssi.inc）、Reka（contact@reka.ai）、Poolside（research@poolside.ai，写在技术报告署名处）、Liquid AI 和 Motif（官网联系表单）、ServiceNow 和 Morgan Stanley（只有团队介绍页，不能算真正的联系渠道）。
- 置信度：高 5 家（NVIDIA、IBM、Liquid AI、Man Group、Hippocratic AI）；中 25 家；低 12 家。
- 没找到对接人的 9 家：Apple、Legora、AI21、Poolside、Cursor、ServiceNow、Point72、Morgan Stanley、EvenUp。其中 Apple、Legora、AI21、Cursor、EvenUp 在「备选联系人」里写了高管或创始人。

## 创始人需要知道的
- **Apple**：后训练负责人 Zirui Wang 的个人主页仍写着「Apple 后训练负责人」，并公开了邮箱，但 BigGo（2026-02）报道他已去 Google DeepMind。所以这个邮箱没有用，也没有写进表格。AFM 3 是和 Google 合作做的，Apple 的切入难度很高。
- **Amazon**：Nova 系列大部分模型已转为维护状态（KTLO），资源集中到 Pieter Abbeel 领导的 Frontier Model Research（FMR）。新旗舰模型预计在 re:Invent（2026-11-30 至 12-04）发布，现在正是后训练数据的窗口期。
- **Microsoft AI**：2026-03 招了一批 Ai2 的人（Ali Farhadi 任 CVP，Hanna Hajishirzi 负责后训练相关工作）。MAI-Thinking-1 的人工盲测由我们的合作方 Surge 完成，接触前先和 Surge 对齐。
- **AI21 Labs**：2026-05 裁员 61%（180→70 人），Shashua 离开，和 Nebius 的并购谈判破裂，公司转做 Maestro 代理平台。预算很弱，优先级应下调。
- **与 AfterQuery 的冲突**：Legora、Motif、NVIDIA 都是 AfterQuery 公开的客户，接触前先和 AfterQuery 对齐边界。
- **对接人已离职**：ServiceNow 基础模型实验室负责人 Torsten Scholak 已离职；Morgan Stanley 前 AI 负责人 Jeff McMillan 已离职创业；JPMorgan 的 Manuela Veloso 已离开，Sumitra Ganesh 2026-02 接任 AI Research 负责人；Bloomberg 的 Gideon Mann 早已去 Millennium，现在 AI Engineering 由 Anju Kambadur 负责。
- **近期窗口**：Cognition 2026-09-10 发布 SWE-2（基于 Kimi K3 后训练，RL 环境数量翻了三倍）；Perplexity 2026-09 发了 Computer 代理后训练研究；Writer 2026-08 发布 Palmyra X6（基于 GLM-5.2 后训练）；Upstage 2026-07 发布 Solar Open 2；IBM 2026-08 发布 Granite 4.2（新增智能体 RL 阶段）。
- **和我们金融强项最契合**：Goldman（AI 代理在测交易会计和对账，正好对应财务结账环境）、Man Group（AlphaGPT/AlphaTrend）、Jump（多代理量化研究）、LG（EXAONE 为客户选股）、Sakana（MUFG 授信、大和证券财富管理）、Bloomberg ASKB、Hebbia。
- **契合度弱**（保留，但建议靠后）：Periodic Labs（材料科学）、Reka（转向物理 AI，钩子是 2025-08 的旧事件）、Abridge、Hippocratic AI、EvenUp（医疗和人身伤害法律）。
- **量化同业**（Two Sigma、Man、Jump、Point72）数据保密要求高，创始团队的背景可能引起对方顾虑，措辞要注意。

## 方法说明
- 大部分官网被网络策略拦截，钩子都用两个独立搜索结果交叉核实，或者读 GitHub raw 原文（NVIDIA Nemotron sft.md、Salesforce CRMArena README）。
- 没有使用任何数据商网站。只看到 ZoomInfo、RocketReach 之类的结果，也没有据此记录邮箱。
