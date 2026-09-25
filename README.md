# SimReal 客户外联

第一批客户外联：名单和草稿。所有草稿由人工审核后自己发送，本仓库不发送任何消息。

## 文件

- `prospects.csv`：名单。列：公司、类别、地区、联系人、职位、来源链接、切入点、置信度。UTF-8（带 BOM，Excel 可直接打开）。
- `drafts/`：每家一个文件。海外公司是英文邮件，国内公司是中文邮件加微信版。每个文件开头是调研备注：联系人和备选、最近发布、招聘 JD 信号、切入点、风险，每条都附来源链接。

## 约定

- **置信度**：指联系人是否确实负责该方向、而且目前仍在职。
  - 高：公司官网、官方公告或本人近期公开发言写明了职责。
  - 中：权威媒体报道或技术报告署名可以推断。
  - 低：信息间接或可能过时。
- 联系人只用公开职业信息。查不到写"未找到"；这时 CSV 里填的是备选联系人（通常是创始人或 CTO），并注明"备选"。
- 模板里只改开头那句和方括号里的内容。以下几处方括号保持原样，由你决定：
  - `[Your name]` / `[姓名]`：发件人姓名
  - 身份与资质核验那句：`[, and every expert is ID- and credential-checked before starting work]` 和 `[，所有专家上岗前均完成身份与资质核验]`
  - `微信/电话：[ ]`
  - `[介绍人]`
- 不提融资、TS、投资方；不放 GitHub 链接。

## 名单（拟定，待确认）

第一批 5 家已完成（✅），其余待你确认风格后再调研。名单本身也可以调整。

### 海外（16）

| 公司 | 类别 | 状态 |
|---|---|---|
| Reflection AI | frontier lab | ✅ |
| Thinking Machines Lab | frontier lab | ✅ |
| Mistral AI | frontier lab | ✅ |
| OpenAI | frontier lab | |
| Anthropic | frontier lab | |
| Google DeepMind | frontier lab | |
| Meta Superintelligence Labs | frontier lab | |
| xAI | frontier lab | |
| Scale AI | 人类数据供应商 | |
| Surge AI | 人类数据供应商 | |
| Mercor | 人类数据供应商 | |
| Harvey | 垂直 AI（法律） | |
| OpenEvidence | 垂直 AI（医疗） | |
| Rogo | 垂直 AI（金融） | |
| Balyasny Asset Management（Applied AI） | 金融机构 AI 团队 | |
| McKinsey（QuantumBlack） | 咨询公司 AI 团队 | |

### 国内（15）

| 公司 | 类别 | 状态 |
|---|---|---|
| 月之暗面 Moonshot AI | 国内大模型公司 | ✅ |
| 智谱 Z.ai | 国内大模型公司 | ✅ |
| DeepSeek | 国内大模型公司 | |
| 阿里巴巴 通义千问 | 国内大模型公司 | |
| 字节跳动 Seed | 国内大模型公司 | |
| MiniMax | 国内大模型公司 | |
| 阶跃星辰 | 国内大模型公司 | |
| 腾讯混元 | 国内大模型公司 | |
| 海天瑞声 | 人类数据供应商 | |
| 数据堂 | 人类数据供应商 | |
| 百川智能 | 垂直 AI（医疗） | |
| 幂律智能 | 垂直 AI（法律） | |
| 恒生电子 | 垂直 AI（金融） | |
| 九坤投资（AI Lab） | 金融机构 AI 团队 | |
| 中国平安 | 金融机构 AI 团队 | |
