# 买方反向索引

由 tools/intel_merge.py 从 4 个分段、804 条公开声明生成。「供应商数」只算点名的供应商；置信度取该客户所有声明里最高的一条。

## 全部买方（按点名的现有供应商数排序）

| 客户 | 类型 | 现有供应商数 | 点名的供应商 | 采购内容 | 最高置信度 | 在我们名单上 |
|---|---|---|---|---|---|---|
| Google DeepMind | frontier lab、其他、科技大厂 | 27 | Prolific、TELUS Digital、Gray Swan AI、LMArena、Scale AI（变动）、GlobalLogic、Spirit Airlines、光轮智能 Lightwheel、Surge AI、Mercor、Turing、Centific、Deccan AI、Mechanize、Bespoke Labs、Adaptive ML、Epoch AI、METR、Irregular、Apollo Research、Snorkel AI、Appen（变动）、Labelbox、Sama、Welocalize、General Reasoning、Vals AI、Haize Labs、BenchFlow | 2024 年对 Google 的收入增长抵消了部分科技客户的下滑；2025 Q1 来自 Google 等科技与电商客户的收入下降；2026 H1 总收入 6.14 亿美元，约 91% 来自基础模型公司；AI 红队/评测；Bard 训练指导手册/标注；Bard/搜索质量评分合同终止（约8280万美元）；Deliberat | 高 | 是 |
| Anthropic | frontier lab、其他、高校研究机构 | 24 | Andon Labs、METR、Gray Swan AI、Apollo Research、Toloka、Mechanize、Deloitte、Signature Science、SecureBio、Mercor、Surge AI、Turing、Handshake AI、Centific、AfterQuery、Bespoke Labs、Irregular、Haize Labs、Snorkel AI、Upwork、Pareto.AI、Halluminate、HUD、Vals AI | 2026 H1 总收入 6.14 亿美元，约 91% 来自基础模型公司；AI 红队/安全评测；CBRN 评测：长程病毒学任务共建；Claude Opus 4.6 系统卡外部对齐测试；Claude Opus 4.6 系统卡外部测试：Vending-Bench 2；Claude Opus 4.6 系统卡：CyScenari | 高 | 是 |
| OpenAI | frontier lab、其他、科技大厂 | 24 | Epoch AI、METR、Gray Swan AI、LMArena、Apollo Research、Scale AI（变动）、Mercor、Handshake AI、Haize Labs、Faculty、Virtue AI、Irregular、SecureBio、Surge AI、Turing、Centific、AfterQuery、Bespoke Labs、Patronus AI、Snorkel AI、Invisible Technologies、Sama、Halluminate、HUD、Vals AI | 2021 年起成为客户；2022 年起为 OpenAI 微调模型；2026 H1 总收入 6.14 亿美元，约 91% 来自基础模型公司；AI 红队/安全评测；Autonomy-10 基准（Operator 发布评测）；ChatGPT 训练承包商（审阅真实用户提示）；Codex Creator Challenge 学生 | 高 | 是 |
| 阿里巴巴 | 其他、国内大模型公司、科技大厂 | 15 | 海天瑞声 SpeechOcean/DataOcean AI、AfterQuery、Mercor、光轮智能 Lightwheel、UniPat AI、博登智能 Boden AI、阿里巴巴、标贝科技 DataBaker、晴数智慧 Magic Data、龙猫数据、曼孚科技 MindFlow、司南 OpenCompass、希尔贝壳 AISHELL、Prime Intellect、General Reasoning | AI训练数据（语音/视觉/NLP）；CV/语音/NLP数据标注（SEED平台）；Lab 平台上可 RL 微调的开源模型；OpenReward 平台环境贡献者（自列）；仿真资产/合成数据/评测；具身仿真资产与合成数据；内部自建专家/众包平台，为本公司模型供数：自建专家社区：影视、法律、金融、通用指令专家；最高时薪约100 | 高 | 是 |
| Meta | frontier lab、其他、科技大厂 | 14 | Surge AI、CrowdStrike、TaskUs、Irregular、Gray Swan AI、Scale AI（变动）、Mercor、Turing、Labelbox、METR、LMArena、司南 OpenCompass、Innodata、General Reasoning、Vals AI | AI 红队/安全评测；AdvancedIF 指令遵循基准，prompt 与评分细则全部由专家编写；AdvancedIF 指令遵循基准；人写 rubric 做 RL 奖励；CyberSOCEval 网络安全评测基准；Forbes 报道列出的客户；Gray Swan Arena 红队竞技场赞助；LiteLLM 供应链攻击导 | 高 | 是 |
| NVIDIA | frontier lab、其他、科技大厂 | 12 | Scale AI、Translated、光轮智能 Lightwheel、General Reasoning、Applied Compute、Mercor、Turing、Centific、AfterQuery、Patronus AI、晴数智慧 Magic Data、Prime Intellect | HelpSteer2/HelpSteer3 偏好数据的标注员通过 Scale AI 签约；HelpSteer3 偏好数据：通用/STEM/代码子集标注；HelpSteer3 多语言子集标注；Isaac Lab-Arena 评测/任务层共建；GR00T 模型部署；合成数据；Lab 平台上可 RL 微调的开源模型；Nemo | 高 |  |
| 字节跳动 | 国内大模型公司、科技大厂 | 11 | 海天瑞声 SpeechOcean/DataOcean AI、Turing、光轮智能 Lightwheel、Abaka AI、恺望数据、UniPat AI、热热数据、字节跳动、标贝科技 DataBaker、龙猫数据、曼孚科技 MindFlow | AI大模型数据；AI训练数据（语音/视觉/NLP）；REER逆向工程推理（开放式生成）论文，2077AI为署名机构；SuperGPQA 285 学科研究生级基准，2077AI 构建、Abaka 为核心贡献者；SuperGPQA 285学科研究生级评测集；具身仿真资产与合成数据；内部自建专家/众包平台，为本公司模型供数： | 高 | 是 |
| Amazon | 其他、科技大厂 | 10 | 海天瑞声 SpeechOcean/DataOcean AI、Collinear AI、Gray Swan AI、Toloka、Turing、Invisible Technologies、micro1、Centific、Patronus AI、METR | 2019年前五大客户；AI训练数据（语音/视觉/NLP）；AWS Marketplace 上架/AWS Startups 合作；Gray Swan Arena 红队竞技场赞助；RL 仿真环境/训练数据；专家数据 / LLM 与代理训练数据；为这些公司生成专家级数据集；公司自述客户；前沿风险评估试点；客户包括前沿实验室、 | 高 |  |
| Microsoft | frontier lab、其他、科技大厂 | 10 | Surge AI、海天瑞声 SpeechOcean/DataOcean AI、Toloka、Turing、Invisible Technologies、micro1、Centific、Scale AI（变动）、标贝科技 DataBaker、晴数智慧 Magic Data、Handshake AI（变动）、Sama | AI训练数据（语音/视觉/NLP）；CEO 在融资报道中点名；Forbes 报道列出的客户；MAI-Thinking-1 盲测人类评测（1276个任务，专业评分员）；Meta-Scale 交易后转向 Handshake 等供应商；RLHF 合同；专家数据 / LLM 与代理训练数据；为这些公司生成专家级数据集；公司自述 | 高 |  |
| 腾讯 | 国内大模型公司、科技大厂 | 10 | 海天瑞声 SpeechOcean/DataOcean AI、Surge AI、Mercor、标贝科技 DataBaker、晴数智慧 Magic Data、龙猫数据、倍赛 BasicFinder、司南 OpenCompass、希尔贝壳 AISHELL、腾讯 | AI训练数据（语音/视觉/NLP）；AI训练数据，含大模型相关数据服务；人类偏好/训练数据；内部自建专家/众包平台，为本公司模型供数：自建 AI 专家社区汇聚垂直领域人才；同时为腾讯提供数据；大模型数据采集/标注；对话式AI/语音/多轮对话数据集；对话式AI/语音数据；数据采集标注；训练数据；语音合成/识别数据及TTS | 高 | 是 |
| 百度 | 科技大厂 | 8 | 海天瑞声 SpeechOcean/DataOcean AI、数据堂 Datatang、恺望数据、标贝科技 DataBaker、晴数智慧 Magic Data、曼孚科技 MindFlow、星尘数据 Stardust、希尔贝壳 AISHELL | 2022年前五大客户（自动驾驶/语音等训练数据）；AI大模型数据；AI训练数据（语音/视觉/NLP）；对话式AI/语音/多轮对话数据集；对话式AI/语音数据；数据标注；自动驾驶/安防/人脸等数据标注；语音合成/识别数据及TTS定制；语音数据采标 | 高 |  |
| xAI | frontier lab、其他 | 7 | LMArena、Scale AI、micro1、Centific、METR、Andon Labs、Handshake AI（变动）、Vals AI | Grok 4 发布会展示 Vending-Bench 结果；Meta-Scale 交易后转向 Handshake 等供应商；xAI 办公室 Grokbox AI 售货机；人类数据/标注；付费 AI Evaluations 服务；客户包括前沿实验室、Microsoft、Amazon 和机器人公司 1X；对话质量提示词数据 | 高 | 是 |
| 京东 | 科技大厂 | 5 | 京东众智、标贝科技 DataBaker、星尘数据 Stardust、倍赛 BasicFinder、希尔贝壳 AISHELL | 数据标注；数据采集标注；电商商品内容生成、智能仓储等“标-训-推”一体化；语音合成/识别数据及TTS定制；语音数据采标 | 高 |  |
| 智谱 | 其他、国内大模型公司 | 4 | Surge AI、海天瑞声 SpeechOcean/DataOcean AI、龙猫数据、Prime Intellect | Lab 平台上可 RL 微调的开源模型；RL 环境（助力 GLM-4.6）；大模型数据处理技术、大模型数据集供给、大模型评测；大模型数据采集/标注 | 中 | 是 |
| Hugging Face | AI 应用公司、其他 | 3 | Snorkel AI、Bespoke Labs、Prime Intellect | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；Lab 平台上可 RL 微调的开源模型；联合举办推理数据集竞赛（Curator） | 高 |  |
| Mistral AI | frontier lab、其他 | 3 | Surge AI、Centific、Invisible Technologies | Forbes 报道列出的客户；多年期 RLHF 合同；融资报道列出的客户 | 中 | 是 |
| Nebius | 其他、科技大厂 | 3 | Toloka、General Reasoning、Prime Intellect | INTELLECT-3 推理服务；OpenReward 上架 SWE-rebench-v2；Tendem 人类专家按需接入智能体（MCP） | 高 |  |
| Prime Intellect | AI 应用公司、其他 | 3 | Snorkel AI、Proximal、BenchFlow | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；FrontierSWE 以 Prime Intellect Environment 形式上架；框架支持运行 Prime Intellect/Verifiers 托管环境 | 高 |  |
| Together AI | AI 应用公司、其他 | 3 | Snorkel AI、Bespoke Labs、Collinear AI | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；TraitBasis 模拟用户集成进 Together Evals；联合举办推理数据集竞赛（Curator） | 高 |  |
| 月之暗面 | 国内大模型公司 | 3 | 海天瑞声 SpeechOcean/DataOcean AI（变动）、Surge AI、龙猫数据、UniPat AI | RL 环境（助力 Kimi K2 Thinking）；RL 训练环境；否认合作；大模型数据采集/标注；模型发布采用其 BabyVision 基准（基准被采用，非付费客户关系）：BabyVision 被纳入 Kimi K2.5 评测（媒体称；GitHub README 未见，待核） | 高 | 是 |
| 科大讯飞 | 国内大模型公司、科技大厂 | 3 | 海天瑞声 SpeechOcean/DataOcean AI、曼孚科技 MindFlow、倍赛 BasicFinder | AI训练数据（语音/视觉/NLP）；数据采集标注；自动驾驶/安防/人脸等数据标注 | 高 |  |
| AI21 Labs | AI 应用公司、frontier lab | 2 | Haize Labs、Invisible Technologies | SFT/RLHF 专家劳动力与流程平台；多百万美元红队合同；自动化红队/越狱测试 | 中 |  |
| Apple | 科技大厂 | 2 | TransPerfect、Huzzle Labs | Apple Intelligence 回答标注（巴塞罗那约200人）；RL 环境/专家轨迹/评测（官网自称，未经第三方核实） | 中 |  |
| Artificial Analysis | 其他 | 2 | Mercor、Datacurve | APEX-Agents-AA 独立排行榜；DeepSWE 基准被纳入 Coding Agent Index | 中 |  |
| Cognition | AI 应用公司 | 2 | Mercor、Applied Compute | APEX-SWE 软件工程基准；定制 RL 后训练模型 / 企业代理 | 中 |  |
| Cohere | AI 应用公司、frontier lab | 2 | Appen、Invisible Technologies | Command R 幻觉减少、10 种语言扩展、稀有编程语言；Command 模型微调专家标注 | 中 |  |
| Cua | AI 应用公司 | 2 | HUD、Snorkel AI | 基于 Cua-Bench 构建 CUA-Bench+ 计算机使用数据；电脑使用 agent 评测集成（OSWorld 等） | 中 |  |
| DoorDash | 企业 | 2 | Applied Compute、HUD | RL 环境/评测平台；定制 RL 后训练模型 / 企业代理 | 中 |  |
| GM | 其他 | 2 | Scale AI、Sama | 融资稿列出的客户；财富 50 强中 25% 为客户 | 低 |  |
| Harvey | 垂直 AI | 2 | Mercor、Vals AI | Harvey Tenet 法律模型：人类专家数据集+合成数据审校；法律 AI 基准（VLAIR）参评；评测平台使用 | 高 | 是 |
| IBM | 企业、科技大厂 | 2 | DataForce、SuperAnnotate | B 轮报道列出的客户；Granite Guardian 风险检测人工标注 | 中 |  |
| Laude Institute | 高校研究机构 | 2 | Snorkel AI、Bespoke Labs | Frontier-Bench（原 Terminal-Bench 3.0）/Terminal-Bench Science；Terminal-Bench（Stanford+Laude 主导的开放学术合作；Bespoke 提供 API 额度） | 中 |  |
| Toyota Research Institute | 企业、其他 | 2 | Bespoke Labs、Scale AI | OpenThoughts 项目共同赞助/合作；融资稿列出的客户 | 高 |  |
| 三星 | 企业、科技大厂 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、龙猫数据 | AI训练数据（语音/视觉/NLP）；终端/互联网数据采集标注；语音数据；2020年销售额大幅下滑 | 高 |  |
| 中国科学院 | 科技大厂、高校研究机构 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、倍赛 BasicFinder | AI训练数据（语音/视觉/NLP）；数据采集标注 | 高 |  |
| 博世 | 企业 | 2 | 光轮智能 Lightwheel、龙猫数据 | 仿真资产/合成数据/评测；自动驾驶数据标注 | 中 |  |
| 商汤 | AI应用公司、科技大厂 | 2 | 恺望数据、倍赛 BasicFinder | AI大模型数据；数据采集标注 | 中 |  |
| 旷视 | 垂直AI、科技大厂 | 2 | 恺望数据、曼孚科技 MindFlow | 自动驾驶/安防/人脸等数据标注；自动驾驶数据 | 中 |  |
| 清华大学 | 高校研究机构 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、百度智能云数据众包 | AI训练数据（语音/视觉/NLP）；十亿像素级视频数据集PANDA | 高 |  |
| 美国联邦政府 | 政府 | 2 | Snorkel AI、Mercor | 专家数据/环境服务（未具名机构）；获得联邦合同 | 中 |  |
| 美国陆军 | 其他、政府 | 2 | Surge AI、Scale AI | 政府客户；融资稿列出的客户 | 中 |  |
| AT&T | 企业 | 1 | Adaptive ML | RLOps 平台微调专用模型，嵌入 FDE（反欺诈、客服、text-to-SQL 等 50+ 用例） | 高 |  |
| AXA Financial | 企业 | 1 | Encord | 物理 AI 与多模态数据 | 高 |  |
| Adobe | 企业 | 1 | Labelbox | 标注平台生产用户 | 低 |  |
| Allen AI | 其他 | 1 | Prime Intellect | Lab 平台上可 RL 微调的开源模型 | 低 |  |
| American Family Insurance | 其他 | 1 | Invisible Technologies | 公司自述客户 | 中 |  |
| Applied Compute | AI 应用公司 | 1 | Mercor | 公司法任务专家数据后训练（约2000例） | 中 |  |
| Arcee | 其他 | 1 | Prime Intellect | Lab 平台上可 RL 微调的开源模型 | 低 |  |
| Arcee AI | AI 应用公司 | 1 | Prime Intellect | INTELLECT-1 去中心化训练协作 | 中 |  |
| Aurora | 企业 | 1 | Uber AI Solutions | 50 多家企业客户中点名的两家 | 中 |  |
| BOUNTY COUNTRY PTY LTD | 其他 | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） | 中 |  |
| CAISI (NIST) | 政府 | 1 | Gray Swan AI | 加入 UK AISI 智能体红队挑战赛 | 高 |  |
| Canva | 企业 | 1 | SuperAnnotate | B 轮报道列出的客户 | 低 |  |
| Center for AI Safety | 其他 | 1 | Scale AI | Humanity's Last Exam | 高 |  |
| Center for AI Safety（CAIS） | 高校研究机构 | 1 | Scale AI | Humanity's Last Exam 专家难题基准 | 高 |  |
| Character AI | 其他 | 1 | Pareto.AI | 专家整理的数据集与评测 | 低 |  |
| Charlotte Hornets | 其他 | 1 | Invisible Technologies | 公司自述客户 | 中 |  |
| Circadence | 企业 | 1 | Scale AI | 政府与企业网络安全智能体 | 高 |  |
| DIU | 其他 | 1 | Scale AI | 融资稿列出的客户 | 低 |  |
| DataComp 社区 | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 开源推理数据集 | 高 |  |
| Databricks | 企业 | 1 | SuperAnnotate | B 轮报道列出的客户 | 低 |  |
| Databricks（Mosaic AI） | 科技大厂 | 1 | SuperAnnotate | DBRX 微调数据与 RAG 评测；获 2025 Databricks ISV 客户影响力合作伙伴奖 | 高 |  |
| Dell | 其他 | 1 | Centific | 融资报道列出的客户 | 中 |  |
| Deloitte | 企业 | 1 | Haize Labs | AI 红队/评测 | 低 |  |
| Eigent | AI 应用公司 | 1 | General Reasoning | OpenReward 上架 SETA 环境 | 高 |  |
| Emergence AI | AI 应用公司 | 1 | Patronus AI | Percival 智能体调试/优化 | 低 |  |
| Etsy | 企业 | 1 | Patronus AI | 多模态 LLM-as-a-Judge 图片描述幻觉检测 | 中 |  |
| Exa | AI 应用公司 | 1 | Vals AI | 评测平台使用 | 低 |  |
| Factory | AI 应用公司 | 1 | Snorkel AI | $3M Open Benchmarks Grants 共同支持方 | 高 |  |
| Figure AI | 垂直 AI、垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测；具身仿真/合成数据 | 中 |  |
| Financial Times | 企业 | 1 | Huzzle Labs | RL 环境/专家轨迹/评测（官网自称，未经第三方核实） | 低 |  |
| Fireworks AI | AI 应用公司 | 1 | Vals AI | 评测平台使用 | 低 |  |
| Fisher Phillips | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） | 中 |  |
| Flapping Airplanes | 其他 | 1 | Prime Intellect | 托管后训练/RL 平台（新兴研究实验室 neolab） | 中 |  |
| Ford | 其他 | 1 | Sama | 财富 50 强中 25% 为客户 | 低 |  |
| Gamma | AI 应用公司 | 1 | Patronus AI | 自动化评测（Patronus Judges） | 中 |  |
| Genentech | 企业 | 1 | Labelbox | 标注平台生产用户 | 低 |  |
| H Company | AI 应用公司 | 1 | Cua | 协助审计 computer-use 能力矩阵 | 低 |  |
| HP | 科技大厂 | 1 | Patronus AI | LLM 自动评测/幻觉检测 | 中 |  |
| HackerOne | 企业 | 1 | Haize Labs | AI 红队/评测 | 低 |  |
| Harvard Law School | 高校研究机构 | 1 | Mercor | APEX 基准由 Mercor 与外部专家（Sunstein、Topol）合著 | 高 |  |
| Juelich Supercomputing Center (JSC) | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究/算力 | 高 |  |
| KCL | 其他 | 1 | Prolific | 研究与企业客户 | 低 |  |
| Khasm Labs | 其他 | 1 | Collinear AI | 加入 Khasm Labs 第 11 期加速器（对接电信/科技大厂） | 低 |  |
| Kore.ai | AI 应用公司 | 1 | Collinear AI | 客服智能体数据包、9 语种安全与质量 | 高 |  |
| LAION | 其他 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 | 高 |  |
| Lazard | 金融机构 | 1 | Huzzle Labs | RL 环境/专家轨迹/评测（官网自称，未经第三方核实） | 低 |  |
| Legaltech Hub | 其他 | 1 | Vals AI | 法律 AI 基准研究合作方 | 中 |  |
| Legora | 垂直 AI | 1 | AfterQuery | 法律领域专家数据 | 中 |  |
| Lenovo | 其他 | 1 | Centific | 融资报道列出的客户 | 中 |  |
| M-A-P | 科技大厂、高校研究机构 | 1 | Abaka AI | KINA知识评测基准；SuperGPQA 285学科研究生级评测集 | 中 |  |
| MATS | 其他、高校研究机构 | 1 | Pareto.AI | 专家整理的数据集与评测；标注员参与 AI 安全研究（辩论评测） | 低 |  |
| METR | 其他 | 1 | Pareto.AI | 专家整理的数据集与评测 | 低 |  |
| MMAR音频推理基准合作方 | 高校研究机构 | 1 | Abaka AI | 语音/音频/音乐深度推理评测 | 低 |  |
| Manulife | 金融机构 | 1 | Adaptive ML | 多年期协议，RLOps 层（核保报价、销售顾问等）；多年期协议，模型微调 | 高 |  |
| McDermott Will & Emery | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） | 中 |  |
| Mercor | 其他 | 1 | Scale AI（变动）、Deeptune（变动）、Sepal AI（变动）、Applied Compute、Spirit Airlines（变动） | 定制 RL 后训练模型 / 企业代理；用 Mercor 专家数据后训练法律/投行模型，APEX-Agents 公司法第一；竞购企业工作流数据（出价750万美元，次高）；被 Mercor 收购（接手其与前沿实验室研究员的关系）；被 Mercor 收购，团队并入纽约办公室；被 Mercor 收购，长程研究/RL 环境；被收 | 高 | 是 |
| MongoDB | 科技大厂 | 1 | Haize Labs | AI 红队/评测 | 低 |  |
| Morgan Stanley | 其他 | 1 | Scale AI | 融资稿列出的客户 | 低 |  |
| Motif Technologies（韩国） | 其他 | 1 | AfterQuery | 韩国大模型实验室训练数据 | 中 |  |
| Motorola Solutions | 企业 | 1 | SuperAnnotate | B 轮报道列出的客户 | 低 |  |
| NASA | 其他 | 1 | Sama | 官网列出的企业客户 | 低 |  |
| Niantic | 企业 | 1 | Uber AI Solutions | 50 多家企业客户中点名的两家 | 中 |  |
| Nous Research | AI 应用公司 | 1 | hillclimb | Nomos 1 模型卡注明与 Hillclimb AI 合作训练；Putnam 数学模型；媒体报道；联合训练数学模型 Nomos 1（Putnam 87/120） | 高 |  |
| Nova AI | AI 应用公司 | 1 | Patronus AI | Percival 智能体调试/优化 | 低 |  |
| ODML）/ Walmart | 其他 | 1 | Sama | 官网列出的企业客户 | 低 |  |
| Ogletree Deakins | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） | 中 |  |
| Oxford | 其他 | 1 | Prolific | 研究与企业客户 | 低 |  |
| P&G | 企业 | 1 | Labelbox | 标注平台生产用户 | 低 |  |
| Palantir | 企业 | 1 | Innodata | 为 Palantir 项目做标注、多模态数据工程和生成式 AI 工作流支持 | 高 |  |
| Parasail | 其他 | 1 | Prime Intellect | INTELLECT-3 推理服务 | 低 |  |
| Pearson | 企业 | 1 | Patronus AI | LLM 自动评测/幻觉检测 | 中 |  |
| Perplexity | AI 应用公司 | 1 | Invisible Technologies | 多年期 RLHF 合同 | 低 |  |
| Phantom AI | 垂直 AI | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） | 中 |  |
| PublicAI | AI 应用公司 | 1 | Abaka AI | 1024 万美元战略合作，为 KOR-Bench/SuperGPQA 征集难题 | 中 |  |
| PyTorch | 其他 | 1 | Snorkel AI | 300 万美元 Open Benchmarks Grants，资助开源智能体基准 | 高 |  |
| PyTorch Foundation | 其他 | 1 | Snorkel AI | $3M Open Benchmarks Grants 共同支持方 | 高 |  |
| Qualcomm | 企业 | 1 | SuperAnnotate | B 轮报道列出的客户 | 低 |  |
| Ramp | 企业 | 1 | Prime Intellect | 托管后训练/RL 平台 | 中 |  |
| Recraft | AI 应用公司 | 1 | Toloka | 专家数据 / LLM 与代理训练数据 | 高 |  |
| Reed Smith | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） | 中 |  |
| SK Telecom | 企业 | 1 | Adaptive ML | 多语种内容审核，微调 Gemma 3 | 高 |  |
| Sarvam AI | AI 应用公司 | 1 | General Reasoning | OpenReward 平台环境贡献者（自列） | 低 |  |
| Scale AI | 其他 | 1 | Mercor（变动）、Haize Labs | 多百万美元红队合同；被 Scale 起诉：前员工带走 100 多份客户策略文件，并向 Scale 大客户推销 Mercor | 中 | 是 |
| Scripps Research | 高校研究机构 | 1 | Mercor | APEX 基准由 Mercor 与外部专家（Sunstein、Topol）合著 | 高 |  |
| Search | 其他 | 1 | Sama | 官网列出的企业客户 | 低 |  |
| Sequrity.ai | AI 应用公司 | 1 | Gray Swan AI | Safeguards 挑战赛奖金赞助 | 高 |  |
| Sharpe | 其他 | 1 | HUD | RL 环境/评测平台 | 低 |  |
| Shopify | 企业、其他 | 1 | Toloka | 专家数据 / LLM 与代理训练数据；融资报道列出的客户，业务为安全评测、红队、专家数据 | 高 |  |
| Skydio | 企业 | 1 | Encord | 物理 AI 与多模态数据 | 高 |  |
| Skyvern | AI 应用公司 | 1 | Halluminate | Web Bench 浏览器 agent 基准 | 高 |  |
| Snorkel AI | 其他 | 1 | Cua | 在 Cua-Bench 框架上共建 KiCad 计算机使用基准（CUA-Bench+） | 中 |  |
| Snowflake | 其他 | 1 | Deccan AI | 后训练数据、评测、RL | 中 |  |
| Stanford | 其他 | 1 | Prolific | 研究与企业客户 | 低 |  |
| Stanford University | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究；Terminal-Bench（Stanford+Laude 主导的开放学术合作；Bespoke 提供 API 额度） | 高 |  |
| Synthesia | 企业 | 1 | Encord | 物理 AI 与多模态数据 | 高 |  |
| Tailscale | 科技大厂 | 1 | Apollo Research | Watcher 智能体监控接入 Tailscale Aperture 网关 | 高 |  |
| Thinking Machines Lab | frontier lab | 1 | General Reasoning | OpenReward 与 Tinker 训练 API 兼容集成 | 中 | 是 |
| Thomson Reuters | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 | 中 |  |
| UC Berkeley | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 | 高 |  |
| UCL | 高校研究机构 | 1 | Pareto.AI | 标注员参与 AI 安全研究（辩论评测） | 低 |  |
| UK AISI | 政府 | 1 | Gray Swan AI | Gray Swan Arena 红队竞技场赞助；智能体红队挑战赛联合举办 | 高 |  |
| US AISI | 政府 | 1 | Gray Swan AI | 加入 UK AISI 智能体红队挑战赛 | 高 |  |
| US CAISI (NIST) | 政府 | 1 | Gray Swan AI | CAISI 发布大规模红队竞赛智能体安全研究 | 高 |  |
| UiPath | 企业 | 1 | HUD | RL 环境/评测平台 | 低 |  |
| University of Oxford (OATML) | 高校研究机构 | 1 | Gray Swan AI | Safeguards 挑战赛联合赞助 | 高 |  |
| University of Washington | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 | 高 |  |
| Upstage | 其他 | 1 | Flitto | Solar Open 2 大规模训练数据构建；韩国主权AI项目联合体中负责数据集构建 | 高 |  |
| Vecflow | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 | 中 |  |
| Vercel | 科技大厂 | 1 | Vals AI | 评测平台使用 | 低 |  |
| Walmart | 企业 | 1 | Labelbox | 标注平台生产用户 | 低 |  |
| Weaviate | AI 应用公司 | 1 | Patronus AI | Percival 智能体调试/优化 | 低 |  |
| Woven by Toyota | 企业 | 1 | Encord | 物理 AI 与多模态数据 | 高 |  |
| Zapier | AI 应用公司 | 1 | Prime Intellect | 托管后训练/RL 平台 | 中 |  |
| Zipline | 企业 | 1 | Encord | 物理 AI 与多模态数据 | 高 |  |
| frontier labs | 企业 | 1 | Bespoke Labs | 推理数据策展、定制 RL 环境/评测数据 | 低 |  |
| kluster.ai | AI 应用公司 | 1 | Bespoke Labs | Curator 推理 API 合作推广 | 高 |  |
| neolabs | frontier lab | 1 | Bespoke Labs | RL 环境与智能体训练/评测基础设施 | 中 |  |
| poolside | frontier lab | 1 | Toloka | 专家数据 / LLM 与代理训练数据 | 高 |  |
| vLex | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 | 中 |  |
| 上汽 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 | 中 |  |
| 上海交通大学 | 高校研究机构 | 1 | AGI-Eval | CoreCodeBench 工程级代码评测 | 高 |  |
| 上海人工智能实验室 OpenDataLab（OmniDocBench） | 高校研究机构 | 1 | Abaka AI | OmniDocBench 数据集标注 | 高 |  |
| 上海人工智能实验室（中国大模型语料数据联盟） | 高校研究机构 | 1 | 上海数据交易所 | 大模型语料数据联盟成员、语料专区 | 低 |  |
| 上海库帕思科技 | 企业 | 1 | 整数智能 MolarData | 共建语料生态产业链 | 中 |  |
| 上海智元新创（智元机器人） | 垂直 AI | 1 | 库帕思 Kupas | 具身智能行业语料库构建、标准共建 | 中 |  |
| 上海电信 | 企业 | 1 | 库帕思 Kupas | AI+数据语料融合应用、垂类智能体 | 中 |  |
| 东京大学 | 高校研究机构 | 1 | Abaka AI | KINA知识评测基准 | 中 |  |
| 东方财富 | 金融机构 | 1 | 司南 OpenCompass | OpenFinData 金融评测集 | 低 |  |
| 中国信通院 | 政府 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 | 中 |  |
| 中国科学院自动化研究所 | 高校研究机构 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 | 中 |  |
| 中国移动 | 企业 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | AI训练数据（语音/视觉/NLP） | 高 |  |
| 中国移动北京/北京电信/北京联通/工行北京分行等 | 企业 | 1 | 北京国际大数据交易所 | 北京数据集团揭牌时签署战略合作 | 低 |  |
| 中国银行 | 金融机构 | 1 | 标贝科技 DataBaker | 语音合成/识别数据及TTS定制 | 低 |  |
| 丰田 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 | 中 |  |
| 丰田 Toyota | 企业 | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 | 中 |  |
| 丰田研究院 | frontier lab | 1 | 光轮智能 Lightwheel | Newton开源物理引擎指导委员会 | 中 |  |
| 乐聚机器人 | 垂直 AI | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 人形机器人数据采集、训练场落地、数据标准 | 中 |  |
| 人形机器人数据训练中心（北京石景山） | 其他 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 具身智能数据训练场：数据资源开发、训练中心建设 | 中 |  |
| 企业 | frontier lab | 1 | Bespoke Labs | RL 环境与智能体训练/评测基础设施 | 中 |  |
| 企业生产力 | 企业 | 1 | Veris AI | 企业 agent 模拟训练环境 | 中 |  |
| 元戎 | 垂直AI | 1 | 恺望数据 | 自动驾驶数据 | 中 |  |
| 制造业） | 企业 | 1 | Veris AI | 企业 agent 模拟训练环境 | 中 |  |
| 前沿实验室 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 | 中 |  |
| 北京大学 | 高校研究机构 | 1 | 智源 FlagEval | HalluDial 幻觉评测集 | 中 |  |
| 北京师范大学 | 高校研究机构 | 1 | 智源 FlagEval | CMMU 多模态评测集 | 中 |  |
| 北京瑞莱智慧科技有限公司 | AI 应用公司 | 1 | 深圳数据交易所 | 语料数据场内交易首单（买方；卖方为哈工大深圳） | 低 |  |
| 北大 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 | 中 |  |
| 华为云 | 科技大厂 | 1 | 星尘数据 Stardust | 智驾数据标注；智驾数据；ModelArts标注平台合作伙伴 | 中 |  |
| 华为云/中国信通院 | 科技大厂 | 1 | 深圳数据交易所 | 可信数据空间创新实验室：大模型语料合规流通 | 低 |  |
| 华为云盘古大模型生态 | 科技大厂 | 1 | 星尘数据 Stardust | 大模型生态伙伴 | 低 |  |
| 华为数据存储 | 科技大厂 | 1 | 景联文科技 | AI数据湖数据工程联合解决方案 | 中 |  |
| 博世 Bosch | 企业 | 1 | 光轮智能 Lightwheel | 仿真/合成数据 | 中 |  |
| 卡内基梅隆大学 | 高校研究机构 | 1 | Abaka AI | KINA知识评测基准 | 中 |  |
| 卡塔尔政府 | 政府 | 1 | Scale AI | 五年合作，支撑 50 多个公共部门 AI 应用 | 低 |  |
| 吉利 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 | 中 |  |
| 吉利 Geely | 企业 | 1 | 光轮智能 Lightwheel | GR00T N1.5 部署于吉利工厂 Unitree H1 人形机器人 | 中 |  |
| 喜马拉雅/Rokid/Roobo | AI 应用公司 | 1 | 标贝科技 DataBaker | 语音合成数据与解决方案 | 低 |  |
| 大疆 | 科技大厂 | 1 | 龙猫数据 | 终端/互联网数据采集标注 | 低 |  |
| 奇瑞 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 | 中 |  |
| 好未来 | 科技大厂 | 1 | 曼孚科技 MindFlow | 自动驾驶/安防/人脸等数据标注 | 低 |  |
| 小米 | 科技大厂 | 1 | 星尘数据 Stardust | 数据标注 | 低 |  |
| 小红书 | AI 应用公司 | 1 | 热热数据 | 内容审核业务 | 中 |  |
| 小鹏汽车 | 企业 | 1 | 标贝科技 DataBaker | 语音合成/识别数据及TTS定制 | 低 |  |
| 广汽 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 | 中 |  |
| 开放传神 OpenCSG | AI应用公司 | 1 | 数据堂 Datatang | 训练数据资源共享与开源生态 | 中 |  |
| 循环智能 | AI 应用公司 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 高质量中文大模型训练数据集共建项目 | 低 |  |
| 拓维信息 | 企业 | 1 | 整数智能 MolarData | 搭载DeepSeek的智能数据标注一体机 | 中 |  |
| 整数智能 | 其他 | 1 | 库帕思 Kupas | 共建语料生态产业链 | 中 |  |
| 新实验室 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 | 中 |  |
| 智元机器人 | 垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 | 中 |  |
| 智元机器人 AgiBot | 垂直 AI | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 | 中 |  |
| 最大客户 | 科技大厂 | 1 | Innodata | 2026 Q2 最大客户占 37%（Q1 为 56%），另一大厂客户从 17% 升至 34%；最大客户新签长程智能体个性化与电脑操作 RL 环境项目 | 高 |  |
| 欧盟委员会 | 其他 | 1 | Prolific | 研究与企业客户 | 低 |  |
| 比亚迪 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 | 中 |  |
| 比亚迪 BYD | 企业 | 1 | 光轮智能 Lightwheel | 仿真/合成数据 | 中 |  |
| 毫末 | 垂直AI | 1 | 恺望数据 | 自动驾驶数据 | 中 |  |
| 毫末智行 | 垂直 AI | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） | 中 |  |
| 海康威视 | 企业 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | AI训练数据（语音/视觉/NLP） | 高 |  |
| 清华 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 | 中 |  |
| 港科大 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 | 中 |  |
| 滴滴 | 科技大厂 | 1 | 标贝科技 DataBaker | 语音合成/识别数据及TTS定制 | 低 |  |
| 澜舟科技 | 国内大模型公司 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 | 中 |  |
| 灵心巧手 | 垂直AI | 1 | 数据堂 Datatang | 具身智能数据 | 中 |  |
| 理想 | 企业 | 1 | 龙猫数据 | 自动驾驶数据标注 | 低 |  |
| 百度AI市场 | 科技大厂 | 1 | 云测数据 Testin Data | 数据标注服务上架百度AI市场（渠道） | 低 |  |
| 百度文心一言（内部） | 国内大模型公司 | 1 | 百度智能云数据众包 | 海口大模型数据标注基地为文心一言做RLHF/标注 | 低 |  |
| 百度智能云 千帆 | 科技大厂 | 1 | 百度众测 | 内部自建专家/众包平台，为本公司模型供数：SFT、RM、模型评估标注；多领域专家资源库（计算机/法律/医疗） | 中 |  |
| 百度等30余家 | 科技大厂 | 1 | 司南 OpenCompass | 采用司南评测体系开展研发 | 低 |  |
| 红杉中国 xbench | 其他 | 1 | UniPat AI | BabyVision 由 xbench 与 UniPat 团队及多家模型公司研究者共建 | 中 |  |
| 美国主要 AI 实验室 | frontier lab | 1 | Labelbox | 覆盖 80% 以上美国头部 AI 实验室 | 低 |  |
| 美国国防部（CDAO） | 政府 | 1 | Scale AI | 生产协议上限从 1 亿提高到 5 亿美元，用于数据处理与决策支持 | 中 |  |
| 美国政府机构 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 | 中 |  |
| 美国空军 | 政府 | 1 | Surge AI | 政府客户 | 中 |  |
| 联想 | 科技大厂 | 1 | 希尔贝壳 AISHELL | 语音数据采标 | 低 |  |
| 腾讯朱雀实验室 | 科技大厂 | 1 | 司南 OpenCompass | SecBench 网络安全评测 | 低 |  |
| 腾讯科恩实验室 | 科技大厂 | 1 | 司南 OpenCompass | SecBench 网络安全评测 | 低 |  |
| 腾讯科技（成都）有限公司 | 科技大厂 | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） | 中 |  |
| 蔚来 | 企业 | 1 | 龙猫数据 | 自动驾驶数据标注 | 低 |  |
| 蚂蚁集团 | 国内大模型公司 | 1 | AfterQuery | 训练数据 | 中 |  |
| 西北工业大学音频语音与语言处理研究组 | 高校研究机构 | 1 | 希尔贝壳 AISHELL | 联合实验室（智能语音与多模态数据） | 低 |  |
| 觅蜂科技（蜂巢数据共创行动） | 垂直 AI | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 物理AI/具身智能数据规模化采集与治理 | 中 |  |
| 诠视科技 | 垂直 AI | 1 | 数据堂 Datatang | 具身智能数据战略合作 | 低 |  |
| 超大云厂商 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 | 中 |  |
| 迪士尼研究院 | frontier lab | 1 | 光轮智能 Lightwheel | Newton开源物理引擎指导委员会 | 中 |  |
| 银河通用 Galbot | 垂直 AI | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 | 中 |  |
| 银河通用机器人 | 垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 | 中 |  |
| 长安 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 | 中 |  |
| 高通 | 企业、科技大厂 | 1 | 晴数智慧 Magic Data | 对话式AI/语音/多轮对话数据集；对话式AI/语音数据 | 低 |  |
| 鹏城实验室 | 高校研究机构 | 1 | 数据堂 Datatang | AI评测测试业务（2023年新增主要客户） | 中 |  |
| （前沿实验室整体） | frontier lab | 1 | Gray Swan AI | AI 安全 | 中 |  |
| Beacon Software | 企业 | 0 | Haize Labs（变动） | 被 Beacon 收购，转为其应用 AI 研究组服务 45 家投资组合公司 | 高 |  |
| Datadog | 科技大厂 | 0 | Adaptive ML（变动） | 被 Datadog 收购并入 Datadog AI Research（独立性终止） | 高 |  |
| LexisNexis (Lexis+AI) | 垂直 AI | 0 | Vals AI（变动） | 法律 AI 基准退出 | 中 |  |
| Scale 流失客户 | frontier lab | 0 | Labelbox（变动） | CEO 称年底前可能从 Scale 流失客户处获得数亿美元新收入 | 中 |  |
| Scale 流失客户（多家实验室） | frontier lab | 0 | Turing（变动） | Turing CEO 称 Meta-Scale 交易是转折点，承接流失客户 | 低 |  |
| micro1 | 其他 | 0 | Spirit Airlines（变动） | 竞购企业数据（报价1250万美元） | 低 |  |

## 不在我们名单上的买方（至少一条中或高置信度声明）

| 客户 | 类型 | 现有供应商数 | 点名的供应商 | 采购内容 |
|---|---|---|---|---|
| NVIDIA | frontier lab、其他、科技大厂 | 12 | Scale AI、Translated、光轮智能 Lightwheel、General Reasoning、Applied Compute、Mercor、Turing、Centific、AfterQuery、Patronus AI、晴数智慧 Magic Data、Prime Intellect | HelpSteer2/HelpSteer3 偏好数据的标注员通过 Scale AI 签约；HelpSteer3 偏好数据：通用/STEM/代码子集标注；HelpSteer3 多语言子集标注；Isaac Lab-Arena 评测/任务层共建；GR00T 模型部署；合成数据；Lab 平台上可 RL 微调的开源模型；Nemo |
| Amazon | 其他、科技大厂 | 10 | 海天瑞声 SpeechOcean/DataOcean AI、Collinear AI、Gray Swan AI、Toloka、Turing、Invisible Technologies、micro1、Centific、Patronus AI、METR | 2019年前五大客户；AI训练数据（语音/视觉/NLP）；AWS Marketplace 上架/AWS Startups 合作；Gray Swan Arena 红队竞技场赞助；RL 仿真环境/训练数据；专家数据 / LLM 与代理训练数据；为这些公司生成专家级数据集；公司自述客户；前沿风险评估试点；客户包括前沿实验室、 |
| Microsoft | frontier lab、其他、科技大厂 | 10 | Surge AI、海天瑞声 SpeechOcean/DataOcean AI、Toloka、Turing、Invisible Technologies、micro1、Centific、Scale AI（变动）、标贝科技 DataBaker、晴数智慧 Magic Data、Handshake AI（变动）、Sama | AI训练数据（语音/视觉/NLP）；CEO 在融资报道中点名；Forbes 报道列出的客户；MAI-Thinking-1 盲测人类评测（1276个任务，专业评分员）；Meta-Scale 交易后转向 Handshake 等供应商；RLHF 合同；专家数据 / LLM 与代理训练数据；为这些公司生成专家级数据集；公司自述 |
| 百度 | 科技大厂 | 8 | 海天瑞声 SpeechOcean/DataOcean AI、数据堂 Datatang、恺望数据、标贝科技 DataBaker、晴数智慧 Magic Data、曼孚科技 MindFlow、星尘数据 Stardust、希尔贝壳 AISHELL | 2022年前五大客户（自动驾驶/语音等训练数据）；AI大模型数据；AI训练数据（语音/视觉/NLP）；对话式AI/语音/多轮对话数据集；对话式AI/语音数据；数据标注；自动驾驶/安防/人脸等数据标注；语音合成/识别数据及TTS定制；语音数据采标 |
| 京东 | 科技大厂 | 5 | 京东众智、标贝科技 DataBaker、星尘数据 Stardust、倍赛 BasicFinder、希尔贝壳 AISHELL | 数据标注；数据采集标注；电商商品内容生成、智能仓储等“标-训-推”一体化；语音合成/识别数据及TTS定制；语音数据采标 |
| Hugging Face | AI 应用公司、其他 | 3 | Snorkel AI、Bespoke Labs、Prime Intellect | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；Lab 平台上可 RL 微调的开源模型；联合举办推理数据集竞赛（Curator） |
| Nebius | 其他、科技大厂 | 3 | Toloka、General Reasoning、Prime Intellect | INTELLECT-3 推理服务；OpenReward 上架 SWE-rebench-v2；Tendem 人类专家按需接入智能体（MCP） |
| Prime Intellect | AI 应用公司、其他 | 3 | Snorkel AI、Proximal、BenchFlow | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；FrontierSWE 以 Prime Intellect Environment 形式上架；框架支持运行 Prime Intellect/Verifiers 托管环境 |
| Together AI | AI 应用公司、其他 | 3 | Snorkel AI、Bespoke Labs、Collinear AI | $3M Open Benchmarks Grants 共同支持方；300 万美元 Open Benchmarks Grants，资助开源智能体基准；TraitBasis 模拟用户集成进 Together Evals；联合举办推理数据集竞赛（Curator） |
| 科大讯飞 | 国内大模型公司、科技大厂 | 3 | 海天瑞声 SpeechOcean/DataOcean AI、曼孚科技 MindFlow、倍赛 BasicFinder | AI训练数据（语音/视觉/NLP）；数据采集标注；自动驾驶/安防/人脸等数据标注 |
| AI21 Labs | AI 应用公司、frontier lab | 2 | Haize Labs、Invisible Technologies | SFT/RLHF 专家劳动力与流程平台；多百万美元红队合同；自动化红队/越狱测试 |
| Apple | 科技大厂 | 2 | TransPerfect、Huzzle Labs | Apple Intelligence 回答标注（巴塞罗那约200人）；RL 环境/专家轨迹/评测（官网自称，未经第三方核实） |
| Artificial Analysis | 其他 | 2 | Mercor、Datacurve | APEX-Agents-AA 独立排行榜；DeepSWE 基准被纳入 Coding Agent Index |
| Cognition | AI 应用公司 | 2 | Mercor、Applied Compute | APEX-SWE 软件工程基准；定制 RL 后训练模型 / 企业代理 |
| Cohere | AI 应用公司、frontier lab | 2 | Appen、Invisible Technologies | Command R 幻觉减少、10 种语言扩展、稀有编程语言；Command 模型微调专家标注 |
| Cua | AI 应用公司 | 2 | HUD、Snorkel AI | 基于 Cua-Bench 构建 CUA-Bench+ 计算机使用数据；电脑使用 agent 评测集成（OSWorld 等） |
| DoorDash | 企业 | 2 | Applied Compute、HUD | RL 环境/评测平台；定制 RL 后训练模型 / 企业代理 |
| IBM | 企业、科技大厂 | 2 | DataForce、SuperAnnotate | B 轮报道列出的客户；Granite Guardian 风险检测人工标注 |
| Laude Institute | 高校研究机构 | 2 | Snorkel AI、Bespoke Labs | Frontier-Bench（原 Terminal-Bench 3.0）/Terminal-Bench Science；Terminal-Bench（Stanford+Laude 主导的开放学术合作；Bespoke 提供 API 额度） |
| Toyota Research Institute | 企业、其他 | 2 | Bespoke Labs、Scale AI | OpenThoughts 项目共同赞助/合作；融资稿列出的客户 |
| 三星 | 企业、科技大厂 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、龙猫数据 | AI训练数据（语音/视觉/NLP）；终端/互联网数据采集标注；语音数据；2020年销售额大幅下滑 |
| 中国科学院 | 科技大厂、高校研究机构 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、倍赛 BasicFinder | AI训练数据（语音/视觉/NLP）；数据采集标注 |
| 博世 | 企业 | 2 | 光轮智能 Lightwheel、龙猫数据 | 仿真资产/合成数据/评测；自动驾驶数据标注 |
| 商汤 | AI应用公司、科技大厂 | 2 | 恺望数据、倍赛 BasicFinder | AI大模型数据；数据采集标注 |
| 旷视 | 垂直AI、科技大厂 | 2 | 恺望数据、曼孚科技 MindFlow | 自动驾驶/安防/人脸等数据标注；自动驾驶数据 |
| 清华大学 | 高校研究机构 | 2 | 海天瑞声 SpeechOcean/DataOcean AI、百度智能云数据众包 | AI训练数据（语音/视觉/NLP）；十亿像素级视频数据集PANDA |
| 美国联邦政府 | 政府 | 2 | Snorkel AI、Mercor | 专家数据/环境服务（未具名机构）；获得联邦合同 |
| 美国陆军 | 其他、政府 | 2 | Surge AI、Scale AI | 政府客户；融资稿列出的客户 |
| AT&T | 企业 | 1 | Adaptive ML | RLOps 平台微调专用模型，嵌入 FDE（反欺诈、客服、text-to-SQL 等 50+ 用例） |
| AXA Financial | 企业 | 1 | Encord | 物理 AI 与多模态数据 |
| American Family Insurance | 其他 | 1 | Invisible Technologies | 公司自述客户 |
| Applied Compute | AI 应用公司 | 1 | Mercor | 公司法任务专家数据后训练（约2000例） |
| Arcee AI | AI 应用公司 | 1 | Prime Intellect | INTELLECT-1 去中心化训练协作 |
| Aurora | 企业 | 1 | Uber AI Solutions | 50 多家企业客户中点名的两家 |
| BOUNTY COUNTRY PTY LTD | 其他 | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） |
| CAISI (NIST) | 政府 | 1 | Gray Swan AI | 加入 UK AISI 智能体红队挑战赛 |
| Center for AI Safety | 其他 | 1 | Scale AI | Humanity's Last Exam |
| Center for AI Safety（CAIS） | 高校研究机构 | 1 | Scale AI | Humanity's Last Exam 专家难题基准 |
| Charlotte Hornets | 其他 | 1 | Invisible Technologies | 公司自述客户 |
| Circadence | 企业 | 1 | Scale AI | 政府与企业网络安全智能体 |
| DataComp 社区 | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 开源推理数据集 |
| Databricks（Mosaic AI） | 科技大厂 | 1 | SuperAnnotate | DBRX 微调数据与 RAG 评测；获 2025 Databricks ISV 客户影响力合作伙伴奖 |
| Dell | 其他 | 1 | Centific | 融资报道列出的客户 |
| Eigent | AI 应用公司 | 1 | General Reasoning | OpenReward 上架 SETA 环境 |
| Etsy | 企业 | 1 | Patronus AI | 多模态 LLM-as-a-Judge 图片描述幻觉检测 |
| Factory | AI 应用公司 | 1 | Snorkel AI | $3M Open Benchmarks Grants 共同支持方 |
| Figure AI | 垂直 AI、垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测；具身仿真/合成数据 |
| Fisher Phillips | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） |
| Flapping Airplanes | 其他 | 1 | Prime Intellect | 托管后训练/RL 平台（新兴研究实验室 neolab） |
| Gamma | AI 应用公司 | 1 | Patronus AI | 自动化评测（Patronus Judges） |
| HP | 科技大厂 | 1 | Patronus AI | LLM 自动评测/幻觉检测 |
| Harvard Law School | 高校研究机构 | 1 | Mercor | APEX 基准由 Mercor 与外部专家（Sunstein、Topol）合著 |
| Juelich Supercomputing Center (JSC) | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究/算力 |
| Kore.ai | AI 应用公司 | 1 | Collinear AI | 客服智能体数据包、9 语种安全与质量 |
| LAION | 其他 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 |
| Legaltech Hub | 其他 | 1 | Vals AI | 法律 AI 基准研究合作方 |
| Legora | 垂直 AI | 1 | AfterQuery | 法律领域专家数据 |
| Lenovo | 其他 | 1 | Centific | 融资报道列出的客户 |
| M-A-P | 科技大厂、高校研究机构 | 1 | Abaka AI | KINA知识评测基准；SuperGPQA 285学科研究生级评测集 |
| Manulife | 金融机构 | 1 | Adaptive ML | 多年期协议，RLOps 层（核保报价、销售顾问等）；多年期协议，模型微调 |
| McDermott Will & Emery | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） |
| Motif Technologies（韩国） | 其他 | 1 | AfterQuery | 韩国大模型实验室训练数据 |
| Niantic | 企业 | 1 | Uber AI Solutions | 50 多家企业客户中点名的两家 |
| Nous Research | AI 应用公司 | 1 | hillclimb | Nomos 1 模型卡注明与 Hillclimb AI 合作训练；Putnam 数学模型；媒体报道；联合训练数学模型 Nomos 1（Putnam 87/120） |
| Ogletree Deakins | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） |
| Palantir | 企业 | 1 | Innodata | 为 Palantir 项目做标注、多模态数据工程和生成式 AI 工作流支持 |
| Pearson | 企业 | 1 | Patronus AI | LLM 自动评测/幻觉检测 |
| Phantom AI | 垂直 AI | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） |
| PublicAI | AI 应用公司 | 1 | Abaka AI | 1024 万美元战略合作，为 KOR-Bench/SuperGPQA 征集难题 |
| PyTorch | 其他 | 1 | Snorkel AI | 300 万美元 Open Benchmarks Grants，资助开源智能体基准 |
| PyTorch Foundation | 其他 | 1 | Snorkel AI | $3M Open Benchmarks Grants 共同支持方 |
| Ramp | 企业 | 1 | Prime Intellect | 托管后训练/RL 平台 |
| Recraft | AI 应用公司 | 1 | Toloka | 专家数据 / LLM 与代理训练数据 |
| Reed Smith | 企业 | 1 | Vals AI | 法律 AI 基准律所联盟（律师对照组） |
| SK Telecom | 企业 | 1 | Adaptive ML | 多语种内容审核，微调 Gemma 3 |
| Scripps Research | 高校研究机构 | 1 | Mercor | APEX 基准由 Mercor 与外部专家（Sunstein、Topol）合著 |
| Sequrity.ai | AI 应用公司 | 1 | Gray Swan AI | Safeguards 挑战赛奖金赞助 |
| Shopify | 企业、其他 | 1 | Toloka | 专家数据 / LLM 与代理训练数据；融资报道列出的客户，业务为安全评测、红队、专家数据 |
| Skydio | 企业 | 1 | Encord | 物理 AI 与多模态数据 |
| Skyvern | AI 应用公司 | 1 | Halluminate | Web Bench 浏览器 agent 基准 |
| Snorkel AI | 其他 | 1 | Cua | 在 Cua-Bench 框架上共建 KiCad 计算机使用基准（CUA-Bench+） |
| Snowflake | 其他 | 1 | Deccan AI | 后训练数据、评测、RL |
| Stanford University | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究；Terminal-Bench（Stanford+Laude 主导的开放学术合作；Bespoke 提供 API 额度） |
| Synthesia | 企业 | 1 | Encord | 物理 AI 与多模态数据 |
| Tailscale | 科技大厂 | 1 | Apollo Research | Watcher 智能体监控接入 Tailscale Aperture 网关 |
| Thomson Reuters | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 |
| UC Berkeley | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 |
| UK AISI | 政府 | 1 | Gray Swan AI | Gray Swan Arena 红队竞技场赞助；智能体红队挑战赛联合举办 |
| US AISI | 政府 | 1 | Gray Swan AI | 加入 UK AISI 智能体红队挑战赛 |
| US CAISI (NIST) | 政府 | 1 | Gray Swan AI | CAISI 发布大规模红队竞赛智能体安全研究 |
| University of Oxford (OATML) | 高校研究机构 | 1 | Gray Swan AI | Safeguards 挑战赛联合赞助 |
| University of Washington | 高校研究机构 | 1 | Bespoke Labs | OpenThoughts 推理数据集联合研究 |
| Upstage | 其他 | 1 | Flitto | Solar Open 2 大规模训练数据构建；韩国主权AI项目联合体中负责数据集构建 |
| Vecflow | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 |
| Woven by Toyota | 企业 | 1 | Encord | 物理 AI 与多模态数据 |
| Zapier | AI 应用公司 | 1 | Prime Intellect | 托管后训练/RL 平台 |
| Zipline | 企业 | 1 | Encord | 物理 AI 与多模态数据 |
| kluster.ai | AI 应用公司 | 1 | Bespoke Labs | Curator 推理 API 合作推广 |
| neolabs | frontier lab | 1 | Bespoke Labs | RL 环境与智能体训练/评测基础设施 |
| poolside | frontier lab | 1 | Toloka | 专家数据 / LLM 与代理训练数据 |
| vLex | 垂直 AI | 1 | Vals AI | 法律 AI 基准（VLAIR）参评 |
| 上汽 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 |
| 上海交通大学 | 高校研究机构 | 1 | AGI-Eval | CoreCodeBench 工程级代码评测 |
| 上海人工智能实验室 OpenDataLab（OmniDocBench） | 高校研究机构 | 1 | Abaka AI | OmniDocBench 数据集标注 |
| 上海库帕思科技 | 企业 | 1 | 整数智能 MolarData | 共建语料生态产业链 |
| 上海智元新创（智元机器人） | 垂直 AI | 1 | 库帕思 Kupas | 具身智能行业语料库构建、标准共建 |
| 上海电信 | 企业 | 1 | 库帕思 Kupas | AI+数据语料融合应用、垂类智能体 |
| 东京大学 | 高校研究机构 | 1 | Abaka AI | KINA知识评测基准 |
| 中国信通院 | 政府 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 |
| 中国科学院自动化研究所 | 高校研究机构 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 |
| 中国移动 | 企业 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | AI训练数据（语音/视觉/NLP） |
| 丰田 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 |
| 丰田 Toyota | 企业 | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 |
| 丰田研究院 | frontier lab | 1 | 光轮智能 Lightwheel | Newton开源物理引擎指导委员会 |
| 乐聚机器人 | 垂直 AI | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 人形机器人数据采集、训练场落地、数据标准 |
| 人形机器人数据训练中心（北京石景山） | 其他 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 具身智能数据训练场：数据资源开发、训练中心建设 |
| 企业 | frontier lab | 1 | Bespoke Labs | RL 环境与智能体训练/评测基础设施 |
| 企业生产力 | 企业 | 1 | Veris AI | 企业 agent 模拟训练环境 |
| 元戎 | 垂直AI | 1 | 恺望数据 | 自动驾驶数据 |
| 制造业） | 企业 | 1 | Veris AI | 企业 agent 模拟训练环境 |
| 前沿实验室 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 |
| 北京大学 | 高校研究机构 | 1 | 智源 FlagEval | HalluDial 幻觉评测集 |
| 北京师范大学 | 高校研究机构 | 1 | 智源 FlagEval | CMMU 多模态评测集 |
| 北大 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 |
| 华为云 | 科技大厂 | 1 | 星尘数据 Stardust | 智驾数据标注；智驾数据；ModelArts标注平台合作伙伴 |
| 华为数据存储 | 科技大厂 | 1 | 景联文科技 | AI数据湖数据工程联合解决方案 |
| 博世 Bosch | 企业 | 1 | 光轮智能 Lightwheel | 仿真/合成数据 |
| 卡内基梅隆大学 | 高校研究机构 | 1 | Abaka AI | KINA知识评测基准 |
| 吉利 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 |
| 吉利 Geely | 企业 | 1 | 光轮智能 Lightwheel | GR00T N1.5 部署于吉利工厂 Unitree H1 人形机器人 |
| 奇瑞 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 |
| 小红书 | AI 应用公司 | 1 | 热热数据 | 内容审核业务 |
| 广汽 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 |
| 开放传神 OpenCSG | AI应用公司 | 1 | 数据堂 Datatang | 训练数据资源共享与开源生态 |
| 拓维信息 | 企业 | 1 | 整数智能 MolarData | 搭载DeepSeek的智能数据标注一体机 |
| 整数智能 | 其他 | 1 | 库帕思 Kupas | 共建语料生态产业链 |
| 新实验室 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 |
| 智元机器人 | 垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 |
| 智元机器人 AgiBot | 垂直 AI | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 |
| 最大客户 | 科技大厂 | 1 | Innodata | 2026 Q2 最大客户占 37%（Q1 为 56%），另一大厂客户从 17% 升至 34%；最大客户新签长程智能体个性化与电脑操作 RL 环境项目 |
| 比亚迪 | 企业 | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 |
| 比亚迪 BYD | 企业 | 1 | 光轮智能 Lightwheel | 仿真/合成数据 |
| 毫末 | 垂直AI | 1 | 恺望数据 | 自动驾驶数据 |
| 毫末智行 | 垂直 AI | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） |
| 海康威视 | 企业 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | AI训练数据（语音/视觉/NLP） |
| 清华 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 |
| 港科大 | 科技大厂 | 1 | Abaka AI | REER逆向工程推理（开放式生成）论文，2077AI为署名机构 |
| 澜舟科技 | 国内大模型公司 | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 大模型数据处理技术、大模型数据集供给、大模型评测 |
| 灵心巧手 | 垂直AI | 1 | 数据堂 Datatang | 具身智能数据 |
| 百度智能云 千帆 | 科技大厂 | 1 | 百度众测 | 内部自建专家/众包平台，为本公司模型供数：SFT、RM、模型评估标注；多领域专家资源库（计算机/法律/医疗） |
| 红杉中国 xbench | 其他 | 1 | UniPat AI | BabyVision 由 xbench 与 UniPat 团队及多家模型公司研究者共建 |
| 美国国防部（CDAO） | 政府 | 1 | Scale AI | 生产协议上限从 1 亿提高到 5 亿美元，用于数据处理与决策支持 |
| 美国政府机构 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 |
| 美国空军 | 政府 | 1 | Surge AI | 政府客户 |
| 腾讯科技（成都）有限公司 | 科技大厂 | 1 | 数据堂 Datatang | 2022年前五大客户（自动驾驶/语音等训练数据） |
| 蚂蚁集团 | 国内大模型公司 | 1 | AfterQuery | 训练数据 |
| 觅蜂科技（蜂巢数据共创行动） | 垂直 AI | 1 | 海天瑞声 SpeechOcean/DataOcean AI | 物理AI/具身智能数据规模化采集与治理 |
| 超大云厂商 | 其他 | 1 | Snorkel AI | 客户类型描述，ARR 3.75 亿美元 |
| 迪士尼研究院 | frontier lab | 1 | 光轮智能 Lightwheel | Newton开源物理引擎指导委员会 |
| 银河通用 Galbot | 垂直 AI | 1 | 光轮智能 Lightwheel | 具身仿真/合成数据 |
| 银河通用机器人 | 垂直AI | 1 | 光轮智能 Lightwheel | 仿真资产/合成数据/评测 |
| 长安 | 企业 | 1 | 恺望数据 | 自动驾驶数据采集标注 |
| 鹏城实验室 | 高校研究机构 | 1 | 数据堂 Datatang | AI评测测试业务（2023年新增主要客户） |
| （前沿实验室整体） | frontier lab | 1 | Gray Swan AI | AI 安全 |
| Beacon Software | 企业 | 0 | Haize Labs（变动） | 被 Beacon 收购，转为其应用 AI 研究组服务 45 家投资组合公司 |
| Datadog | 科技大厂 | 0 | Adaptive ML（变动） | 被 Datadog 收购并入 Datadog AI Research（独立性终止） |
| LexisNexis (Lexis+AI) | 垂直 AI | 0 | Vals AI（变动） | 法律 AI 基准退出 |
| Scale 流失客户 | frontier lab | 0 | Labelbox（变动） | CEO 称年底前可能从 Scale 流失客户处获得数亿美元新收入 |

## 公开承认向外采购、但没点名供应商的买方

- OpenAI（2 条）
- 字节跳动（2 条）
- NVIDIA（2 条）
- Anthropic（1 条）
- Google DeepMind（1 条）
- SpaceX（原 xAI）（1 条）
- Cohere（1 条）
- Amazon（1 条）
- Meta（1 条）
- Harvey（1 条）
- 中国头部6家AI实验室（1 条）
- Mistral AI（1 条）
- Microsoft（1 条）
- 腾讯（1 条）

## 供应商声称有、但没点名的客户

- 未具名 frontier labs：Bespoke Labs、Deeptune、Fleet、Good Start Labs、Refresh
- 1X Technologies：光轮智能 Lightwheel
- 头部大模型公司（未具名）：智能知识、曼孚科技 MindFlow
- 中国科技大厂（未具名）：Appen
- frontier AI labs 与世界500强（未具名）：Abaka AI
- 头部车企与智能驾驶算法客户（未具名）：整数智能 MolarData
- 头部手机厂商和大模型公司（未具名）：景联文科技
- 约60家大模型公司（未具名）：景联文科技
- 多家大模型企业（未具名）：博登智能 Boden AI
- 互联网头部企业（未具名）：热热数据
- 未具名AI科技厂商：澳鹏中国 Appen China
- 大模型AI企业（未具名）：澳鹏中国 Appen China
- 中国知网/中文在线/中汽智联/中国搜索等36家：北京国际大数据交易所
- 前沿模型团队（未具名）：Copula Lab
- 160+ 中大型企业（未具名）：SuperCLUE
- 多家头部猎头公司（未具名）：xbench
- 头部营销公司（未具名）：xbench
- 8 家前沿实验室（未具名）：Handshake AI
- 1X：micro1
- 美国前十大银行中的 7 家：Snorkel AI
- 全球十大科技公司中的 8 家：Appen
- 某头部社交媒体客户（未具名）：TELUS Digital
- 最大客户（未具名，外界普遍推测为 Meta）：Innodata
- "Magnificent Seven" 中的 5 家：Innodata
- 另一大厂客户（均未具名）：Innodata
- 新前沿实验室客户（未具名）：Innodata
- "Magnificent Seven" 大厂客户（未具名）：Innodata
- 生成式 AI 七大公司中的 3 家：iMerit
- 8 家自动驾驶公司：iMerit
- 3 个美国政府机构：iMerit
- 某大型科技公司（未具名）：RWS TrainAI
- 主要 frontier labs（未具名，称全部头部实验室为客户）：AfterQuery
- 未具名 AI 实验室：Datacurve
- 未具名早期企业客户（金融服务：Veris AI
- 未具名 Fortune 500 企业：Bespoke Labs
- 未具名 三家全球前四 AI 实验室：Collinear AI
- 未具名 国家级 AI 研究实验室：Collinear AI
- 未具名 frontier AI labs：Preference Model
- 未具名 1–3 家实验室（独家合同）：Preference Model
- 未具名 Fortune 500 与顶级 AI 研究实验室：Sepal AI
- 未具名 4 家头部 AI 公司（Chat Arena 前六中的四家）：Calaveras
- 未具名 美国前沿实验室：Calaveras
- 未具名 frontier labs（自称）：Refresh
- （未具名）多数前沿实验室与超大规模云厂商：Patronus AI
- 未具名头部 frontier lab（首个直签合同）：Poindexter Labs
