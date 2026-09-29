# 报价 Benchmark（内部参考，不对外）

对外材料里只放我们自己的参考报价（`collateral/SimReal-公司简介与参考报价.docx` 第四节）。下面是定价时参考的公开市场价和推算方法。

## 公开市场价

| 品类 | 公开区间 | 来源 | 可信度 |
|---|---|---|---|
| RL 任务（含验证器） | 每任务 $200–2,000；复杂软件工程任务可达 $20,000 | Epoch AI | 高 |
| 独家 vs 非独家 | 独家约为非独家的 4–5 倍 | Epoch AI | 高 |
| 界面复刻环境 | 网站复刻约 $20,000/个；Slack 级复杂产品约 $300,000 | Epoch AI、SemiAnalysis | 中高 |
| 实验室合同规模 | 每季度六到七位数美元，常见 $30 万–100 万以上 | Epoch AI | 高 |
| 单任务训练算力 | 约 $2,400/任务 | Mechanize | 中（估算） |
| 专家时薪（付给专家） | Mercor 平均约 $85/时；律师 $55–150+；医生 $110–250；金融 $60–250 | Mercor 官网及第三方 | 中 |
| 平台加价 | 约 30–35%，专家拿到客户付款的 60–70% | 第三方估算 | 中低 |
| 专家小时（向客户收） | Surge 约 $85–200+/专家小时；专家撰写任务 $200–2,000/个；企业合同 $5–6 万/年起 | 第三方评测站 | 中低 |
| SFT 示范数据 | 通用 $0.1–1/条；研究生级专家题约 $58/题（约 35 分钟） | 行业博客 | 中低 |
| 偏好数据 | 通用 $0.5–5/条；专家对比可达约 $100/对 | 行业博客 | 中低 |
| 私有评测 | 平台订阅 $249–10,000/月；定制项目 $12.5 万–82 万/年 | AI Superior | 低 |
| 合成 Agent 轨迹 | 纯模型生成 $0.3–0.6/条（只算算力） | AgentTrek、Explorer 等论文 | 高 |
| 国内通用文本标注 | 0.05–0.5 元/条 | 标注公司公开报价 | 中 |
| 国内专家数据 | 奥赛级数学题 1,000 道约 20 万元；一般 150–800 元/条 | 整数智能 | 中 |
| 国内专家时薪 | 字节 Xpert 100–500 元/时；高端 800–1,000 元/时 | 媒体报道 | 中 |

## 我们的报价怎么推

单价 ≈ 专家时薪 × 单条工时 × 1.3–1.5（质检与管理）× 1.5–2（毛利与风险）

- 海外：金融专家 $120/时，每条 30 分钟，成本 $60；加质检管理约 $84；报价约 $130–170/条。
- 国内：金融专家 300 元/时，每条 30 分钟，成本 150 元；加质检管理约 210 元；报价约 320–420 元/条。
- 独家按非独家的 4–5 倍报。

## 来源

- Epoch AI：An FAQ on Reinforcement Learning Environments — https://epoch.ai/gradient-updates/state-of-rl-envs
- SemiAnalysis：RL Environments and RL for Science — https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science
- Mechanize：Cheap RL tasks will waste compute — https://www.mechanize.work/blog/cheap-rl-tasks-will-waste-compute/
- Mercor：AI Trainer Salary — https://www.mercor.com/resources/experts/ai-trainer-salary-hourly-rates/
- Mercor：律师专家页 — https://www.mercor.com/experts/lawyers/
- ValueAdd VC：Mercor 收入与抽成分析 — https://valueaddvc.com/blog/how-does-mercor-make-money-2b-arr-20b-valuation-and-the-expert-data-marketplace-explained
- HeroHunt：Top 10 Data Annotators for AI Labs (2026) — https://www.herohunt.ai/blog/top-10-data-annotators-for-ai-labs-2026-benchmark/
- Olostep：AI Training Data Providers — https://www.olostep.com/blog/ai-training-data-providers
- Digital Divide Data：RLHF Services — https://www.digitaldividedata.com/blog/rlhf-services-end-to-end-provider
- AI Superior：Cost of Private LLM Evaluation Services in 2026 — https://aisuperior.com/cost-of-private-llm-evaluation-services/
- AgentTrek — https://agenttrek.github.io/
- 整数智能：当老板问起 LLM 的落地，数据要花多少钱 — https://www.molardata.com/article/LLMluodideshujuchengben
- 曼孚科技：数据标注服务收费标准 — https://www.mindflow.com.cn/NewsStd_1177.html
- 新浪科技：时薪冲上 400 元 — https://finance.sina.com.cn/tech/roll/2025-12-16/doc-inhaxefx3811644.shtml
- 投资界：深扒 151 份 JD — https://news.pedaily.cn/202606/564988.shtml
