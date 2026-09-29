# 对外短消息模板（小红书 / 微信 / LinkedIn 私信）

依据：四类公开采购帖（Rubric 采购、金融 Agent 轨迹、基座模型长期采购、数据同行找渠道）里的关键词，对上我们的能力。

## 卖点（按采购方的关键词排）

- **Rubric / 评测**：Rubric 设计与拆解、Reference Answer、逐项评分与质检、LLM-as-a-Judge 评测集、Benchmark 定制。评分标准由领域专家写，上线前做对抗测试（财务月结环境评分漏洞 6 → 0；谜题基准 400 次作弊攻击 0 次成功）。
- **后训练数据**：复杂 Query 构造（专家手写，不是众包）、SFT、CoT 推理、RLHF 偏好、Reward 数据。
- **Agent 数据**：长程多轮任务、工具调用轨迹、完整 Session（工具输入/输出与中间过程全保留），金融和代码场景为主。
- **RL 环境与验证器**：交易（Xitadel，开源模型训练后交易表现 +12%）、财务月结、软件工程、数学证明、逻辑推理、AI 研究、未来预测。
- **代码**：代码 SFT、代码调试指令、"能否挺过下一个版本"的代码验证。
- **领域专家**：金融、医疗、法律、供应链；7,000+ 已报名，通过 21 所合作高校可触达 20 万+ 专业人士。
- **团队**：剑桥 AI 研究背景；Jane Street、Citadel（城堡）、D. E. Shaw、Millennium、Optiver。
- **背书与交付**：一线 VC 支持；已为 Surge AI、AfterQuery 供给；支持高度定制；可先小批量 Demo、提供脱敏样例、稳定批量交付。

## 通用版（私信）

你好，我是 SimReal 联合创始人[姓名]。我们是一线 VC 支持的后训练数据团队，团队来自剑桥 AI 研究、Jane Street、Millennium、城堡（Citadel），已为 Surge AI、AfterQuery 供给。

我们做：
· Rubric 设计/拆解、Reference Answer、逐项评分质检、LLM-as-a-Judge 评测、Benchmark
· 复杂 Query、SFT、CoT、RLHF 偏好、Reward 数据
· Agent 长程轨迹：多轮对话、工具调用、完整 Session
· RL 环境与验证器，代码 SFT 与调试数据
覆盖金融、医疗、法律、供应链、代码，支持高度定制。7,000+ 领域专家已报名，可先小批量 Demo、提供脱敏样例。

方便聊聊您的具体需求吗？

## 针对性开头（放在通用版第一句之后）

**Rubric 采购**
看到您在采购 Rubric 数据。我们的 Rubric 由领域专家设计，上线前做对抗测试，评分漏洞 6 → 0；技术团队懂 RL、SFT 和 LLM-as-a-Judge，能稳定批量交付。

**金融 Agent 轨迹**
看到您在找金融场景 Agent 轨迹。我们是量化团队出身，由金融从业者在真实工作流里使用 Agent，产出完整 Session：30+ 次 Tool Call、5 轮以上真人对话、工具输入输出和中间过程全保留，可以先给样例评估。

**基座模型长期采购**
看到贵团队长期采购代码和 Agent 数据。我们做代码 SFT 与调试指令、Agent 多轮工具调用轨迹、CoT 和 RLHF 偏好数据，全部专家手写或真实执行，不做模板批量，可先给脱敏样本内部测评。

**数据同行 / 渠道**
看到您在找垂直领域专家和甲方项目。我们正好补这块：金融、医疗、法律专家资源，加上 RL 环境和验证器，已在给 Surge AI、AfterQuery 供给，可以项目共享、联合交付。

## 超短版（一条消息，约 80 字）

你好，SimReal，一线 VC 支持，团队来自剑桥、Jane Street、Millennium、城堡。做 Rubric/Benchmark、SFT/CoT/RLHF、Agent 长程轨迹、RL 环境，覆盖金融/医疗/法律/供应链/代码，已给 Surge AI、AfterQuery 供给，可先做 Demo。方便聊吗？

## 邮件短版（手动发送）

发往官方通用邮箱时，第一句加：
- 中文：您好，麻烦转交[负责人]，或负责商务合作的同事。
- 英文：Hi team, could you forward this to [Name], or whoever handles partnerships?

### 客户｜大模型公司

主题：SimReal × [公司名]｜后训练专家数据与 RL 环境

[称呼]您好，我是 SimReal 联合创始人[姓名]。我们为大模型后训练提供专家数据、Rubric 评测和 RL 训练环境，覆盖金融、法律、医疗、代码。团队来自剑桥和 Jane Street、Citadel、Millennium，7,000+ 行业专家已报名。想了解贵司目前的数据需求，可以先给样例或做小批量试点。方便约 20 分钟聊聊吗？

[姓名]｜SimReal｜business@simreal.co

Subject: SimReal x [Company]: expert data and RL environments

Hi [Name], I'm [Your name], co-founder of SimReal. We supply expert data, rubric-based evals and RL environments for post-training across finance, law, medicine and code. Our team comes from Cambridge, Jane Street, Citadel and Millennium, and 7,000+ domain experts have signed up with us. Happy to share samples or run a small pilot. Open to a 20-minute call?

[Your name] | SimReal | business@simreal.co

### 客户｜AI 应用 / Agent 公司

主题：SimReal × [公司名]｜Agent 评测与训练数据

[称呼]您好，我是 SimReal 联合创始人[姓名]。我们可以帮贵司做两件事：按你们的业务出一套评测（题目加评分标准），上线前先测，换模型时直接对比；再用行业专家数据把模型练得更懂你们的场景。团队来自剑桥和 Jane Street、Citadel、Millennium。可以先给样例看效果，方便约 20 分钟吗？

[姓名]｜SimReal｜business@simreal.co

Subject: SimReal x [Company]: evals and training data for your agents

Hi [Name], I'm [Your name], co-founder of SimReal. We help AI product teams in two ways: a private eval built around your workflow, so you can test before launch and compare models when you switch, and expert data to make your model better at your domain. Our team comes from Cambridge, Jane Street, Citadel and Millennium. Happy to share samples first. Open to a 20-minute call?

[Your name] | SimReal | business@simreal.co

### 渠道伙伴

主题：SimReal × [公司名]｜专家供给与 RL 环境合作

[称呼]您好，我是 SimReal 联合创始人[姓名]。我们做后训练的专家数据和 RL 环境，已与 Surge AI、AfterQuery 合作，7,000+ 行业专家已报名，可触达 20 万+ 专业人士。想和贵司谈供给合作：我们出金融、法律、医疗专家和 RL 环境，贵司交付客户，贴牌或联名都可以。方便约 20 分钟吗？

[姓名]｜SimReal｜business@simreal.co

Subject: SimReal x [Company]: expert supply partnership

Hi [Name], I'm [Your name], co-founder of SimReal. We build expert data and RL environments for post-training and already work with Surge AI and AfterQuery; 7,000+ domain experts have signed up with us. We'd like to be a supply partner: our finance, legal and medical experts and environments, delivered to your customers under your brand or co-branded. Open to a 20-minute call?

[Your name] | SimReal | business@simreal.co

### 投资人

主题：SimReal｜让 AI 在真实工作中按结果进化（种子轮）

[称呼]您好，我是 SimReal 联合创始人[姓名]。我们为 AI 搭建真实工作的训练环境：旗舰交易环境让开源模型在真实行情上交易表现提升 12%。团队四位量化出身，来自剑桥、LSE、杜克，有 Jane Street、Citadel、Millennium、Optiver 经历；已与 Surge AI、AfterQuery 合作。正在进行种子轮融资，方便的话我把 BP 发您？

[姓名]｜SimReal｜business@simreal.co

Subject: SimReal: RL environments where AI learns from real outcomes (seed)

Hi [Name], I'm [Your name], co-founder of SimReal. We build the environments where AI does real work and learns from real outcomes; our trading environment lifted an open model's trading performance by 12% on unseen market data. We're four quants from Cambridge, LSE and Duke with backgrounds at Jane Street, Citadel, Millennium and Optiver, and we already work with Surge AI and AfterQuery. We're raising a seed round. Can I send you the deck?

[Your name] | SimReal | business@simreal.co
