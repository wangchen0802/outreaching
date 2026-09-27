"""Build `investors/<slug>` documents for the approval page's investor tab.

Source of truth for order, contacts and opening lines is INVESTORS below; facts
come from intel/vc-overseas-funds.csv and intel/vc-overseas-deals.csv. Outreach
state (`outreach`, `recipient`) belongs to the page and is not written here.

Waves: 1 = warm-up (seed funds and angels most likely to reply and write a
cheque, few conflicts), 2 = know the space but have a conflict or a later stage,
3 = the most important funds, contacted last once the pitch has been tested,
9 = not now (reason given, no email).

Usage: python3 tools/build_investors.py [--out DIR]
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

WAVES = {1: "第一批：先热身", 2: "第二批：懂赛道，有冲突或阶段偏后", 3: "第三批：最重要，最后联系", 9: "暂不联系"}

# (slug, wave, name, type, region, contact, role, contact_url, confidence,
#  salutation, opening, why, deals, conflicts, china, no_email)
INVESTORS = [
    # ---- Wave 1 ----
    ("scribble", 1, "Scribble Ventures", "VC", "美国", "Stu Smith", "Scribble Ventures；发布了 Proximal 种子投资帖（创始人/管理合伙人 Elizabeth Weil 可抄送）",
     "https://www.scribble.vc/elizabeth-weil", "低", "Hi Stu,",
     "Saw Scribble led Proximal's seed. We're building the same kind of long-horizon, verifiable RL environments, but for finance rather than coding.",
     "领投过 RL 环境公司的种子轮，单笔小（约 30 万–75 万美元）、决策快；Proximal 做编码，和金融不重叠。",
     "Proximal 种子领投", "Proximal（编码 RL 环境，相邻不重叠）", "未找到", ""),
    ("decibel", 1, "Decibel Ventures", "VC", "美国", "未找到", "先在官网团队页确认负责 Veris AI 的合伙人",
     "https://www.businesswire.com/news/home/20250603868539/en/Veris-AI-Emerges-from-Stealth-with-$8.5M-to-Train-AI-Agents-Using-Simulated-Experience-Removing-Roadblocks-to-Enterprise-Adoption", "低", "Hi [name],",
     "Saw Decibel co-led Veris AI's seed to train agents in simulated enterprise environments. We're building simulated environments with automatic verifiers for finance work.",
     "种子基金，领投过 agent 模拟环境；阶段完全对口。",
     "Veris AI 种子联合领投 $8.5M", "Veris AI（企业 agent 模拟环境）", "未找到", ""),
    ("acrew", 1, "Acrew Capital", "VC", "美国", "未找到", "先在官网团队页确认负责 Veris AI 或 Invisible 的合伙人",
     "https://www.businesswire.com/news/home/20250603868539/en/Veris-AI-Emerges-from-Stealth-with-$8.5M-to-Train-AI-Agents-Using-Simulated-Experience-Removing-Roadblocks-to-Enterprise-Adoption", "低", "Hi [name],",
     "Acrew co-led Veris AI's seed and backs Invisible, so you've seen both the simulation side and the human-data side of post-training. SimReal sits where they meet: finance RL environments, built with our own expert network.",
     "同时投了模拟环境和专家数据两类公司，最容易听懂我们的定位；种子阶段对口。",
     "Veris AI 种子联合领投；Invisible 老股东", "Veris AI；Invisible Technologies", "未找到", ""),
    ("kindred", 1, "Kindred Ventures", "VC", "美国", "未找到", "先在官网确认 Scorecard 投资的负责人",
     "https://kindredventures.com/announcement/scorecard-solving-ai-agent-evaluation-at-scale/", "低", "Hi [name],",
     "Saw Kindred led Scorecard's seed on agent evaluation. We build the other half of that loop: finance environments with automatic verifiers that labs can train against, not just test on.",
     "种子领投过 agent 评测，没有 RL 环境竞品。",
     "Scorecard 种子领投 $3.75M", "无", "未找到", ""),
    ("pear", 1, "Pear VC", "VC", "美国", "未找到", "先在官网确认负责 Vals AI 的合伙人",
     "https://sacra.com/c/vals-ai/", "低", "Hi [name],",
     "Pear backed Vals from the seed, and Vals has become a reference point for finance and legal benchmarks. We turn the same kind of real finance work into RL environments that labs can train on.",
     "pre-seed/种子基金，评测公司股东，没有 RL 环境竞品。",
     "Vals AI 种子、A 轮；BenchFlow 种子", "无", "未找到", ""),
    ("sv-angel", 1, "SV Angel", "VC", "美国", "未找到", "先在官网确认对接人",
     "https://techcrunch.com/2026/08/26/arga-is-building-a-better-way-to-train-enterprise-ai-agents/", "低", "Hi [name],",
     "SV Angel is in Fleet, Arga and Origin Lab, so you've watched the environment market form early. We're building the finance version, with verifiers written by people from Citadel and Jane Street.",
     "本赛道跟投最活跃的种子基金之一；投过 HeyGen，对华人团队友好。",
     "Fleet；Arga Labs；Origin Lab；Judgment Labs", "Fleet；Arga Labs", "投过 HeyGen", ""),
    ("boxgroup", 1, "BoxGroup", "VC", "美国", "未找到", "先在官网确认对接人",
     "https://www.businesswire.com/news/home/20260409469482/en/AfterQuery-Raises-$30-Million-Series-A-Round-at-$300-Million-Valuation", "低", "Hi [name],",
     "BoxGroup backed AfterQuery and Arga early, and both have finance people on the founding team. We're a finance-native team too, focused on RL environments and verifiers rather than raw expert labels.",
     "早早投了两家金融背景团队做的 AI 数据/环境公司，看得懂我们的背景。",
     "AfterQuery（早期）；Arga Labs 种子", "AfterQuery；Arga Labs", "未找到", ""),
    ("abstract", 1, "Abstract Ventures", "VC", "美国", "未找到", "先在官网确认对接人",
     "https://beinsure.com/news/deeptune-raises-43mn-to-build-ai-agents/", "低", "Hi [name],",
     "Abstract is in Deeptune and Applied Compute, so you've seen both the teams building environments and the teams training on them. We build finance environments with automatic verifiers.",
     "RL 环境和后训练两边都跟投过；Deeptune 已并入 Mercor，竞品冲突减弱。",
     "Deeptune A 轮；Applied Compute", "Deeptune（已被 Mercor 收购）", "未找到", ""),
    ("776", 1, "776", "VC", "美国", "未找到", "先在官网确认对接人",
     "https://a16z.com/announcement/investing-in-deeptune/", "低", "Hi [name],",
     "Saw 776 in Deeptune's Series A. With Deeptune now part of Mercor, we think there's room for an independent environment builder, and we're starting with finance.",
     "投过 RL 环境公司，且那家已被收购，组合里出现空位。",
     "Deeptune A 轮", "Deeptune（已被 Mercor 收购）", "未找到", ""),
    ("emergence", 1, "Emergence Capital", "VC", "美国", "未找到", "先在官网确认负责 Arga 的合伙人",
     "https://techcrunch.com/2026/08/26/arga-is-building-a-better-way-to-train-enterprise-ai-agents/", "低", "Hi [name],",
     "Emergence backed Arga's sandboxes for enterprise software. We're building the finance counterpart: trading and financial-close environments with automatic verifiers.",
     "投过企业软件 RL 沙箱，种子到 A 轮；据摘要是 Genspark 早期投资人（低置信度）。",
     "Arga Labs 种子", "Arga Labs", "据摘要投过 Genspark（前百度团队），未核实", ""),
    ("gradient", 1, "Gradient Ventures（Google）", "战略投资", "美国", "未找到", "先在官网确认负责 Arga 的合伙人",
     "https://techcrunch.com/2026/08/26/arga-is-building-a-better-way-to-train-enterprise-ai-agents/", "低", "Hi [name],",
     "Gradient backed Arga's seed on sandboxes for enterprise agents. We're building the same kind of environments for finance, and Google is one of the labs that buys this kind of work.",
     "Google 旗下种子基金，投过企业 RL 沙箱；Google 本身是 RL 环境大买家。",
     "Arga Labs 种子", "Arga Labs", "未找到", ""),
    ("mayfield", 1, "Mayfield", "VC", "美国", "未找到", "先在官网确认负责 Bespoke Labs 的合伙人",
     "https://www.businesswire.com/news/home/20260706827813/en/Bespoke-Labs-Announces-$40M-to-Build-the-Environments-That-Train-Reliable-Agents", "低", "Hi [name],",
     "Mayfield joined Bespoke Labs' Series A on RL environments. We're building environments for finance, where verifying outcomes takes people who have done the work.",
     "投过 RL 环境公司，种子阶段活跃。",
     "Bespoke Labs A 轮", "Bespoke Labs", "未找到", ""),
    ("episode1", 1, "Episode 1 Ventures", "VC", "英国（伦敦）", "未找到", "先在官网确认负责 Poindexter Labs 的合伙人",
     "https://tech.eu/2026/06/02/poindexter-labs-raises-ps2m-to-improve-training-data-for-advanced-ai/", "低", "Hi [name],",
     "Saw Episode 1 led Poindexter Labs' seed on training data for advanced AI. We're building finance RL environments and expert data, with a team from Citadel, Millennium and Jane Street.",
     "欧洲少数领投 AI 训练数据种子轮的基金，竞争少、回复率可能更高。",
     "Poindexter Labs 种子领投 £2M", "Poindexter Labs（训练数据）", "未找到", ""),
    ("conviction", 1, "Conviction", "VC", "美国", "Sarah Guo", "创始人",
     "https://x.com/saranormous/status/2059785254077116890", "高", "Hi Sarah,",
     "Your line that \"AI is largely frozen after deployment\" stuck with me. Environments where agents keep practicing against verifiable outcomes are one way to change that, and we're building them for finance.",
     "种子基金，创始人本人关注 agent 持续学习；投过 HeyGen，对华人团队友好。",
     "Trajectory Labs", "无", "投过 HeyGen", ""),
    ("elad-gil", 1, "Elad Gil", "天使", "美国", "Elad Gil", "个人投资人",
     "https://aiweekly.co/alerts/applied-compute-in-talks-for-3b-round-led-by-elad-gil", "中", "Hi Elad,",
     "You've backed Applied Compute, Braintrust and DatologyAI, which covers most of the post-training loop. We work on the environment layer, starting with finance.",
     "信号型天使，后训练、评测、数据策展都投过；投过 HeyGen。",
     "Applied Compute；Braintrust；DatologyAI；Scale AI", "Scale AI", "投过 HeyGen", ""),
    ("dylan-patel", 1, "Dylan Patel（SemiAnalysis）", "天使", "美国", "Dylan Patel", "SemiAnalysis 创始人；公开渠道是本人 X",
     "https://www.hud.ai/blog/announcing-16m-series-a", "高", "Hi Dylan,",
     "You angel-invested in HUD and Prime Intellect. We're building RL environments too, but vertical: finance tasks with verifiers written by people from Citadel and Jane Street.",
     "活跃的 RL 基础设施天使，愿意投早期团队。",
     "HUD A 轮；Prime Intellect 种子扩展", "HUD；Prime Intellect", "未找到", ""),
    ("yash-patil", 1, "Yash Patil（Applied Compute CEO）", "天使", "美国", "Yash Patil", "Applied Compute CEO",
     "https://a16z.com/announcement/investing-in-deeptune/", "中", "Hi Yash,",
     "You backed Deeptune as an angel, and Applied Compute trains agents for enterprises. We build finance environments with automatic verifiers, which may matter to you both as an investor and as a buyer.",
     "天使投过 RL 环境；Applied Compute 同时是潜在客户，一次沟通两种机会。",
     "Deeptune A 轮天使", "Deeptune（已被 Mercor 收购）", "未找到", ""),
    # ---- Wave 2 ----
    ("madrona", 2, "Madrona", "VC", "美国（西雅图）", "Vivek Ramaswami", "合伙人",
     "https://www.madrona.com/gray-swan-series-a/", "高", "Hi Vivek,",
     "Saw Madrona co-led Gray Swan's Series A. Red-teaming and RL environments share a problem: you need realistic tasks and a reliable way to score them. We're building both for finance.",
     "领投过红队/评测，没有 RL 环境竞品；阶段偏 A 轮。",
     "Gray Swan AI A 轮联合领投", "无", "未找到", ""),
    ("redpoint", 2, "Redpoint", "VC", "美国", "未找到", "先在官网确认负责 Irregular 的合伙人",
     "https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models/", "低", "Hi [name],",
     "Redpoint co-led Irregular's round on security evaluations for frontier models. We're building evaluations and training environments for finance, where outcomes can be scored automatically.",
     "领投过前沿模型评测，没有竞品冲突。",
     "Irregular 联合领投", "无", "未找到", ""),
    ("lux", 2, "Lux Capital", "VC", "美国", "未找到", "先在官网确认负责 Applied Compute 的合伙人",
     "https://siliconangle.com/2025/10/30/former-openai-researchers-launch-applied-compute-80m-funding/", "低", "Hi [name],",
     "Lux has backed Applied Compute twice. Teams like that need realistic environments to train against; we build them for finance.",
     "持续加注后训练平台，没有竞品冲突。",
     "Applied Compute（两轮）", "无", "未找到", ""),
    ("samsung-next", 2, "Samsung Next", "战略投资", "韩国/美国", "未找到", "先在官网确认对接人",
     "https://www.grayswan.ai/news/gray-swan-announces-series-a", "低", "Hi [name],",
     "Samsung Next joined Gray Swan's Series A, and Samsung backed Patronus. We're building training environments for finance agents, with automatic verifiers.",
     "韩国战略方，连投两家评测公司，没有 RL 环境竞品。",
     "Gray Swan AI A 轮；Patronus AI B 轮（Samsung）", "无", "未找到", ""),
    ("raine", 2, "The Raine Group", "VC", "美国", "未找到", "先确认对接人",
     "https://www.businesswire.com/news/home/20260409469482/en/AfterQuery-Raises-$30-Million-Series-A-Round-at-$300-Million-Valuation", "低", "Hi [name],",
     "Raine joined AfterQuery's Series A, so you've seen how much labs will pay for finance expertise. We focus on the environment and verifier layer built on top of that expertise.",
     "商人银行背景，懂金融专家数据；但持有 AfterQuery。",
     "AfterQuery A 轮", "AfterQuery（最直接竞品之一）", "未找到", ""),
    ("8vc", 2, "8VC", "VC", "美国", "未找到", "先在官网确认负责 Bespoke Labs 的合伙人",
     "https://www.businesswire.com/news/home/20260706827813/en/Bespoke-Labs-Announces-$40M-to-Build-the-Environments-That-Train-Reliable-Agents", "低", "Hi [name],",
     "8VC led Bespoke Labs' seed and backs Vals. We sit between the two: environments you can train on, with verifiers strict enough to evaluate with, starting in finance.",
     "领投过 RL 环境种子轮，也是评测公司股东；持有 Bespoke。",
     "Bespoke Labs 种子领投；Vals AI", "Bespoke Labs", "未找到", ""),
    ("standard-capital", 2, "Standard Capital", "VC", "美国", "Dalton Caldwell", "领投 HUD A 轮",
     "https://www.linkedin.com/posts/daltoncaldwell_hud-standard-capital-series-a-activity-7473502415812448256-wRab", "高", "Hi Dalton,",
     "You described HUD as to Scale what Airbnb is to Hilton. We're betting on a vertical version of that: finance environments whose verifiers are written by people who have done the work.",
     "对 RL 环境有明确观点，但只做 A 轮；现在认识，为下一轮铺路。",
     "HUD A 轮领投 $16M", "HUD", "未找到", ""),
    ("wing", 2, "Wing VC", "VC", "美国", "Peter Wagner", "创始合伙人，公开评论了 Bespoke Labs 投资",
     "https://www.businesswire.com/news/home/20260706827813/en/Bespoke-Labs-Announces-$40M-to-Build-the-Environments-That-Train-Reliable-Agents", "高", "Hi Peter,",
     "Wing's piece on who will win the RL environment market argues the bottleneck is verifying data, not collecting it. That's the part we focus on: finance environments whose verifiers are written by people from Citadel and Jane Street.",
     "写过 RL 环境市场研究，强调验证，正对我们的卖点；但持有 Bespoke，偏 A 轮。",
     "Bespoke Labs A 轮领投；Gray Swan AI A 轮联合领投", "Bespoke Labs", "未找到", ""),
    ("menlo", 2, "Menlo Ventures", "VC", "美国", "Deedy Das", "合伙人，种子到 B 轮（Tim Tully 官网所列投资含 Fleet）",
     "https://menlovc.com/team/deedy-das/", "高", "Hi Deedy,",
     "Your July map of every startup selling AI training data is the clearest picture of this market we've seen. We're one of the few focused on finance, with verifiers written by people from Citadel and Jane Street.",
     "对赛道最熟的合伙人之一；但持有 Fleet、Mercor，要讲清差异。",
     "Fleet；Mercor；Prime Intellect", "Fleet；Mercor；Prime Intellect", "未找到", ""),
    ("lightspeed", 2, "Lightspeed", "VC", "美国/全球", "Faraz Fatemi", "合伙人，领投 Origin Lab",
     "https://www.businesswire.com/news/home/20260513129175/en/Origin-Lab-Raises-$8M-Seed-Led-by-Lightspeed-to-Build-the-Platform-Turning-Video-Game-Worlds-Into-Training-Data-for-AI", "高", "Hi Faraz,",
     "Your note on Origin Lab, that frontier AI now needs data \"grounded in interactive environments\", is the bet we're making in finance.",
     "2026 年连续领投训练数据和评测的种子轮；投过 Pika，对华人团队友好。重要，但比第三批冲突少，放第二批末尾。",
     "Origin Lab 种子领投；Judgment Labs 领投；Snorkel AI 跟投", "Snorkel AI（跟投）", "投过 Pika（华人创始人）", ""),
    ("sig", 2, "Susquehanna（SIG）", "战略投资", "美国（费城）", "未找到", "先确认 SIG 投资部门对接人",
     "https://techcrunch.com/2026/03/25/deccan-ai-raises-25m-as-ai-training-push-relies-on-india-based-workforce", "低", "Hi [name],",
     "SIG joined Deccan AI's Series A in human data for AI training. We're a team from Citadel, Millennium and Jane Street building finance RL environments and expert data.",
     "量化做市机构投过人类数据公司，背景相通；对接人需找。",
     "Deccan AI A 轮", "Deccan AI（人类数据）", "未找到", ""),
    ("altos", 2, "Altos Ventures", "VC", "美国", "Zac Mohring", "AfterQuery 董事",
     "https://www.businesswire.com/news/home/20260409469482/en/AfterQuery-Raises-$30-Million-Series-A-Round-at-$300-Million-Valuation", "高", "Hi Zac,",
     "You called human data \"an enormous market and critical bottleneck for frontier models.\" We agree, and we think the next bottleneck is environments and verifiers, which is where SimReal focuses, starting in finance.",
     "判断和我们完全一致，但 AfterQuery 是最直接的竞品，大概率不投；可以听反馈。",
     "AfterQuery A 轮领投", "AfterQuery（最直接竞品之一）", "未找到", ""),
    ("sequoia", 2, "Sequoia Capital", "VC", "美国", "未找到（Irregular 投资文作者为 Shaun Maguire、Dean Meyer）", "负责 Fleet 的合伙人未找到",
     "https://sequoiacap.com/article/partnering-with-irregular-ahead-of-the-curve/", "低", "Hi [name],",
     "Sequoia backed Fleet and Irregular, so you've seen both training environments and evaluations up close. We're building finance environments with automatic verifiers.",
     "多家 RL/评测公司股东，但持有 Fleet，负责人不明。",
     "Fleet；Irregular；Applied Compute；Ineffable Intelligence", "Fleet", "未找到", ""),
    ("datadog", 2, "Datadog", "战略投资", "美国", "未找到", "企业发展/战略投资部门，先确认对接人",
     "https://investors.datadoghq.com/news-releases/news-release-details/datadog-acquires-adaptive-ml-accelerate-its-investment-ai", "低", "Hi [name],",
     "Datadog backed Patronus and acquired Adaptive ML this year. We build finance RL environments with automatic verifiers, the kind of training and evaluation layer those teams work with.",
     "收购了 Adaptive ML，是后训练的买家和潜在退出方；战略沟通为主。",
     "Patronus AI A/B 轮；收购 Adaptive ML", "Patronus AI", "未找到", ""),
    ("yc", 2, "Y Combinator", "加速器", "美国", "批次申请", "走官网申请，不发邮件",
     "https://www.ycombinator.com/companies/industry/Reinforcement%20Learning", "中", "",
     "",
     "本赛道孵化最多（AfterQuery、HUD、Halluminate、Datacurve 等），但批次内竞品多。",
     "AfterQuery；HUD；Halluminate；Datacurve；Refresh；Andon Labs 等", "AfterQuery；HUD；Halluminate；Datacurve", "未找到",
     "YC 走批次申请，不发冷邮件。"),
    # ---- Wave 3 ----
    ("chemistry", 3, "Chemistry", "VC", "美国", "Mark Goldberg", "领投 Datacurve",
     "https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/", "中", "Hi Mark,",
     "Your piece \"RL Reigns Supreme\" and the Datacurve investment make Chemistry one of the few firms with a written view on this market. We're building the finance side of it: trading and financial-close environments with automatic verifiers.",
     "有 RL 投资论文，领投过年轻创始人的数据公司，对华人团队友好；持有 Datacurve（编码方向）。",
     "Datacurve A 轮领投", "Datacurve（编码数据与环境）", "Datacurve 联合创始人被 36Kr 报道为华人（国籍未核实）", ""),
    ("kleiner", 3, "Kleiner Perkins", "VC", "美国", "Leigh Marie Braswell", "合伙人；据摘要领投 Applied Compute 并任董事，曾在 Scale AI",
     "https://www.kleinerperkins.com/people/leigh-marie-braswell/", "中", "Hi Leigh Marie,",
     "You led Applied Compute's round and worked at Scale before that, so you've seen both the data side and the training side. We build finance RL environments with verifiers written by people from Citadel and Jane Street.",
     "合伙人懂数据业务；Applied Compute 是潜在客户，可形成组合协同。",
     "Applied Compute 领投 $80M；LMArena 跟投", "无", "未找到", ""),
    ("index", 3, "Index Ventures", "VC", "美国/欧洲", "未找到", "负责 Moment、Adaptive ML 的合伙人未找到，先查官网",
     "https://www.bloomberg.com/news/articles/2026-05-19/former-citadel-quants-raise-78-million-for-ai-fintech-moment", "低", "Hi [name],",
     "Index has now led two rounds for Moment, a team of former Citadel Securities quants. We're another team from Citadel, Millennium and Jane Street, building finance RL environments for AI labs.",
     "唯一查到连续领投前 Citadel 量化团队的一线基金，也领投过后训练平台种子轮。",
     "Adaptive ML 种子领投；Moment B、C 轮领投；Matrices 种子", "Scale AI（老股东）", "未找到", ""),
    ("a16z", 3, "a16z", "VC", "美国", "Jennifer Li", "GP，基础设施（Martin Casado 领投 Deeptune，可抄送）",
     "https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/", "中", "Hi Jennifer,",
     "You said the big labs are building RL environments in-house but also looking at third-party vendors because the work is so complex. We're one of those vendors, focused on finance.",
     "公开且明确的 RL 环境投资论点；Deeptune 被收购后留有空位；跟投过前 Citadel 团队的 Moment。",
     "Deeptune A 轮领投；Vals AI A 轮领投；LMArena；Braintrust", "Deeptune（已被 Mercor 收购）", "未找到", ""),
    ("general-catalyst", 3, "General Catalyst", "VC", "美国", "Yuri Sagalov", "董事总经理，负责种子项目，领投 Arga",
     "https://www.generalcatalyst.com/team/yuri-sagalov", "中", "Hi Yuri,",
     "You told TechCrunch that a repeatable sandbox environment matters much more with agents than it did with humans. We're building that for finance: trading and financial-close environments with automatic verifiers.",
     "合伙人专做种子，刚领投企业 RL 沙箱，观点和我们高度一致；要回应与 Mercor 的关系。",
     "Arga Labs 种子领投；Mercor 种子领投；Haize Labs；General Intuition", "Mercor；Arga Labs", "未找到", ""),
    ("hrt", 3, "HRT Ventures（Hudson River Trading）", "战略投资", "美国（纽约）", "未找到", "先通过官网 ventures 页或前同事渠道找负责人",
     "https://www.hudsonrivertrading.com/ventures/", "低", "Hi [name],",
     "HRT backed Vals and Gray Swan this year. We're a team from Citadel, Millennium and Jane Street building finance RL environments and verifiers for AI labs.",
     "量化机构本身，背景最契合，今年连投两家评测公司；最重要，放最后，等话术成熟再发。",
     "Vals AI A 轮；Gray Swan AI A 轮", "无", "未找到", ""),
    ("jane-street", 3, "Jane Street", "战略投资", "美国（纽约）", "前同事渠道", "不发冷邮件",
     "https://www.coreweave.com/news/jane-street-and-coreweave-announce-seed-investment-in-numerata-developer-of-ai-powered-software-development-tools", "中", "",
     "",
     "团队前东家之一，以机构名义领投过 AI 种子轮（Numerata），也是金融 RL 环境的潜在客户。",
     "Numerata 种子领投（非本赛道）", "无", "未找到",
     "前东家，走前同事内部引荐，不发冷邮件；注意前雇主关系。"),
]

NOT_NOW = [
    ("khosla", "Khosla Ventures", "创始人公开说 \"We'll never be in China.\"，中国籍创始人团队匹配度低"),
    ("founders-fund", "Founders Fund", "合伙人对 Benchmark 投 Manus 被审查一事公开嘲讽，对华态度偏鹰派"),
    ("benchmark", "Benchmark", "深度绑定 Mercor；投 Manus 后遭美国财政部审查"),
    ("felicis", "Felicis", "两轮领投 Mercor，且偏 A 轮以后"),
    ("01-advisors", "01 Advisors", "领投 micro1（专家数据直接竞品）"),
    ("radical", "Radical Ventures", "领投 Prime Intellect，偏大额 A 轮"),
    ("bcv", "Bain Capital Ventures", "持有 Fleet，负责人不明"),
    ("growth", "Insight Partners、S32、Addition、Vanara、Thrive、Accel、Bezos Expeditions、Greenfield", "成长期基金或已投竞品，种子阶段不对口"),
    ("strategic-late", "NVIDIA、GV、Intel Capital、Dell Technologies Capital", "战略投资多在后期，覆盖多家竞品"),
    ("angels-hard", "Noam Brown、Jeff Dean、Patrick Collison、Nat Friedman / Daniel Gross", "可及性低；Friedman 和 Gross 已进入 Meta"),
    ("foody", "Brendan Foody（Mercor CEO）", "直接竞品创始人"),
]


def build():
    docs = []
    for i, r in enumerate(INVESTORS, 1):
        (slug, wave, name, typ, region, contact, role, url, conf,
         sal, opening, why, deals, conflicts, china, no_email) = r
        docs.append({
            "slug": slug, "order": i, "wave": wave, "waveLabel": WAVES[wave],
            "name": name, "type": typ, "region": region,
            "contact": contact, "role": role, "contactUrl": url, "confidence": conf,
            "salutation": sal, "opening": opening, "why": why,
            "deals": deals, "conflicts": conflicts, "china": china, "noEmail": no_email,
        })
    for j, (slug, name, reason) in enumerate(NOT_NOW, 1):
        docs.append({
            "slug": slug, "order": 900 + j, "wave": 9, "waveLabel": WAVES[9],
            "name": name, "why": reason,
        })
    return docs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "build" / "investors"))
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    docs = build()
    for d in docs:
        (out / (d["slug"] + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(docs), "documents written to", out)


if __name__ == "__main__":
    main()
