# SimReal 客户外联

第一批客户外联：名单和草稿。所有草稿由人工审核后自己发送，本仓库不发送任何消息。

## 审批页

https://claude.ai/artifact/WCBiAySyzEqAHkJ2YkbUj2 （私有，只有你能打开）

每家一张卡片：批准，或者退回修改并写一句原因。退回的由 Claude 修改后放回待审。页面上方的「发件信息」填一次，复制邮件时会自动替换署名、微信/电话，以及身份核验那句（三选一：保留方括号 / 使用 / 删掉）。

- 页面源码：`approval/index.html`
- 页面数据由 `tools/build_db.py` 从 `prospects.csv` 和 `drafts/` 生成，写进页面的数据库（`prospects/<slug>`）。审批状态只存在页面数据库里。
- 模板在 `ops/templates.md`（第 2 版：一句自我介绍、一句背书、合作意向和需求）。`tools/render_drafts.py` 按模板生成邮件，`tools/check_drafts.py` 逐封核对，只允许称呼、公司名和合作那句不同。

## 市场情报：RL 数据买方地图

https://claude.ai/artifact/WrAr9qDnxYctaMi8KRLrjE （私有）

RL 环境、人类数据、专家网络、评测类公司公开点名过的客户和合作方，按买方反向索引，每条都附原文证据和来源链接。调研说明见 `ops/intel-brief.md`。

- `intel/<分段>-claims.csv`、`intel/<分段>-vendors.csv`、`intel/<分段>-notes.md`：四个分段（海外大中型、海外 RL 初创、国内、买方视角）的原始结果
- `intel/claims.csv`、`intel/vendors.csv`、`intel/buyers.md`：`tools/intel_merge.py` 合并去重后的结果和买方索引
- `intel/page/`：页面模板和生成结果，`tools/build_intel_page.py` 重建
- `intel/candidates.json`：从买方索引里挑出的候选新客户，在审批页「候选新客户」里决定是否加入外联
- 投资人：`intel/vc-funds.csv`（112 家机构和天使）、`intel/vc-deals.csv`（110 笔交易），由 `tools/vc_merge.py` 从 `intel/vc-overseas-*`、`intel/vc-china-*` 合并；优先接触名单在 `intel/vc-priority.json`，页面上是「投资人」区块。调研说明见 `ops/vc-brief.md`

## 文件

- `prospects.csv`：名单。列：公司、类别、地区、联系人、职位、来源链接、切入点、置信度。UTF-8（带 BOM，Excel 可直接打开）。
- `drafts/`：每家一个文件。海外公司是英文邮件，国内公司是中文邮件加微信版。每个文件开头是调研备注：联系人和备选、最近发布、招聘 JD 信号、切入点、风险，每条都附来源链接。

## 约定

- **置信度**：指联系人是否确实负责该方向、而且目前仍在职。
  - 高：公司官网、官方公告或本人近期公开发言写明了职责。
  - 中：权威媒体报道或技术报告署名可以推断。
  - 低：信息间接或可能过时。
- 联系人只用公开职业信息。查不到写"未找到"；这时 CSV 里填的是备选联系人（通常是创始人或 CTO），并注明"备选"。
- 模板里只改称呼、公司名和合作那句。以下几处方括号保持原样，由你决定：
  - `[Your name]` / `[姓名]`：发件人姓名
  - `微信/电话：[ ]`
  - `[介绍人]`
- 不提融资、TS、投资方；不放 GitHub 链接。

## 名单

✅ = 草稿已上审批页（31 家都已核实一遍，见 `ops/verify-*.md`）。审批状态以审批页为准。

### 海外（16）

| 公司 | 类别 | 状态 |
|---|---|---|
| Reflection AI | frontier lab | ✅ |
| Thinking Machines Lab | frontier lab | ✅ |
| Mistral AI | frontier lab | ✅ |
| OpenAI | frontier lab | ✅ |
| Anthropic | frontier lab | ✅ |
| Google DeepMind | frontier lab | ✅ |
| Meta Superintelligence Labs | frontier lab | ✅ |
| xAI | frontier lab | ✅ |
| Scale AI | 人类数据供应商 | ✅ |
| Surge AI | 人类数据供应商 | ✅ |
| Mercor | 人类数据供应商 | ✅ |
| Harvey | 垂直 AI（法律） | ✅ |
| OpenEvidence | 垂直 AI（医疗） | ✅ |
| Rogo | 垂直 AI（金融） | ✅ |
| Balyasny Asset Management（Applied AI） | 金融机构 AI 团队 | ✅ |
| McKinsey（QuantumBlack） | 咨询公司 AI 团队 | ✅ |

### 国内（15）

| 公司 | 类别 | 状态 |
|---|---|---|
| 月之暗面 Moonshot AI | 国内大模型公司 | ✅ |
| 智谱 Z.ai | 国内大模型公司 | ✅ |
| DeepSeek | 国内大模型公司 | ✅ |
| 阿里巴巴 通义千问 | 国内大模型公司 | ✅ |
| 字节跳动 Seed | 国内大模型公司 | ✅ |
| MiniMax | 国内大模型公司 | ✅ |
| 阶跃星辰 | 国内大模型公司 | ✅ |
| 腾讯混元 | 国内大模型公司 | ✅ |
| 海天瑞声 | 人类数据供应商 | ✅ |
| 数据堂 | 人类数据供应商 | ✅ |
| 百川智能 | 垂直 AI（医疗） | ✅ |
| 幂律智能 | 垂直 AI（法律） | ✅ |
| 恒生电子 | 垂直 AI（金融） | ✅ |
| 九坤投资（AI Lab） | 金融机构 AI 团队 | ✅ |
| 中国平安 | 金融机构 AI 团队 | ✅ |
