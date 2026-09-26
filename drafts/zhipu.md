# 智谱 Z.ai

- 类别：国内大模型公司｜地区：国内（北京）
- 收件人：**吕鑫（Xin Lv）**，智谱 O Team 负责人，方向是推理 RL、RL 基础设施和 Agentic RL；团队维护开源 RL 框架 slime
- 置信度：高。本人主页写明："I lead the O Team focusing on Reasoning RL, RL infra and Agentic RL for the GLM model family"（已读原文，主页最后更新于 2025-11）。2026-02 发布的 GLM-5 技术报告里他是第二作者；slime 的 README 写明它支撑了 GLM-4.5 到 GLM-5.3 的训练（已读原文）。
- 来源：
  - 本人主页：https://davidlvxin.github.io/ （源文件 https://github.com/davidlvxin/davidlvxin.github.io/blob/master/_pages/about.md ）
  - 中文名：Google Scholar 显示为 "Xin Lv (吕鑫)"：https://scholar.google.com/citations?user=rJzgbYQAAAAJ
  - slime：https://github.com/THUDM/slime
- 备选：
  - **曾奥涵（Aohan Zeng）**，GLM-5 第一作者；有媒体称他为"智谱 GLM 基座模型 & 训练基础设施负责人"（搜索摘要，头衔未核实）：https://cloud.tencent.com/developer/article/2644244
  - **唐杰**，首席科学家（创始人级别，只作为兜底）
- 数据 / 标注 / 数据采购负责人：**未找到**。
- 称呼用"吕老师"：他在学术圈活跃，这个称呼比较常见。

## 调研备注

**最近发布**
- **GLM-5.3**（2026-08）：README 写明它和 GLM-5.2 用同一个基座，"every gain comes from post-training"，Z.ai Code Bench 比 GLM-5.2 提升 50%，CyberGym 达到 SOTA（已读原文）：https://github.com/zai-org/GLM-5
- **GLM-5.2**（2026-06）：Terminal-Bench 2.1 从 62.0 提到 81.0，SWE-bench Pro 从 58.4 提到 62.1（同上）。
- **GLM-5 技术报告**（2026-02）：用异步 RL 框架 slime，阶段是 SFT → Reasoning RL → Agentic RL → General RL：https://arxiv.org/abs/2602.15763 。据二手解读，报告里有约 1 万个可验证环境，并用"高质量人类专家回答"作锚点来改善文风（搜索摘要）：https://www.53ai.com/news/OpenSourceLLM/2026022239486.html
- 下一步是 GLM-6 的"完全自训练"方向（2026-08-31 业绩会，搜索摘要）：https://news.qq.com/rain/a/20260831A0CDGI00 。2026-09 报道募资约 50 亿美元，主要用于下一代模型（搜索摘要）：https://www.21jingji.com/article/20260913/herald/f91335df96ad595e331836c1efb7ea8f.html
- 2026-01-08 在港股上市（2513.HK）。招股书在本环境打不开，二手资料只提到供应商里有"研发支持提供商（如数据清洗及大模型评估服务）"，没有披露标注支出或供应商名称。另外据报道在推进科创板上市，招股书会披露前五大供应商，值得留意。

**JD 里的数据需求**（飞书招聘页在本环境打不开，以下是搜索摘要，发布时间是按岗位 ID 推断的）
- AI院-GLM后训练团队-算法工程师（社招，约 2025-06）：构建和优化数学、代码、复杂推理等能力方向的对齐数据。https://zhipu-ai.jobs.feishu.cn/index/position/7511570084462283017/detail
- GLM团队-后训练算法工程师（26 届校招）：https://zhipu-ai.jobs.feishu.cn/zhipucampus/m/position/detail/7539833581066586378
- 2026 日常实习："研究Agent长程任务能力、基于强化学习的Agent能力提升及训练数据构建"：https://www.wondercv.com/xiaozhao/zhipu-ai-2026-spring-recruitment-beijing-5959-d0d523/
- 没有找到数据采购或供应商管理岗位。

**切入点**
- 编程以外的长程可验证环境：他们的 RL 规模已经上去了，但环境集中在代码和终端任务，而财务结账、交易（Xitadel）、预测都是新领域的长程任务。
- General RL 阶段需要专家 SFT 和偏好数据，可以用金融、法律、医疗专家的回答作锚点。
- 评分标准和评测集。
- 如果走"完全自训练"，对验证器的需求会增加，对静态数据的需求会减少。

**风险**
- **合规**：智谱在 2025-01-16 被列入美国商务部实体清单：https://www.federalregister.gov/documents/2025/01/16/2025-00704/addition-of-entities-to-and-revision-of-entry-on-the-entity-list 。发送前请确认 SimReal 的主体、合作高校和美国籍专家参与是否受影响。
- 自建倾向强：slime 是自研框架，环境也是自建的，路线图往自训练走。
- 研发预算主要花在算力上；收入以 MaaS 为主（2026 上半年约 86.5%，搜索摘要），行业定制的优先级在下降。

**核实说明**：主页、slime README、GLM-5 README 和实体清单读的是原文，其余来自搜索摘要。

---

## 邮件

主题：SimReal｜智谱 后训练专家数据

吕老师您好，

我是 SimReal（simreal.co）联合创始人[姓名]，我们为大模型后训练提供 RL 环境、验证器和专家数据。

Jane Street、Citadel 的从业者在支持我们的工作，每个环境上线前都做对抗测试，至今 400 次作弊攻击无一成功。

看到 GLM-5.3 只靠后训练把内部代码评测提升了 50%，希望在编程以外的环境和专家数据上和贵司合作。想了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。我们可以先做小批量付费试点，质量高，价格有竞争力。

下周是否方便约 20 分钟聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]

---

## 微信版（引荐后）

吕老师您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型后训练做 RL 环境、验证器和专家数据，Jane Street、Citadel 的从业者在支持我们，每个环境上线前都做对抗测试。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），我们可以先做小批量付费试点，质量高，价格有竞争力。您看下周方便约 20 分钟吗？
