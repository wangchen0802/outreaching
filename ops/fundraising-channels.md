# 海外融资渠道：同类公司怎么找到投资人和钱（2026-10）

范围：RL 环境、专家数据、评测这一类公司。资料来自 X、Substack、SaaStr、TechCrunch、加速器官网和融资新闻。Reddit 上没搜到同类公司的融资复盘帖，讲冷邮件的帖子结论和下面一致。

## 结论

同类公司的钱主要有四个来源：

1. **加速器**：YC 孵化得最多，AfterQuery、Datacurve、HUD、Halluminate 都是 YC 出来的。
2. **天使**：前沿实验室研究员和赛道里的创始人以个人身份投。
3. **冷邮件**：发给公开写过 RL 环境论点的合伙人，种子阶段冷邮件进得去。
4. **客户收入**：先拿客户收入，Surge AI 一分钱没融，做到了 10 亿美元以上收入。

我们现在最该做的：
- 把投资人邮件缩到 100 词左右，先发第 1 批；
- 10 月中旬到 11 月初申请 a16z speedrun 和 YC；
- 同时把算力额度和不稀释的资助申请掉。

## 同类公司怎么融的

| 公司 | 怎么融的 |
|---|---|
| AfterQuery | YC 50 万美元 → A 轮 3,000 万美元（Altos、Raine 领投） |
| Datacurve | YC W24 50 万美元（Pioneer Fund、Afore、Northside 等跟投）→ 种子轮 270 万美元（Balaji 领投）→ A 轮 1,500 万美元（Chemistry 领投）。天使里有 DeepMind、Anthropic、OpenAI 的员工（个人身份） |
| HUD | YC W25 + Exceptional Capital |
| Halluminate | YC S25 + Orange Collective、Antigravity、Batch Ventures |
| Mechanize | 910 万美元，全部来自天使型投资人：Nat Friedman、Daniel Gross、Patrick Collison |
| Deeptune | A 轮 4,300 万美元，a16z 领投（2026 年） |
| Surge AI | 创始人自掏约 30 万美元起步，前五年不拿 VC 的钱，第一天就盈利，靠客户收入做到 10 亿美元以上 |

规律有两个：
- 起步大多靠 YC 或天使，A 轮才由一线基金领投。
- 实验室研究员当天使，对后面的融资和获客都有帮助。

来源：[Tracxn: AfterQuery](https://tracxn.com/d/companies/afterquery/__vQqry2tXBlSdZidiY72DiDUR6es3MWKnwSarCLj2EG8/funding-and-investors)、[Tracxn: Datacurve](https://tracxn.com/d/companies/datacurve/__2w9YlTVQ2FbPLzVtvcqLEI1v_XXMwKgf4xoxLtbqb-0/funding-and-investors)、[Maginative: Datacurve A 轮](https://www.maginative.com/article/datacurve-raises-15m-series-a-led-by-chemistry/)、[rl-list: HUD](https://www.rl-list.com/vendors/hud)、[rl-list: Halluminate](https://www.rl-list.com/vendors/halluminate)、[rl-list 名录](https://www.rl-list.com/)、[Fortune: Deeptune](https://fortune.com/2026/03/19/andreessen-horowitz-ai-startups-deeptune-series-a)、[Inc.: Surge AI](https://www.inc.com/sam-blum/bootstrapped-to-1-billion-surge-ai-ceo-edwin-chen-on-how-he-did-it/91207937)、[20VC: Edwin Chen](https://www.thetwentyminutevc.com/edwin-chen)

## 冷邮件现在怎么写才有回复

- **回复率**：平均只有 1–5%。个性化，再加上具体数据，能到 10–15%。（[Prospeo](https://prospeo.io/s/how-to-cold-email-investors)）
- **投资人在被 AI 邮件淹没**：每周收几百封陌生来信，很多是 AI 写的，一眼就能认出来。Air Street 的 Nathan Benaich 公开抱怨过 AI 生成的 pitch 邮件泛滥。（[Causo](https://hub.causo.ai/guides/cold-email-vcs-2026)）
- **越短越好**：拿到回复的冷邮件大多不到 100 词。（[VC Boom](https://www.vcboom.com/guides/cold-email-length-reply-data)）
- **种子轮冷邮件有用**：B 轮以后投资人基本只看引荐。（[SaaStr](https://www.saastr.com/dear-saastr-does-cold-emailing-vcs-work-what-are-some-tactics-to-help-increase-the-odds/)）
- **失败的头号原因是找错人**，不是写得不好：阶段、方向、单笔金额要对得上。

我们现在的投资人模板将近 200 词，建议换成下面这个短版（约 100 词）。短版拿掉了"两家前沿实验室在谈"和"GitHub 500+ 星"，这两条还没确认，先不对外写。

```
Subject: SimReal: RL environments for finance, built by ex-Jane Street and Citadel quants (seed)

Hi [Name],

[Hook]

I'm [Your name], co-founder of SimReal. We build RL environments and verifiers where models do real finance work and are scored on real outcomes. Our trading environment, Xitadel, lifted Qwen3.8-27B's trading performance 12% on unseen market data, reproduced across runs. We already supply Surge AI and AfterQuery, and 7,000+ domain experts have signed up.

We're four quants from Jane Street, Citadel, Millennium and Optiver (Cambridge, LSE, Duke), raising a $20M seed.

Worth 20 minutes? Happy to send the deck.

[Your name]
SimReal | business@simreal.co
```

## 现在能申请的项目（按截止时间）

| 项目 | 截止 | 条件 | 说明 |
|---|---|---|---|
| a16z speedrun SR008 | 优先窗口 10/12–11/1，全年滚动 | 最多 100 万美元：先 50 万美元换 10%，下一轮再投 50 万美元 | 2027 年 1–4 月在旧金山。a16z 有公开的 RL 环境投资论点。[官网](https://speedrun.a16z.com/apply) |
| YC W27 | 11/2 太平洋时间晚 8 点，12/11 出结果 | 标准条款 50 万美元 | 2027 年 1–3 月在旧金山。本赛道 YC 孵化最多，同批次里竞品也多。[申请](https://ycombinator.com/apply) |
| Conviction Embed | 滚动 | 早期项目 | embed@conviction.com，已在名单里 |
| South Park Commons Founder Fellowship | 2026 秋季已截止，2027 春季今年晚些时候开放 | 40 万美元先投，下一轮再投 60 万美元，另有最多 100 万美元的算力额度 | [官网](https://www.southparkcommons.com/news/f26-founder-fellowship/) |
| Menlo × Anthropic Anthology Fund | 滚动，两周内答复 | 10 万美元起，另有 Anthropic 额度 | 要求基于 Anthropic 模型开发产品，和我们只是部分对口。[官网](https://menlovc.com/menlo-anthology-fund/) |

加速器要让出 7–10% 的股份，和 2,000 万美元的种子轮放在一起算要权衡。但同类公司大多走了这条路，拿到的是品牌和批次内的投资人网络。

## 不稀释股权的钱

- **算力额度**：几家可以叠加，合计能覆盖 30–50 万美元的算力成本。（[GMI Cloud](https://www.gmicloud.ai/en/blog/gpu-credit-programs-for-ai-startups-from-prototype-to-production-without-dilution)、[Thunder Compute](https://www.thundercompute.com/blog/nvidia-inception-program-guide)）
  - Google for Startups AI：最高 35 万美元，需要有机构投资；没有机构投资时 2.5–5 万美元。
  - AWS Activate：最高 10 万美元，高档位同样需要机构投资。
  - NVIDIA Inception：不要股份。没有融资的团队通常拿到 1–2.5 万美元。
- **Laude Institute Slingshots**：快速资助，给钱也给算力，2026 年 6 月第三批里有基准和评测类项目（TBench Science、Harbor）。适合我们把部分环境或验证器开源出来申请。（[Laude](https://www.laude.org/updates/slingshots-three)）
- **英国 AISI Challenge Fund**：每个项目 5–20 万英镑，方向是安全、控制、对齐和韧性。上一轮截止是 2026-04-01，后面还会开新一轮。（[UK Authority](https://www.ukauthority.com/articles/ai-security-institute-launches-challenge-fund/)）
- **英国主体才适用（需要确认我们是不是英国公司）**：
  - SEIS：公司最多融 25 万英镑，投资人能抵 50% 的所得税，对英国天使吸引力很大。
  - EIS：2026 年 4 月起额度翻倍，每年 1,000 万英镑（知识密集型公司 2,000 万英镑）。
  - Innovate UK "Efficient, Structured and Controllable AI Systems"：10/12–11/18 开放申请，总额 166 万英镑，面向英国中小企业。

  来源：[Protax](https://www.protax.org.uk/articles/eis-guide-uk-startups-2026/)、[Innovate UK](https://apply-for-innovation-funding.service.gov.uk/competition/2582/overview/9fdb47a5-011c-4c47-ac5e-c426e295fe89)
- **客户预付款**：Surge 的路子。实验室买独家环境的价格约是非独家的 4–5 倍（[Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)）；我们的报价单已经写了预付 50%。一个实验室的付费试点，比任何一封冷邮件都更能打动投资人。

## X 和行业名录怎么用

- **X**：先在赛道里公开发言的投资人帖子下面认真回复，再发邮件，开场句提他们的帖子。这几位都已经在名单里，开场句也用上了：
  - Deedy Das（Menlo）：2026 年 7 月发过一张"所有向实验室卖训练数据和 RL 环境的公司"图谱，50 多家，合计约 85 亿美元收入。（[X](https://x.com/deedydas/status/2076124392711696455)）
  - Chris Zeoli（Wing）：写了 RL 环境市场专题，核心观点是验证层决定输赢。（[Wing](https://www.wing.vc/content/rl-environments-for-agentic-ai-who-will-win-the-training-verification-layer-by-2030)）
  - Nathan Benaich（Air Street）：写 State of AI 报告。
- **还有一家公开写过 RL 环境论点的基金，不在名单里**：[Sapphire Ventures](https://sapphireventures.com/blog/reinforcement-learning-environments-ai-agents/)，下一轮可以补进来。
- **行业名录**：把 SimReal 提交到 [rl-list.com](https://www.rl-list.com/) 和 [Pavlov's List](https://pavlovslist.com/)。实验室和投资人都在看这两个名录，Menlo 的图谱也是按这类名录统计的。
- **行业报道**：Epoch AI 采访过 18 位 RL 环境公司、新实验室和前沿实验室的人（[X](https://x.com/EpochAIResearch/status/2010814868832887163)）。这类报道和播客能带来曝光，可以主动联系作者。

## 下一步

1. **本周**：投资人邮件换成短版，先发第 1 批。有邮箱的是 Conviction、Mayfield、Kindred、Air Street，见 `collateral/SimReal-海外VC名单.xlsx`。
2. **10/12–11/1**：申请 a16z speedrun SR008。11/2 前决定要不要申请 YC W27。
3. **现在就申请**：NVIDIA Inception、AWS Activate、Google for Startups AI，拿到机构投资后再升档。
4. **提交名录**：把 SimReal 提交到 rl-list.com 和 Pavlov's List。
5. **找天使**：通过剑桥和量化圈的校友，找前沿实验室研究员当天使（参照 Datacurve 的种子轮）。
