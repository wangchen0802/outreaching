# 核实报告：国内公司（中文邮件 + 微信版）

日期：2026-09-25。本次会话约用了 80 次 WebSearch。官网、新闻站、交易所公告站、federalregister / ecfr / trade.gov 在本环境都打不开（WebFetch 和 curl 都被拦），所以媒体类事实都来自搜索摘要，一手原文只读了 GitHub 上的仓库 README 和个人主页源文件。13 份草稿都跑过 `python3 tools/check_drafts.py`，邮件和微信版都是 `match: True`，没有命中禁用词。

没有改动任何邮件开头句，只新增了两份草稿的开头句（数据堂、幂律）。

跨公司的一条新发现：2026-09-08 NSA、CISA、FBI 联合通报，点名 DeepSeek、Moonshot AI、阿里、MiniMax、阶跃星辰和 Z.ai 对美国前沿模型做工业级蒸馏（https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a ）。另据 CNBC 2026-06-17，美国商务部自 2025-10 起没有再新增实体清单条目，DeepSeek 的列入已获跨部门批准，但被白宫暂缓（https://www.cnbc.com/2026/06/17/us-deepseek-blacklist-cxmt-national-security-risks-.html ）。已写进相关草稿的风险一节。

---

## 百川智能 Baichuan

**状态**：核实，未改邮件（只改了备注和来源）

- 鞠强的"模型技术负责人"头衔，在 2026-01 的四个报道里一致：腾讯新闻 https://view.inews.qq.com/a/20260113A06A5000 、https://news.qq.com/rain/a/20260114A02D2L00 、36氪 https://36kr.com/p/3638614683487360 、界面/新浪 https://finance.sina.com.cn/tech/roll/2026-01-14/doc-inhhfrsv5195131.shtml 。2026-05 M4 发布的报道里仍有他（https://www.sohu.com/a/1027948979_211762 ）。没有查到离职消息。
- "鞠强 = Qiang Ju"：专门搜了中英文，仍然没有同时写出两个名字的出处，还是按拼音对应，已在草稿里注明。"Qiang Ju" 在 M2、M3、M4 的作者名单里都有。
- 实体清单：没有查到百川被列入。智谱是 2025-01 首个被列入的大模型公司；CNBC 报道称 2025-10 以后没有新增条目。清单原文打不开，发送前仍需再查一次。
- 开头一句的 SPAR++ "把奖励锚定到关键临床片段上"：arXiv HTML v2（https://arxiv.org/html/2606.08982v2 ）和 alphaXiv 中文摘要（https://www.alphaxiv.org/zh/abs/2606.08982 ）的搜索摘要都能对上，保留不改。
- M4 作者名单的来源改为 arXiv 原始链接，GitHub 订阅副本标注为副本。
- 补充：2026-07 最后一位联创茹立云离职（https://www.guandian.hk/article/20260717/574164.html ）。

CSV：百川智能 Baichuan|垂直 AI（医疗）|国内|鞠强（Qiang Ju）|模型技术负责人|https://news.qq.com/rain/a/20260114A02D2L00 ; https://36kr.com/p/3638614683487360 ; https://view.inews.qq.com/a/20260113A06A5000 ; https://github.com/baichuan-inc/Baichuan-M3-235B|M4 的 SPAR++ 要按病史采集、风险识别、工具使用逐段打分，随访、慢病、用药等新场景需要医生来写和审片段级评分标准与留出评测集|中

## 字节跳动 Seed

**状态**：核实，未改

- 重新读了钟宛君主页源文件（https://github.com/zhongwanjun/zhongwanjun.github.io ，intro.md 和 news_en.md）："one of the algorithm leads for general agent optimization"、2026.06 Seed 2.1、2026.06 豆包专业版办公任务模式（本人是算法负责人之一）、2026.04 Agent-World，开头一句的三个事实都对得上。
- 没有查到离职消息。草稿里没有需要替换的新闻镜像：36氪、华尔街见闻的原始链接本来就在，GitHub 上的研究笔记是转述，已标为二手。

CSV：字节跳动 Seed|国内大模型公司|国内|钟宛君（Wanjun Zhong）|Seed 高级研究员，通用 Agent 优化的算法负责人之一；豆包专业版办公任务模式算法负责人之一|https://zhongwanjun.github.io/ ; https://github.com/zhongwanjun/zhongwanjun.github.io/blob/master/_pages/includes/intro.md ; https://arxiv.org/abs/2604.18292|办公和知识工作类 agent 的专家任务、隐藏验证器和评分标准（财务结账、会计、金融），可按 EdgeBench / SForge 的格式交付|高

## DeepSeek 深度求索

**状态**：核实，未改邮件（补了合规信息）

- 邵智宏主页原文仍写 "I am a Research Scientist at DeepSeek"（https://github.com/zhihongshao/zhihongshao.github.io/blob/master/_pages/about.md ）；没有查到离职消息。
- 开头一句（V4 对难验证任务改用 rubric 引导的 RL 数据加生成式奖励模型，只需少量人工标注）：除了 GitHub 上的报告文本副本，Fireworks（https://fireworks.ai/blog/what-deepseek-v4-says-about-training-platforms ）和 Kili（https://kili-technology.com/blog/data-story-deepseek-v4 ）两篇独立文章也能对上，保留不改。
- 合规：补了实体清单列入被暂缓（CNBC）和 2026-09 蒸馏通报（CISA）。
- GitHub 新闻存档（Investing.com 摘要）没找到原始报道，标注为副本。补了 DeepSeek Harness 桌面版预览（2026-09-25，https://finance.sina.com.cn/tech/digi/2026-09-25/doc-iniszfcz4504743.shtml ）。

CSV：DeepSeek 深度求索|国内大模型公司|国内|邵智宏（Zhihong Shao）|DeepSeek 研究员（Research Scientist），推理 RL（GRPO、R1、DeepSeekMath-V2）|https://zhihongshao.github.io/ ; https://github.com/zhihongshao/zhihongshao.github.io/blob/master/_pages/about.md ; https://arxiv.org/abs/2606.19348|难验证任务的专家评分标准和少而多样的人工标注（金融、会计、法律），以及新领域专家模型需要的带验证器 RL 环境|中

## 海天瑞声 SpeechOcean

**状态**：核实，未改邮件（联系人确认为李科）

- 李科 vs 王晓东：李科是现任。2026-06-05 公司关于 2025 年度业绩说明会召开情况的公告写"董事、总经理李科"（搜索摘要）：https://pdf.dfcfw.com/pdf/H22_AN202606051823299557_1.pdf 。王晓东是 2023-02 至 2024-11 的前任，2024–2025 年的文件已标"离任"，那份第三方笔记写错了。
- 2026 半年报（2026-08-27）的高管名单本身没能读到：上交所、巨潮、东方财富的 PDF 都被拦，搜索也没返回这一节。所以严格说，"对照 2026 半年报核对"没有做成，用的是更早两个月的公告。发送前请手动看一眼半年报"公司董事、高级管理人员变动情况"一节。
- 开头一句（官网"大模型数据服务"：各领域专家团队，做 SFT、RLHF、DPO 和评测数据）：官网页面的搜索摘要仍然一致，保留不改。
- 一季报改为引用新浪的原始公告链接，GitHub 笔记标为转述。

CSV：海天瑞声 SpeechOcean|人类数据供应商|国内|李科|联合创始人、董事、总经理（CEO）|https://pdf.dfcfw.com/pdf/H22_AN202606051823299557_1.pdf ; https://finance.sina.com.cn/stock/aiassist/ggbd/2024-11-07/doc-incvczxs9820775.shtml ; https://ex.chinadaily.com.cn/exchange/partners/82/rss/channel/cn/columns/sz8srm/stories//WS68c927b9a310f07257748c24.html|专家供给合作：他们的专家池强在人数和语种，金融、会计、法律、医疗的博士和执业资历专家可以由我们按项目补充供给|中

## 恒生电子 Hundsun

**状态**：核实，未改邮件

- 范径武仍是总裁：2026-06-05 发布 LIGHT 6.0（新浪 https://finance.sina.com.cn/roll/2026-06-05/doc-iniakrwf9350254.shtml 、财联社 https://www.cls.cn/detail/2392024 ）；2026-04-21 的薪酬报道仍称"恒生电子总裁范径武"（https://finance.sina.com.cn/tech/roll/2026-04-21/doc-inhvheze6873927.shtml ）。开头一句保留。
- 财联社快讯改为引用原始链接（https://www.cls.cn/detail/2391730 ，另有新浪 7x24 https://wap.cj.sina.cn/pc/7x24/4918893 ），GitHub 转存标为副本。
- 备选白硕：补了 2025-09 21 世纪专访（https://www.21jingji.com/article/20250905/herald/bcd0654737c874a159f66511b4cf0c89.html ）和 2025-10 东方财富的在任来源，置信度从低提到中。

CSV：恒生电子 Hundsun|垂直 AI（金融）|国内|范径武|恒生电子副董事长兼总裁|https://finance.sina.com.cn/roll/2026-06-05/doc-iniakrwf9350254.shtml ; https://www.stcn.com/article/detail/3945768.html ; https://www.cls.cn/detail/2391730|光子平台上投研、投顾、合规智能体的从业者评分标准和验收评测集，先从评测集小批量试点|中

## MiniMax 稀宇科技

**状态**：核实，未改邮件（更正了一个日期）

- 程威宇：重新读了青稞 Talk 列表原文第 81 行（https://github.com/qingkelab/qingketalk ），条目仍在；用中文搜他的名字没有找到其他公开来源或离职报道，置信度维持中。
- Olive Song：AI Engineer 讲者页称她是 RL research lead（https://ai.engineer/speakers/olive-song ），已补进备选。
- 开头一句：M3 的 BankerToolBench 76.1，MiniMax 官网博客（https://www.minimax.io/blog/minimax-m3 ）、Qubrid、OfficeChai 都能对上；"M2.5 和金融、法律等资深从业者一起建数据、定标准"重新读了 README 原文。保留不改。
- M2.7 发布日期由 2026-04 更正为 2026-03-18（搜索摘要）。补了 2026-09 蒸馏通报。

CSV：MiniMax 稀宇科技|国内大模型公司|国内|程威宇|MiniMax 算法工程师、通用模型后训练负责人（2026-01 公开头衔）|https://github.com/qingkelab/qingketalk ; https://www.minimax.io/news/post-training-experience-and-insights-for-agent-models ; https://github.com/MiniMax-AI/MiniMax-M3|金融、投行类 cowork 任务的专家数据、评分标准和可接进 Forge 的 RL 环境（Xitadel、财务结账）|中

## 中国平安 Ping An

**状态**：已修改（替换 GitHub 镜像来源，更新备注；邮件未改）

- 王晓航：2025-07-29 起任集团 CTO 兼平安科技总经理（第一财经 https://www.yicai.com/news/102747417.html 、中国经济网）；2026-04（每经 https://www.nbd.com.cn/articles/2026-04-22/4352737.html ）、2026-08（华尔街见闻专访，腾讯新闻转载 https://news.qq.com/rain/a/20260826A08CSE00 ）、2026-09-22（每经云栖报道 https://www.nbd.com.cn/articles/2026-09-22/4588645.html ）均在任。
- 开头一句的"AI超级客服"：证券市场周刊（https://static.weeklyonstock.com/25/1121/qdy202324.html ）和读特新闻（https://m.dutenews.com/n/article/10257215 ）两个独立来源，保留不改。
- 镜像替换：财联社 GitHub 镜像 → 证券市场周刊、读特；TrendRadar 快照 → 腾讯新闻、网易转载；云栖第三方笔记 → 每经、中华网（笔记只保留在"核对不到的数字"一条）；何明科 → 财联社 https://www.cls.cn/detail/2163205 、21 世纪经济报道；ProbPlug → arXiv https://arxiv.org/abs/2609.10122 ；校招 → 新浪原文；十大头条 → 证券市场周刊、观察者网（并更正："7+N+1"是 2025-06 发布的）。2025-11-19 那条财联社快讯本身没找到单独链接，GitHub 转存标为副本保留。
- 云栖数字：Token 300 亿到 3000 亿以上、"一句话办事"4 个月覆盖 300 多项服务、使用人次破亿，媒体能对上；AI 医生一致性 91% 等几项对不上，单列为未核实。
- 肖京补了 2025 年来源，置信度提到中；何明科补了 2026-04 在任来源。

CSV：中国平安 Ping An|金融机构 AI 团队|国内|王晓航|中国平安集团首席技术官（CTO）兼平安科技总经理|https://www.yicai.com/news/102747417.html ; https://www.nbd.com.cn/articles/2026-04-22/4352737.html ; https://www.nbd.com.cn/articles/2026-09-22/4588645.html ; https://static.weeklyonstock.com/25/1121/qdy202324.html|医疗评测（境内医生写的病例评分标准、医学事实核验集）和保险、银行办事智能体的多步任务评测|中

## 阿里巴巴 通义千问 Qwen

**状态**：核实，未改邮件

- 郑楚杰主页原文仍写 "Leading the OPD team for post-training consolidation"（https://github.com/chujiezheng/chujiezheng.github.io/blob/master/_pages/about.md ）。
- 周浩接任后训练负责人：补了原始链接，21 世纪经济报道 https://www.21jingji.com/article/20260305/herald/8626d9d7e4b5878d19802e71980542a4.html 、新浪 https://finance.sina.com.cn/jjxw/2026-03-05/doc-inhpwzrs3350491.shtml 、36氪 https://36kr.com/p/3708425301749891 。
- 开头一句（Qwen3.8 把 professional work 和 long-horizon agentic tasks 列为主要提升方向）：重新读了 README 原文（https://github.com/QwenLM/Qwen3.8 ），保留不改。补了 2026-09 蒸馏通报。

CSV：阿里巴巴 通义千问 Qwen|国内大模型公司|国内|郑楚杰（Chujie Zheng）|Qwen 团队 member of technical staff，带 OPD 团队做后训练整合，牵头大规模 RL|https://chujiezheng.github.io/ ; https://github.com/chujiezheng/chujiezheng.github.io/blob/master/_pages/about.md ; https://arxiv.org/abs/2507.18071|专业工作和长程 agent 任务的 RL 环境与专家数据（Xitadel、财务结账、法律），以及带理由的专家评审和评分标准|高

## 阶跃星辰 StepFun

**状态**：核实，未改邮件

- 焦斌星：2026-02 Step 3.5 Flash 论文作者名单里有他；搜索摘要（LinkedIn，仅旁证）称他是联合创始人兼 VP。2026 年的具体分工仍没有公开说法，置信度维持中。
- 开头一句：Step 5 Preview 主打金融和专业知识工作，腾讯新闻（https://news.qq.com/rain/a/20260920A06SE900 ）、21 世纪经济报道（https://www.21jingji.com/article/20260921/herald/742325e7deb08d056e5801bcae9c9974.html ）、新浪一致；Step 3.5 Flash 要把 RL 用到专业工作的专家级任务上，README 原文第 476 行一致。保留不改。
- 补充：金融方向有三套自研 FinStepBench 评测；补了 2026-09 蒸馏通报。

CSV：阶跃星辰 StepFun|国内大模型公司|国内|焦斌星（Binxing Jiao）|联合创始人，数据负责人（2024 年说法）|https://www.qbitai.com/2024/04/132306.html ; https://www.cls.cn/detail/1627876 ; https://arxiv.org/abs/2602.10604|金融专家数据和环境：Step 5 Preview 主打金融分析，内部在招金融 SFT/GRPO 岗，Xitadel、财务结账环境加 CFA、会计背景专家写的评分标准最匹配|中

## 腾讯混元 Tencent Hunyuan

**状态**：已修改（替换 GitHub 转录来源，把一条未核实的职务降级；邮件未改）

- 姚顺雨：首席 AI 科学家兼大语言模型部、AI Infra 部负责人（2025-12-17），改用原始链接：36氪 https://36kr.com/p/3599552216957189 、澎湃 https://www.thepaper.cn/newsDetail_forward_32195162 、量子位 https://www.qbitai.com/2025/12/361841.html 。2026-07-23 成立基础模型部、由他负责：财新 https://companies.caixin.com/2026-07-24/102467665.html 、21 世纪经济报道、观察者网。
- "2026-09-24 兼任 AI Data 部负责人"：两次中文搜索都只查到 2025-12 的安排（刘煜宏负责 AI Data 部），原始的晚点报道没有找到。已在收件人一行和来源里改成"二手转述，未核实"。
- AI Lab 撤销（2026-03-20）改用第一财经 https://www.yicai.com/news/103097489.html 和新浪原文。36氪 2026-08-14 那条原文打不开，GitHub RSS 副本标注保留。
- 开头一句（Hy4 preview 训练数据和内部软件工程师、金融分析师、安全专家等共建）：IT之家（https://www.ithome.com/0/995/570.htm ）、新浪、腾讯新闻和官网的搜索摘要一致，README 原文此前已读，保留不改。

CSV：腾讯混元 Tencent Hunyuan|国内大模型公司|国内|姚顺雨（Shunyu Yao）|腾讯首席 AI 科学家，兼基础模型部（2026-07 由大语言模型部和多模态模型部合并）和 AI Infra 部负责人|https://36kr.com/p/3599552216957189 ; https://www.qbitai.com/2025/12/361841.html ; https://companies.caixin.com/2026-07-24/102467665.html ; https://github.com/Tencent-Hunyuan/Hy4-preview|金融建模、金融分析方向的外部专家数据和 Agent 轨迹评分标准与质检，可对接 AI Data 部的数据交付团队|中

## 九坤投资 Ubiquant（IQuest Research）

**状态**：核实，未改邮件（中文名未找到）

- Bryan Dai 的中文名：用中英文搜了"九坤 / IQuest / 至知创新研究院 + Bryan Dai"和研究院负责人，公开报道里没有出现，称呼保持"Bryan Dai"。
- 至知创新研究院的来源换成原始报道：中证报 https://jnzstatic.cs.com.cn/zzb/htmlInfo/112783.html （"九坤投资创始团队发起设立的、独立于量化投研体系的全新平台"）、证券时报 https://www.stcn.com/article/detail/3568306.html 。
- 开头一句（ModularRSI 把 Terminal-Bench 2.0 从 47.57% 提到 52.43%）：重新读了 README 原文（https://github.com/IQuestLab/ModularRSI ），保留不改。

CSV：九坤投资 Ubiquant（AI 研究团队 IQuest Research）|金融机构 AI 团队|国内|Bryan Dai|九坤 AI 研究团队（IQuest Research / 至知创新研究院）的资深研究负责人，具体头衔未找到|https://github.com/UbiquantAI/URM ; https://github.com/UbiquantAI/one-shot-em ; https://github.com/IQuestLab/ModularRSI|交易和预测环境作为代码以外的长程可验证环境（也可只作留出评测），加金融、医疗专家校准的 judge 和验证器|中

## 数据堂 Datatang

**状态**：新增（drafts/datatang.md）

- 联系人：齐红威是董事长兼总经理（2011-08 起），出自 2024 年报和 2025 半年报（搜索摘要）；早期线索"只在 2020 年博客里被称为 CEO"已更正。专家供给或合作负责人没有找到。
- 上市：2024-01 北交所辅导备案；2026-06-29 发布辅导验收完成的提示性公告（https://xinsanban.eastmoney.com/Article/NoticeContent?id=AN202606291826532946 ），尚未看到正式申报；仍在新三板（831428）。
- 具身工厂：8000 平方米、300 套灵巧手设备，官网新闻（https://datatang.com/news/1223 ）、腾讯新闻 2026-09-20（https://news.qq.com/rain/a/20260920A0820100 ）、36氪（https://eu.36kr.com/zh/p/3810340908817928 ，称 2025-09 建于保定）一致。"600 名采集员、今年目标 10 万小时"没有核实到，没有采用（官网写的是已积累 10 万小时 Ego-Centric 数据，不是年度目标）。
- 灵心巧手战略合作 2026-01-21 确认（https://36kr.com/newsflashes/3648901596487555 ）。
- 大模型专家数据：早期线索说"看不到"，核实下来不成立。官网有"垂域大模型数据服务"，从专家库遴选数学、医疗、法律方向的人员（https://www.datatang.com/llm 、https://www.datatang.net/news/1181 ）。但这些都是公司自己的表述，所以开头一句改用有独立来源的具身工厂。匹配度偏弱写进了风险。

CSV：数据堂 Datatang|人类数据供应商|国内|齐红威|创始人、董事长兼总经理|http://notice.10jqka.com.cn/api/pdf/82f365a65766e516_1745837250/%E6%95%B0%E6%8D%AE%E5%A0%82:2024%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf ; https://qxb-pdf-osscache.qixin.com/AnBaseinfo/71c1f298ee9ef193c13d42aeb750add7.pdf ; https://news.qq.com/rain/a/20250305A033J200|专家供给合作：他们在数学、医疗、法律有自有专业团队，金融、会计等执业资历专家可以由我们按项目补充供给；重心在具身数据，匹配度一般|中

## 幂律智能 PowerLaw

**状态**：新增（drafts/powerlaw.md）

- 仍在运营：2025-09-08 发布 AI 律师智能体"吾律"（极客公园 https://www.geekpark.net/news/353582 、新浪 https://finance.sina.com.cn/tech/roll/2025-09-08/doc-infptzmr4723331.shtml 、腾讯新闻）；虎嗅 2026-04-22 有长篇报道（https://www.huxiu.com/article/4850995.html ）。2023-12 以后没有新融资消息。
- 联系人：张惟师，联合创始人兼 CTO（虎嗅 2026-04、2025-09 发布稿、新浪 2022-08）。涂存超是联合创始人兼 CEO，有多个来源（36氪、投资界、IT桔子），不止早期线索说的一份第三方文件，但都是 2023 年的，作为备选。另有副总裁李融（2025 年主持"法律数据评测与大模型"圆桌）。
- 早期线索核实：PowerLawGLM（2023，和智谱合作）、蓝驰领投近 8000 万元 Pre-B（2023-12）、MeCheck / MeFlow 都确认；"吾律"确实是幂律的产品，发布报道的标题就写着幂律智能。
- 开头一句用吾律能交付盖章版律师函、起诉状和证据目录，多家报道一致；事实距今一年，已在风险里注明。

CSV：幂律智能 PowerLaw|垂直 AI（法律）|国内|张惟师|联合创始人兼 CTO|https://www.huxiu.com/article/4850995.html ; https://blog.csdn.net/csdnnews/article/details/151328513 ; https://finance.sina.com.cn/tech/roll/2022-08-18/doc-imizmscv6747731.shtml|吾律交付律师函、起诉状等法律文书，需要执业律师写的验收标准、留出评测集和工具调用类的多步任务轨迹|中
