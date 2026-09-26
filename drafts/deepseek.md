# DeepSeek 深度求索

- 类别：国内大模型公司｜地区：国内（杭州）
- 收件人：**邵智宏（Zhihong Shao）**，DeepSeek 研究员（Research Scientist），做推理 RL：GRPO（DeepSeekMath）、DeepSeek-R1、DeepSeekMath-V2（把推理 RL 扩展到难验证任务）
- 置信度：中。本人主页写明 "I am a Research Scientist at DeepSeek"，并说 DeepSeekMath "establishes the GRPO-based RL foundation for post-training DeepSeek models"（已读原文；主页已列出 2025-11 的 DeepSeekMath-V2，具体更新日期看不到）。2026-04 的 DeepSeek-V4 技术报告作者名单里有他，没有标"已离职"（已读原文）。主页没有写他带哪个团队，"后训练负责人"这个说法没有公开来源。
- 来源：
  - 本人主页：https://zhihongshao.github.io/ （源文件 https://github.com/zhihongshao/zhihongshao.github.io/blob/master/_pages/about.md ）
  - DeepSeek-V4 技术报告附录 A.1 作者名单（带 * 的是已离职）：https://arxiv.org/abs/2606.19348 。arXiv 在本环境打不开，读的是 GitHub 上的全文文本副本：https://github.com/bojieli/ai-infra-book/blob/main/references/text/deepseek-v4.txt
- 备选：
  - **吴俣（Yu Wu）**：2025 年初媒体称他是"DeepSeek 后训练团队负责人"，北航博士、前微软亚洲研究院（搜索摘要，2025 年报道，之后没有再核实）：https://36kr.com/p/3107974505942532 、https://news.pku.edu.cn/mtbdnew/15ac0b3e79244efa88b03a570cbcbcaa.htm 。V4 作者名单里有 "Yu Wu"，没有标离职（已读原文），但没法确认就是同一个人，也没法确认他现在还管后训练。置信度低。
  - **梁文锋**，创始人（只作为兜底），也在 V4 作者名单里。
- 数据 / 标注 / 数据采购负责人：**未找到**。
- 已离职（V4 报告里标 * 的 10 人）：王炳宣、阮翀、郭达雅、魏浩然、Haowei Zhang、Jun Ran、Junlong Li、Kezhao Huang、Y.Q. Wang、Zipeng Zhang（已读原文）。据报道，郭达雅 2026-03 去了字节 Seed，王炳宣去了腾讯（搜索摘要）：https://www.nbd.com.cn/articles/2026-04-25/4360477.html
- 称呼用"邵老师"：中文名由本人主页标题 "Zhihong Shao 邵智宏" 确认。

## 调研备注

**最近发布**
- **DeepSeek-V4 预览版**（2026-04-24）：V4-Pro 1.6T 参数（激活 49B），V4-Flash 284B（激活 13B），都支持 1M 上下文，开源权重。技术报告是 arXiv 2606.19348（已读全文文本）。后训练部分：
  - §5.1.1：数学、代码、agent、指令遵循等领域各训一个专家模型，先在领域数据上做 SFT，再用 GRPO 做 RL，奖励信号按领域定制。
  - 难验证任务不再用标量奖励模型，改为 "we curate rubric-guided RL data and employ a Generative Reward Model (GRM)"，而且 "only a minimal set of diverse human annotations"。
  - §5.1.2：用十多个教师模型做全词表 on-policy distillation，合并成一个模型，取代了 V3.2 的混合 RL 阶段。
  - §5.2.5：自研沙箱平台 DSec，单集群管理几十万个并发沙箱实例，底层用 3FS。
  - §5.4.3 白领任务：自建 30 个中文专业任务，覆盖金融、教育、法律、科技等 13 个行业，由标注员对比 Opus-4.6-Max 做盲评，不输率 63%。报告也写了弱项：指令遵循和格式美观。
  - §5.4.4 代码 agent：从 50 多名内部工程师收集约 200 个真实研发任务，每个任务配人工标注的评分标准，最后保留 30 个作评测集。
- **V4 正式版**（2026-07 中旬）：7-15 起高峰时段按 2 倍计价（二手资料，称出自官方更新日志）：https://github.com/xbtlin/ai-berkshire/blob/main/reports/中国大模型六强横向研究-20260721/03-DeepSeek.md
- **DeepSeek Harness**（仓库 2026-08-13 创建）：开源 agent 框架，"everything-is-a-plugin"，目前是开发者预览版（已读 README）：https://github.com/deepseek-ai/deepseek-harness
- **V4.1-Flash**（2026-09-10）：新结构，原生支持多模态输入；9-14 起 V4 Pro 服务下线，请求转到 V4.1-Flash（搜索摘要）：https://news.qq.com/rain/a/20260909A0BH7M00 、https://news.qq.com/rain/a/20260910A04UP100 。deepseek-recipe 的 README 写了 V4 / V4.1 的 prompt 编码和 V4.1 的图像预处理，能对上（已读原文）：https://github.com/deepseek-ai/deepseek-recipe
- 其他开源：DeepSpec（推测解码训练与评测，2026-06）、DeepJIT、DeepSelect（2026-09，算子库）：https://github.com/deepseek-ai
- **融资**：据报道 2026-05 到 06 月完成首轮外部融资，约 500 亿元；IPO 最快 2026 年内递交材料（二手资料，出处同上 ai-berkshire 报告）。

**JD 里的数据需求**（talent.deepseek.com 在本环境打不开，以下没有 JD 原文）
- 2026-06-25 发"英雄帖"：33 个岗位，分七大类，"所有部门规模至少扩大一倍"；另设不限专业背景的"AI 跨界技术人才"岗位。Investing.com 的摘要说招聘重点是数据工程师、开发工程师和 AI 跨学科人才（新闻摘要，原始报道没有找到，读的是 GitHub 上的新闻存档副本）：https://github.com/EstLLLLL/Claude01/blob/main/news/2026-06-26.md
- 新浪 2026-09-08 的标题是"DeepSeek一口气扩招150人！0个AI研究岗"（只看到搜索结果标题，正文没读）：https://finance.sina.com.cn/tech/csj/2026-09-08/doc-iniraite6059201.shtml
- 没有找到数据标注、数据采购或供应商管理岗位的原文。建议手动看一下招聘页里数据相关的岗位。

**切入点**
- 最匹配的是难验证任务的专家评分标准（rubric）和"少而多样"的人工标注。V4 的思路就是少量人工标注加 rubric 引导的 RL，所以卖点是质量，不是量：金融、会计、法律专家写 rubric、给出带理由的标注。
- 白领专业任务：他们已经自建了覆盖 13 个行业的中文专业任务评测，并且靠人工盲评。可以提供更大的专业评测集和专家评审，比如财务结账、会计、法律。
- 新领域的专家模型：流程是"每个领域训一个专家再蒸馏"，加一个金融专家模型就需要带验证器的金融 RL 环境，Xitadel（交易）和财务结账环境直接对得上。交付可以按他们的沙箱格式来，DSec 对外是统一的 Python 接口。
- 数学证明：邵智宏做的 DeepSeekMath-V2 做的是自我验证的证明，可以谈 SimReal 的数学证明环境、验证器，以及人工证明评审。
- 代码 agent 的评测集他们用内部工程师自己做，软件工程不是优先切入点。

**风险**
- 自建倾向很强：团队小（媒体称公司约 170 人，二手），报告明确写要尽量少用人工标注，公开资料里看不到任何外部数据供应商。
- 很少对外发声，后训练的分工没有公开，联系人只能按论文和主页推断。
- 合规：DeepSeek 目前不在实体清单上，但据 CNBC 2026-06-17 报道，美国跨部门委员会已批准把它列入，白宫为避免贸易摩擦暂缓发布（搜索摘要）：https://www.cnbc.com/2026/06/17/us-deepseek-blacklist-cxmt-national-security-risks-.html 。2026-09-08 NSA、CISA、FBI 联合发布通报，点名 DeepSeek、Moonshot AI、阿里、MiniMax、阶跃星辰和 Z.ai（智谱）对美国前沿模型做工业级蒸馏（搜索摘要，通报页和 ExecutiveGov 报道一致）：https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a 、https://www.executivegov.com/articles/nsa-fbi-cisa-warn-china-ai-distillation-attacks 。这不是制裁或实体清单，但会加重美国籍专家和合作高校的顾虑。发送前请确认 SimReal 的主体、合作高校和美国籍专家参与是否受影响。
- 人员有流动（V4 报告里 10 人标了离职），但邵智宏和吴俣都没有标。

**核实说明**：2026-09-25 复核：邵智宏主页原文仍写 "I am a Research Scientist at DeepSeek"；2026 年没有查到离职报道。开头一句（V4 对难验证任务改用 rubric 引导的 RL 数据和生成式奖励模型、只需少量人工标注）除 GitHub 文本副本外，Fireworks 和 Kili 两篇独立文章的搜索摘要也能对上，保留不改。V4 技术报告的原始链接是 arXiv 2606.19348，GitHub 文本只作副本。补充：实体清单暂缓和 2026-09 蒸馏通报两条合规信息；DeepSeek Harness 桌面版预览在 2026-09-25 有报道（新浪，搜索摘要）：https://finance.sina.com.cn/tech/digi/2026-09-25/doc-iniszfcz4504743.shtml 。以下为原调研说明。邵智宏主页、V4 技术报告全文（GitHub 上的文本副本，页眉写着 arXiv:2606.19348v1）、deepseek-harness 和 deepseek-recipe 的 README 读的是原文。V4.1-Flash、吴俣的职务、离职去向和招聘信息来自搜索摘要或 GitHub 上的二手存档。

---

## 邮件

主题：SimReal｜DeepSeek 后训练专家数据

邵老师您好，

我是 SimReal（simreal.co）联合创始人[姓名]，我们为大模型后训练提供 RL 环境、验证器和专家数据。

Jane Street、Citadel 的从业者在支持我们的工作，每个环境上线前都做对抗测试，至今 400 次作弊攻击无一成功。

看到 V4 在难验证任务上改用 rubric 加少量人工标注，希望在 rubric 和专家标注上和贵司合作。想了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。我们可以先做小批量付费试点，质量高，价格有竞争力。

下周是否方便约 20 分钟聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

邵老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型后训练做 RL 环境、验证器和专家数据，Jane Street、Citadel 的从业者在支持我们，每个环境上线前都做对抗测试。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），我们可以先做小批量付费试点，质量高，价格有竞争力。您看下周方便约 20 分钟吗？
