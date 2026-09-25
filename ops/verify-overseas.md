# 海外公司核实报告（2026-09-25）

范围：12 份海外草稿核实 + 新增 Scale AI。所有邮件 `python3 tools/check_drafts.py` 均为 match: True，无禁用词。本次共用 WebSearch 68 次（上限 200）。

12 份核实草稿的联系人都仍在职，开场白事实均已核实，邮件正文一处未改；改动集中在来源链接（GitHub 副本换成原始发布方）和 核实说明。

## Anthropic
- 状态：fixed（只改了来源和核实说明，联系人和开场白核实无误）
- 变更：
  - 联系人 Jared Kaplan 确认仍是联合创始人兼 Chief Science Officer，没有查到离职的报道：https://www.anthropic.com/company/leadership 、https://www.hertzfoundation.org/people/jared-kaplan/ 、https://en.wikipedia.org/wiki/Jared_Kaplan
  - 开场白中的 Excel 并购模型测试和 Optiver "highest score we've recorded" 已经核实，开场白不变：https://www.anthropic.com/claude-opus-5-5 、https://www.vellum.ai/blog/claude-opus-5-5-benchmarks-explained 、https://www.technology.org/2026/09/23/anthropic-claude-opus-5-5-launch-pricing-benchmarks/
  - 第三方 GitHub 时间线（jqueryscript/anthropic-claude-timeline）换成了官方新闻页 https://www.anthropic.com/news
  - GitHub 上的招聘页快照（bojieli/ai-infra-book）标注为副本，原始岗位链接是 Greenhouse
  - 更新了核实说明
- prospects.csv 行：`Anthropic|frontier lab|海外|Jared Kaplan|联合创始人兼 Chief Science Officer（备选联系人，数据负责人未找到）|https://www.anthropic.com/company/leadership ; https://www.anthropic.com/claude-opus-5-5|财务结账、对账、报表审计环境（结果可以用程序验证），对应 Domain Scaling 团队的金融方向；Xitadel 作为可训练的交易环境；补会计师、买方和交易从业者|中`

## Balyasny Asset Management（Applied AI 团队）
- 状态：verified unchanged（邮件不变；核实说明做了补充）
- 变更：
  - Charlie Flanagan 确认是 Chief AI Officer、Management Committee 成员，没有查到离职的报道：https://www.bamfunds.com/about-us/leadership/charlie-flanagan （搜索摘要）、https://theorg.com/org/bamfunds/org-chart/charlie-flanagan 、https://www.hedgeweek.com/balyasny-launches-ai-fellowship-to-embed-specialists-in-trading-teams/
  - 开场白中的 "thousands of real-world financial tasks with verifiable outcomes across equities, macro and commodities" 和 BAMAgent 已经核实，开场白不变：https://claude.com/blog/working-at-the-frontier-how-balyasny-asset-management-evaluates-and-governs-claude-fable-5
  - 之前没能核实的 OpenAI 客户案例，这次在 BAM 官网找到，已补进最近发布和核实说明：https://www.bamfunds.com/news-and-insights/balyasny-openai-feature
  - 来源里没有 GitHub 副本
- prospects.csv 行：`Balyasny Asset Management（Applied AI 团队）|金融机构 AI 团队|海外|Charlie Flanagan|Chief AI Officer|https://claude.com/blog/working-at-the-frontier-how-balyasny-asset-management-evaluates-and-governs-claude-fable-5 ; https://www.bamfunds.com/about-us/leadership/charlie-flanagan|可验证结果的金融任务和验证器、预测类任务、长流程 agent 评测环境和专家评分，不是 SFT 或原始后训练数据（BAM 不训练模型）|高`

## Google DeepMind
- 状态：fixed（只改了来源和核实说明，联系人和开场白核实无误）
- 变更：
  - Tulsee Doshi 确认仍在职：CNBC 2026-09-02 称她是 senior director of product management，The Hacker News 2026-09 的报道也引用了她的话：https://www.cnbc.com/2026/09/02/google-starts-september-with-ai-momentum-after-long-losing-streak.html 、https://thehackernews.com/2026/09/google-anthropic-and-openai-unveil.html
  - 开场白中 3.8 Flash 在 Vals Finance Agent V2 和 Harvey Legal Agent Benchmark 上超过 3.7 Flash 和其他前沿模型，已经核实，开场白不变：https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ 、https://www.vellum.ai/blog/gemini-3-8-flash-benchmarks-explained 、https://www.datacamp.com/blog/gemini-3-8-flash-cyber
  - 核实说明里的博客 GitHub 镜像（ia3andy/devoured）已删掉，改用 blog.google 原文
  - SemiAnalysis 的观点换成了原文链接 https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence （付费）；hczhu 的二手笔记只作为标注过的副本保留
  - 更新了核实说明
- prospects.csv 行：`Google DeepMind|frontier lab|海外|Tulsee Doshi|Senior Director，Gemini 模型产品负责人（Head of Product, Gemini Models）|https://blog.google/authors/tulsee-doshi/ ; https://www.cnbc.com/2026/09/02/google-starts-september-with-ai-momentum-after-long-losing-streak.html ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/|3.8 Flash 公开用 Vals Finance Agent V2 和 Harvey Legal Agent Benchmark 当卖点，Xitadel、财务结账环境和金融、法律专家写的评分标准可以对上金融和法律 agent 的训练与评测|中`

## Harvey
- 状态：verified unchanged
- 变更：
  - 联系人和开头一句都没改。官方作者页 https://www.harvey.ai/blog/author/niko-grupen 、Google Cloud Next 讲者页 https://www.googlecloudevents.com/next-vegas/speaker/2188391/niko-grupen 和 The Org 都写 Niko Grupen 是 Head of Applied Research。2026-09 初他还以 Harvey 身份在 Artificial Lawyer 上发表评论（https://www.artificiallawyer.com/2026/09/07/harvey-legora-on-openais-gpt-6-astra/ ）。没有查到离职消息。
  - 开头一句（Tenet 用公开法律数据、合成数据和模拟长程法律工作的人类专家数据做后训练）已核实。依据是 Harvey 官方 X 帖 https://x.com/harvey/status/2090454750059958440 ，Harvey 博客 https://www.harvey.ai/blog/post-training-update-harvey-tenet 、Fireworks 博客 https://fireworks.ai/blog/post-training-kimi-k3-with-harvey-for-long-horizon-legal-work 和 MarkTechPost 的说法一致。
  - 融资备注补了日期（2026-09-09）和原始链接：官方博客 https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence 、TechCrunch https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/ 。原来只引了 Benzinga 的概述。
  - 来源里没有 GitHub 转载的新闻。核实说明已补上本次复核的内容。
- prospects.csv 行：`Harvey|垂直 AI（法律）|海外|Niko Grupen|Head of Applied Research|https://www.harvey.ai/blog/author/niko-grupen ; https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark ; https://x.com/nikogrupen/status/2097369705791307952|最直接的是长程任务和评分标准。Tenet 明确用了 "human expert data simulating long-horizon legal work"。LAB 的任务格式是公开的，我们的律师可以直接按 task.json 格式写新任务和 pass/fail 评分标准，覆盖它们还薄的领域和法域。|高`

## McKinsey – QuantumBlack
- 状态：verified unchanged
- 变更：
  - 联系人没改。McKinsey 官网个人页 https://www.mckinsey.com/our-people/tomas-lajous 和 AI Magazine（https://aimagazine.com/executive/tomas-lajous ）的搜索摘要都写 Tomás Lajous 是 Senior Partner、QuantumBlack Labs 全球负责人，没有查到离职消息。但没有带 2026 年日期的官方确认，置信度维持中。官网个人页已加到来源第一条。
  - 开头一句已核实，没改。依据是 Google Cloud Press Corner 新闻稿（2026-04-22）https://www.googlecloudpresscorner.com/2026-04-22-McKinsey-and-Google-Cloud-Launch-the-McKinsey-Google-Transformation-Group-to-Scale-Enterprise-Impact-for-the-AI-era ，McKinsey 博客、PR Newswire 和 Yahoo Finance 的说法一致："QuantumBlack technologists will collaborate with Google's forward deployed engineers (FDEs) to work on challenging client use cases"。
  - 来源里没有 GitHub 转载的新闻。ARK 仓库是 McKinsey 自己的项目，保留。核实说明已更新。
- prospects.csv 行：`McKinsey – QuantumBlack|咨询公司 AI 团队|海外|Tomás Lajous|Senior Partner，QuantumBlack Labs 全球负责人|https://www.mckinsey.com/our-people/tomas-lajous ; https://aimagazine.com/news/quantumblack-a-global-force-in-agentic-ai-transformation ; https://www.mckinsey.com/capabilities/quantumblack/labs ; https://www.linkedin.com/posts/tomaslajous_i-am-excited-to-join-quantumblack-labs-as-activity-7287499245123715074-7hRQ|最匹配的是客户 agent 的验收评测。他们给金融机构和受监管行业做中后台 agent（Agents at Scale、AppliedAI 合作），可以提供专家写的评分标准和领域评测集，按业务流程做验收测试。|中`

## Mercor
- 状态：fixed（只改了备注，邮件没改）
- 变更：
  - 联系人没换。Bertie Vidgen 仍在 Mercor：LinkedIn 标题（搜索摘要）写 "AI Researcher @ Mercor"，另有搜索摘要说他任 Strategic Project Lead；他也是 2026-07 APEX-Accounting 的作者。原来置信度说明里的 "Head of Human Data" 找不到佐证，已删掉，置信度维持中，发送前仍需人工确认职位。
  - 开头一句已核实，没改。它讲的是 Mercor 需要专家，符合人类数据供应商开头一句的要求。APEX-Accounting 的 "authored and solved by experts in accounting and bookkeeping" 在 arXiv https://arxiv.org/abs/2607.27189 、Ramp Labs https://labs.ramp.com/apex-accounting 和 Mercor newsletter https://www.mercor.com/apex/newsletter/introducing-apex-accounting-built-with-ramp/ 里说法一致。APEX-Agents 的任务由投行分析师、咨询顾问和公司律师编写，见 https://www.mercor.com/blog/introducing-apex-agents/ 和 Epoch AI https://epoch.ai/benchmarks/apex-agents 。
  - Deeptune 收购原来标注为"GitHub 新闻简报转引 Fortune"，已确认 Fortune 原文存在，并补上 Mercor 官方博客 https://www.mercor.com/blog/mercor-to-acquire-deeptune/ 和 SiliconANGLE https://siliconangle.com/2026/07/09/mercor-buys-deeptune-build-training-environments-ai-agents/ 。APEX-Accounting 条目补了 Ramp 和 Mercor 的官方链接。核实说明已更新。
- prospects.csv 行：`Mercor|人类数据供应商|海外|Bertie Vidgen|APEX 基准系列的主导作者|https://github.com/Mercor-Intelligence/archipelago ; https://arxiv.org/abs/2601.14242 ; https://arxiv.org/abs/2607.27189|最对口的是会计和财务结账。APEX-Accounting 从出题、解题到评分标准全由会计和簿记专家完成，我们的财务结账环境和会计专家可以直接对上，做成他们能转售的环境，或者补专家。|中`

## Meta Superintelligence Labs
- 状态：fixed（联系人和开场白核实无误，只替换了来源）
- 变更：
  - 联系人 Alexandr Wang 核实：Meta 官网领导层页面 https://www.meta.com/about/leadership/alexandr-wang/ 、CNBC 2026-06-14 https://www.cnbc.com/2026/06/14/meta-hired-alexandr-wang-to-build-ai-its-zuckerbergs-job-to-sell-it.html ，2026-09-23 在 Meta Connect 演讲（搜索摘要），没有离职消息。已补进来源。
  - 开场白（Muse Spark 健康训练数据 "1,000+ physicians"）已核实：https://ai.meta.com/blog/introducing-muse-spark-msl/ 、https://www.helpnetsecurity.com/2026/04/09/meta-muse-spark-personal-superintelligence/ 、https://healthcare-digital.com/news/metas-muse-spark-physician-informed-ai-in-healthcare 。开场白不改。
  - 备选 Maher Saba 的来源原是 GitHub 二手转述，已换成原文：https://the-decoder.com/meta-creates-new-applied-ai-engineering-division/ 、https://www.eweek.com/news/meta-forms-new-ai-engineering-org-superintelligence/ （2026-03 成立，由他牵头，其中一个团队负责任务、数据采集和评测）
  - SemiAnalysis 的 GitHub 副本（raw.githubusercontent.com/hczhu/...）已换成原文：https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence （付费墙）
  - 核实说明已更新。
- prospects.csv 行：`Meta Superintelligence Labs|frontier lab|海外|Alexandr Wang|Meta Chief AI Officer，Meta Superintelligence Labs（MSL）负责人（备选联系人，数据负责人未找到）|https://www.meta.com/about/leadership/alexandr-wang/ ; https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/ ; https://www.cnbc.com/2026/06/14/meta-hired-alexandr-wang-to-build-ai-its-zuckerbergs-job-to-sell-it.html ; https://fortune.com/2026/07/09/meta-muse-spark-1-1-release-alexandr-wang-superintelligence-labs-mark-zuckerberg/|只做员工替代不了的持证专家领域：医生、律师写的评分标准和评测集；金融方向用 Xitadel 和财务结账环境做小批量试点|中`

## OpenAI
- 状态：fixed（联系人和开场白核实无误，只替换了来源）
- 变更：
  - 联系人 Phoebe Thacker 核实：2026-04 伦敦办公室报道 https://www.cnbc.com/2026/04/13/openai-london-office-sam-altman-uk-stargate.html 、https://tech.eu/2026/04/13/openai-to-move-to-first-permanent-london-office-with-capacity-to-more-than-double-headcount/ 、Border Telegraph；LinkedIn 标题仍是 Head of Human Data Ops（搜索摘要）。没有查到 2026 年离职或转岗。置信度维持中，因为没有读到官方页面原文。
  - 开场白（2026-09-10 基于 GPT-6 Astra 发布 ChatGPT for Financial Services，先面向投行和股票研究）已核实：https://openai.com/index/introducing-chatgpt-financial-services/ 、https://www.cnbc.com/2026/09/10/openai-chatgpt-for-financial-services-targets-work-of-junior-bankers.html 、https://pulse2.com/openai-launches-chatgpt-for-financial-services-with-gpt-6-astra-and-built-in-premium-data/ 。开场白不改。
  - GPT-5.5 的 GitHub 时间线链接（jqueryscript/chatgpt-timeline）已换成官方页：https://openai.com/index/introducing-gpt-5-5/
  - 核实说明已更新。
- prospects.csv 行：`OpenAI|frontier lab|海外|Phoebe Thacker|Global Head of Data Research Programmes 兼 London Site Lead|https://www.cnbc.com/2026/04/13/openai-london-office-sam-altman-uk-stargate.html ; https://tech.eu/2026/04/13/openai-to-move-to-first-permanent-london-office-with-capacity-to-more-than-double-headcount/ ; https://www.startuphub.ai/people/phoebe-thacker|投行和股票研究 OpenAI 已自己覆盖；可补交易（Xitadel）和财务结账 / 会计两块，以及表格和财务模型的 verifier 与专家评分标准|中`

## OpenEvidence
- 状态：fixed（联系人和开场白核实无误，只替换了来源）
- 变更：
  - 联系人 Sam Finlayson 核实：通过 raw.githubusercontent.com 重读主页源码，仍写 "SVP of Medical AI, OpenEvidence"；2026-07-10 EvidenceGrade 官方新闻稿也以这个头衔引用他。置信度维持高。
  - 开场白（EvidenceGrade 给每个回答下面引用的证据评级）已核实：https://www.prnewswire.com/news-releases/openevidence-launches-evidencegrade-empowering-physicians-to-see-the-strength-of-cited-evidence-beneath-each-ai-answer-302822750.html 、https://hitconsultant.net/2026/07/13/openevidence-launches-evidencegrade-medical-ai/ 、https://www.fiercehealthcare.com/ai-and-machine-learning/openevidence-launches-medical-ai-copilot-feature-grades-medical-evidence 。开场白不改。
  - 融资和出售传闻原先引用两个 GitHub 新闻摘要，已换成：Axios 2026-09-25 https://www.axios.com/pro/health-tech-deals/2026/09/25/openevidence-250m-raise-15b-valuation-a16z （150 亿美元估值融 2.5 亿美元，a16z 和 Byers 领投）；AI Weekly 转述 Business Insider 的出售传闻 https://aiweekly.co/alerts/openevidence-raises-250m-at-15b-25-above-januarys-12b-mark-and-weighing-sale （BI 原文链接没找到）；Dealroom 转述的进入肿瘤药研发报道 https://dealroom.co/news/155918-openevidence-raises-250m-at-15b-pivots-into-drug-development/
  - 官方公告的 GitHub 镜像补上原始页面 https://www.openevidence.com/announcements ，镜像保留并标为副本；EvidenceGrade 条目补上 PR Newswire 新闻稿链接。
  - 核实说明已更新。
- prospects.csv 行：`OpenEvidence|垂直 AI（医疗）|海外|Samuel (Sam) Finlayson|SVP of Medical AI|https://sgfin.github.io/ ; https://www.prnewswire.com/news-releases/openevidence-launches-evidencegrade-empowering-physicians-to-see-the-strength-of-cited-evidence-beneath-each-ai-answer-302822750.html|按专科提供医生写的评测集、校准集和评分标准，覆盖引用准确性和证据等级判断，对接 EvidenceGrade 和子专科模型|高`

## Rogo
- 状态：verified unchanged
- 变更：
  - 邮件无改动。开头一句的“928 道题、由前金融从业者编写、15,000+ 条评分标准”与 Rogo 官方 X 帖原话一致（https://x.com/RogoAI/status/2059743405203480888 ），arXiv 和 Hugging Face 数据集页的摘要也吻合（https://arxiv.org/abs/2606.03829 、https://huggingface.co/datasets/RogoAI/big-finance-benchmark ）。
  - 联系人 Alex Wang：LinkedIn 搜索摘要显示 "AI @ Rogo"，他是 BigFinanceBench 第一作者，单位 Rogo，2026-09 的 Anthropic 页面也引用了他，判断仍在职。正式头衔仍未查到，置信度保持中。
  - 核实说明里补充了 2026-09-25 的复核记录。本稿没有 GitHub 镜像链接。
- prospects.csv 行：`Rogo|垂直 AI（金融）|海外|Alex Wang|Applied AI（Anthropic 官方页面上的写法，未写是否带团队）|https://www.anthropic.com/claude-fable-and-mythos-5-1 ; https://arxiv.org/abs/2606.03829|最直接的是评分标准和评测集。BFB 的 50 题已经公开，又被 OpenAI、Anthropic 拿去做发布评测，需要持续补充不公开的新题。52 位出题人规模不大，我们的专家供给可以扩到私募信贷、重组、PE 尽调等 BFB 还没覆盖好的流程。|中`

## Surge AI
- 状态：fixed（只改了来源链接和备注，邮件没改）
- 变更：
  - 邮件无改动。开头一句逐项对照 Chartography README 原文核实（通过 raw.githubusercontent.com 读取，https://github.com/surge-ai/chartography ）："written by someone who reads these charts for a living … independently verified by three additional experts"，领域包括工程、金融、供应链、医疗；Surge 博客的搜索摘要表述一致（https://surgehq.ai/blog/chartography ）。
  - 联系人 Sushant Mehta：LinkedIn 搜索摘要显示 "Post-Training Research at Surge AI"，仍在职。头衔已写进表头，置信度保持中。
  - Lenny's Podcast 文字稿原来链接到 GitHub 副本，已换成节目原页面：https://www.lennysnewsletter.com/p/surge-ai-edwin-chen
  - 博客 RSS 原来链接到 GitHub 镜像，已换成 Surge 博客原址：https://www.surgehq.ai/blog
  - HANDBOOK.md 原来链接到第三方笔记，已换成 Surge 官方仓库：https://github.com/surge-ai/handbook
  - Chartography 论文原先读的全文来自 GitHub，现在标注为“副本”，链接本身就是 arXiv 原址。
- prospects.csv 行：`Surge AI|人类数据供应商|海外|Sushant Mehta|Surge AI 研究员（LinkedIn 标题 Post-Training Research at Surge AI，搜索摘要），负责 RL 环境和专家基准|https://arxiv.org/abs/2602.16179 ; https://arxiv.org/abs/2608.10677 ; https://arxiv.org/abs/2607.25398 ; https://www.linkedin.com/in/sushant-mehta/|专家供给：Surge 的基准都要多名专家出题加复核（Chartography 每题 4 人），领域集中在金融、医疗账单/保险、工程、供应链、HR、数学。我们可以补高校博士生和资深从业者，重点是金融、会计、医疗、工程。|中`

## xAI (SpaceXAI)
- 状态：verified unchanged（邮件没改，公司结构备注有修正）
- 变更：
  - 邮件无改动。Grok 4.7 "trained with a longer reinforcement learning run … weighted toward problems that take many hours to complete" 在 x.ai 官方页面摘要、The New Stack 和 MarkTechPost 里一致（https://x.ai/news/grok-4-7 、https://thenewstack.io/grok-4-7-agent-stamina/ 、https://www.marktechpost.com/2026/09/21/spacexai-releases-grok-4-7/ ）。
  - 公司名 SpaceXAI 仍然正确：x.ai 官方页面标题是 "Introducing Grok 4.7 | SpaceXAI"，2026-07-06 xAI 的 X 账号改为 @SpaceXAI（https://finance.yahoo.com/technology/ai/articles/xai-makes-rebrand-spacexai-complete-215010760.html 、https://dataconomy.com/2026/07/07/elon-musk-rebrands-merged-xai-and-spacex-as-spacexai/ ）。有的媒体说成 SpaceX 整体改名为 SpaceXAI（https://www.socialmediatoday.com/news/spacex-rebrands-as-spacexai/824656/ ），X 归属的说法也不统一。原备注写的是“X 也归在它下面”，已改成注明各方说法不一。
  - 联系人 Jack Garabedian：2026-09 关于 SpaceX 购买倒闭创业公司数据的报道提到他接手后在整顿 human data 团队（https://thenextweb.com/news/spacex-dead-startups-data-grok ，搜索摘要），判断 9 月仍在任，已写进置信度说明，置信度保持中。
  - 本稿没有 GitHub 镜像链接。TradingView 上的是路透快讯转载，路透原文打不开，所以保留。
- prospects.csv 行：`xAI (SpaceXAI)|frontier lab|海外|Jack Garabedian|人类数据团队（human data team，也就是训练 Grok 的 AI tutor 团队）负责人|https://www.bloomberg.com/news/articles/2026-06-09/musk-s-xai-taps-starlink-staffer-to-run-grok-training-team ; https://www.tradingview.com/news/reuters.com,2026:newsml_FWN42G143:0-jack-garabedian-a-starlink-engineer-will-be-taking-over-the-human-data-team-at-xai-bloomberg-news/ ; https://tribune.net.ph/2026/06/09/xai-shakes-up-grok-leadership ; https://thenextweb.com/news/spacex-dead-startups-data-grok|最匹配的是金融。他们明确在找信用、银团和投资方面的专家，所以 Xitadel、财务结账环境和金融专家写的评分标准都用得上。Grok 4.x 主打知识工作和企业市场，也是同一个方向。|中`

## Scale AI
- 状态：new
- 变更：
  - 新建 drafts/scale-ai.md。收件人 Yuan Xue（Emily），Head of Enterprise AI：本人主页写明职位（https://yuanxue.github.io/ ，源文件已读），2026-08 CliniCARE-Bench 末位作者兼 scale.com 联系人（https://arxiv.org/abs/2608.07796 ，搜索摘要），入职博客 https://scale.com/blog/why-i-joined-scale-yuan-xue 。她不是专家供给负责人，置信度定为中。
  - 专家供给 / 合作负责人未找到。备选 Xiaote Zhu（Outlier GM，2024-11 任命，Forbes 2025-03 仍称 GM，2026 在职未确认，低）：https://scale.com/blog/new-era-outlier 、https://www.forbes.com/sites/richardnieva/2025/03/06/scale-ai-outlier-us/ ；Francis deSouza（CEO，2026-08-10 起，高）：https://scale.com/blog/scale-appoints-new-ceo 、https://www.axios.com/2026/07/30/scale-ai-google-cloud-coo-francis-desouza
  - 领导层：Alexandr Wang 2025-06 去了 Meta；Jason Droege 2025-06 起任临时 CEO，已由 deSouza 接任（Bloomberg、Axios、官方新闻稿一致）。
  - 开场白的事实已用 README 原文核实：DrugDiscoveryBench 的 82 个任务 "graded by an LLM judge against expert-authored rubrics"（https://github.com/scaleapi/DrugDiscoveryBench ）；CliniCARE-Bench 25 个 scenario × 30 = 750 个 case（https://github.com/scaleapi/clinicare ）；RSI Bench 邀请外部专家贡献任务（https://github.com/scaleapi/rsi-benchmark ）。早先记录的仓库创建日期因 GitHub API 不可用未复核；SWE-Atlas / SWE-Interact / MCP Atlas 未复核，未使用。
  - 在招的专家领域：Human Frontier Collective 招 STEM Fellow（CS、ML、物理、生物、化学、数学等 PhD）和 Medical Fellow（MD/DO），另有金融、法律方向，US 和 UK 都在招（搜索摘要）：https://hfc.scale.com/ 、https://scale.com/careers/4574113005 、https://scale.com/careers/4591782005 、https://scale.com/careers/4612329005 ；scale.com/experts 称覆盖 "40+ subject domains"：https://scale.com/experts
  - Meta 投资的影响：2025-06 Meta 投资 143 亿美元、持股 49%，据 Reuters 报道 Google（最大客户）计划终止合作，OpenAI、Microsoft、xAI 也在收缩；2025-07 裁员约 200 名员工和 500 名承包商：https://www.techmeme.com/250613/p23 、https://techcrunch.com/2025/06/14/google-reportedly-plans-to-cut-ties-with-scale-ai 、https://www.cnbc.com/2025/07/16/scale-ai-cuts-14percent-of-workforce-after-meta-investment-hiring-of-wang.html
- prospects.csv 行：`Scale AI|人类数据供应商|海外|Yuan Xue|Head of Enterprise AI；CliniCARE-Bench 负责人（专家供给负责人未找到）|https://yuanxue.github.io/ ; https://arxiv.org/abs/2608.07796 ; https://github.com/scaleapi/DrugDiscoveryBench ; https://github.com/scaleapi/clinicare ; https://hfc.scale.com/|专家供给合作：补 CliniCARE-Bench、DrugDiscoveryBench 和 HFC 需要的临床、生命科学专家，另有金融、法律和 AI 研究（RSI Bench）；按 Harbor 格式交付环境和评分标准|中`
