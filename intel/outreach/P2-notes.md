# P2（partner）调研说明

调研日期：2026-09-27。共用约 100 次 WebSearch。官网、arXiv 和新闻站基本都被网络策略拦截，只有 GitHub raw 能直接读原文，所以大部分证据来自搜索摘要，置信度也相应偏保守。

## 数量
- 共 36 行：种子名单保留 31 家，自行补充 5 家。
- 有公开邮箱的 7 家：HUD（founders@）、Collinear（CEO 本人）、Halluminate（CEO 本人）、Vals AI（CEO 本人）、Andon Labs（founders@）、hillclimb（founders@）、Good Start Labs（CEO 本人）。
  - Collinear、Halluminate、HUD 的邮箱写在官方 GitHub README 里，已读原文。
  - 其余几家的邮箱只在搜索摘要里看到，出处是论文作者邮箱、YC Launch 页或官方隐私声明，发送前建议再点开来源确认一次。
- 置信度：高 2，中 25，低 9。
- 另有 5 家只有官网公开的通用邮箱，已放在“备用渠道”：Prime Intellect、Mechanize、General Reasoning、Gray Swan、Patronus。其余多数只有官网联系页、官网或 YC 公司页。

## 剔除（4 家，未写入 CSV）
- **Adaptive ML**：2026-06-30 被 Datadog 收购，并入 Datadog AI Research，不再对外卖服务。
- **Haize Labs**：2026-09-17 被 Beacon 收购，CEO Leonard Tang 转任 Beacon 的 VP of AI Research。
- **Virtue AI**：2026-08-17 被 Fortinet 收购。
- **Deeptune**：2026-07-09 被 Mercor 收购，CEO Tim Lupo 加入 Mercor。Mercor 在 P1 分段，由那边负责联系。

## 自行补充（5 家，2025–2026 年成立，公开表示为前沿实验室做 RL 环境或专家评测）
- **Perit.AI**（YC F26）：专家网络，把医生、律师、银行家等变成任务、rubric 和 RL 环境；自称客户包括 Amazon AGI。它和我们在供给侧直接重叠。
- **Polymath**（YC W26）：生成模拟公司类环境，发布了 Horizon-SWE。
- **Haladir**（YC W26）：基于求解器的 RL 环境，主业是物流。
- **CoArena**（YC S26）：免费的 computer-use 对战榜，底下是付费数据业务。
- **idler**（YC S25，2025 年成立）：2026-08 获 Paradigm 领投的 900 万美元种子轮，卖现成的评测和环境数据集，含法律、战略运营等方向。
- 考虑过但未收录：Abundant、Antim Labs、dmodel 都是 2024 年成立，不符合“2025–2026 新成立”；Enact、Fern 做机器人物理环境，与我们不匹配；Sepal AI 已被 Mercor 收购。

## 需要创始人注意的事
1. **刚融到钱，最可能有预算：**
   - Prime Intellect：2026-07 A 轮 1.3 亿美元，估值 10 亿美元。
   - Bespoke Labs：累计 4000 万美元，Wing 领投。
   - Patronus：2026-06 B 轮 5000 万美元，同时推出 Digital World Models 和 RL Environments 产品线。
   - Vals AI：2026-08 A 轮 4000 万美元，a16z 领投。
   - Gray Swan：2026-05 A 轮 4000 万美元。
   - Fleet：据报道 A 轮 4500 万美元，估值 7.25 亿美元。
   - Arga Labs：2026-08 种子轮 1000 万美元。
   - idler：2026-08 种子轮 900 万美元。
2. **Mechanize 换了掌舵人。** Google 与 Mechanize 的人才加授权交易已在 9 月完成，Tamay Besiroglu 和十余名员工加入 DeepMind。公司由原 chief of staff Guive Assadi 任 CEO 继续经营，前景不明。它可能正缺供给能力，也可能不再采购。
3. **Irregular 舆论敏感。** 2026 年 8–9 月，它的网络安全评测沙箱外泄，牵连 OpenAI、Anthropic、Meta、Google（CNBC、Forbes 均有报道）。邮件里不要提这件事。
4. **Halluminate 与我们直接竞争。** 它 2026 年专做投行、PE、咨询方向的 RL 环境，建议只谈专家供给。
5. **供给侧重叠。** Huzzle Labs、Perit.AI、hillclimb 都有自己的专家网络，合作更可能是互补领域（金融、量化）的分包。
6. **联系人缺口：**
   - Matrices、Preference Model：没查到创始人姓名。
   - Arena、Prime Intellect：没查到合作或 BD 负责人，“备选联系人”里给的是 CEO 或 CMO。
   - Habitat：没有官网，也没有任何联系渠道。
   - Exabite（原 Calaveras，已改名）：联系人的职位未核实。
7. **置信度判断。** 联系人职位大多出自 LinkedIn 或第三方目录的搜索摘要，按规则这类来源不能单独评为“高”。只有 HUD（CEO 本人演讲加官方 README）和 Collinear（官网 about 页加官方 README 邮箱）评为“高”。
