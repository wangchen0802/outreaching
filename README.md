# SimReal 外联

三类外联：渠道伙伴（第一步）、投资人、客户。草稿由你批准后，从 business@simreal.co 自己发送；本仓库和 Claude 不发送任何消息。

## 审批页

https://claude.ai/artifact/WCBiAySyzEqAHkJ2YkbUj2 （私有，只有你能打开）

三个标签：渠道伙伴 112 家、投资人 147 家、客户 98 家。每张卡片：
1. 批准，或退回修改写一句原因（Claude 每天 01:13 UTC 处理退回的卡片）。
2. 批准后点「在 Gmail 打开第 1 封」：收件人、主题、正文都已填好，从发件邮箱发出后点「标记已发送」。
3. 跟进邮件（渠道和客户第 4、10 天，投资人第 5、12 天）到期后出现在「今天要发」里。对方回复了点「对方已回复」，序列停止。
4. 没有公开邮箱的，卡片上有「自己查到的邮箱」输入框，填了就用它发；也可以按「备用渠道」走官网表单。
5. 每一栏「待发送」可以导出 CSV，用 Gmail 邮件合并工具批量发。新邮箱建议每天不超过 30 封，先配好 SPF / DKIM / DMARC。

- 页面源码：`approval/index.html`；数据在页面数据库 `prospects/<id>`（渠道 `p-`、投资人 `v-`、客户无前缀）。
- 模板：`ops/templates.md`（第 3 版，三类各有首封、两封跟进、短消息/微信版）。
- 名单：`lists/partners.csv`、`lists/investors.csv`、`prospects.csv`（客户）。调研原始行在 `intel/outreach/<分段>.csv`，说明在同名 `-notes.md`，调研要求见 `ops/outreach-brief.md`。
- 工具：`tools/build_outreach.py`（调研行 → 名单和草稿）、`tools/render_drafts.py`（按模板重新生成）、`tools/check_drafts.py`（逐封核对模板和禁用词）、`tools/build_db.py`（草稿 → 页面数据）。
- 投资人发送顺序沿用之前那版投资人标签定的分批（`intel/outreach/investor-waves.json`）：第 1 批先热身，第 3 批最重要、最后发，暂缓的排最后。

## 约定

- 联系人和邮箱只用公开信息，每条附来源。个人邮箱只收本人或雇主公开发布的；查不到写"未找到"，不猜邮箱格式，不用数据经纪网站。
- 专家数量写"7,000+ 已报名，可触达 20 万+ 专业人士"，不写"20 万已验证专家"。
- 渠道伙伴和投资人邮件写 Surge AI、AfterQuery 合作和正在融资；客户邮件不写（避免和渠道伙伴撞单）。不放 GitHub 链接。

## 市场情报：RL 数据买方地图

https://claude.ai/artifact/WrAr9qDnxYctaMi8KRLrjE （私有）

RL 环境、人类数据、专家网络、评测类公司公开点名过的客户和合作方，按买方反向索引，每条都附原文证据和来源链接。调研说明见 `ops/intel-brief.md`。

- `intel/<分段>-claims.csv`、`intel/<分段>-vendors.csv`、`intel/<分段>-notes.md`：四个分段（海外大中型、海外 RL 初创、国内、买方视角）的原始结果
- `intel/claims.csv`、`intel/vendors.csv`、`intel/buyers.md`：`tools/intel_merge.py` 合并去重后的结果和买方索引
- `intel/page/`：页面模板和生成结果，`tools/build_intel_page.py` 重建
- `intel/candidates.json`：从买方索引里挑出的候选新客户，在审批页「候选新客户」里决定是否加入外联
- 投资人：`intel/vc-funds.csv`（112 家机构和天使）、`intel/vc-deals.csv`（110 笔交易），由 `tools/vc_merge.py` 从 `intel/vc-overseas-*`、`intel/vc-china-*` 合并；优先接触名单在 `intel/vc-priority.json`，页面上是「投资人」区块。调研说明见 `ops/vc-brief.md`

## Duke 校友投资人

Duke 毕业满 8 年（2018 年及以前拿到 Duke 学位）、2026 年在天使到 A 轮投资机构做决策、或自己写天使/种子支票的人，共 71 位（高匹配 12、中 30、低 29），另有 58 位查过但不符合，原因都写了。

- 名单：`lists/duke-alumni-investors.csv`（全部字段和来源）、`lists/duke-alumni-investors.md`（可读版）、`collateral/SimReal-Duke-alumni-investors.pdf`（打印版）
- 每人有简介、Duke 学位和年份、阶段、相关投资、一句开场钩子、联系方式。个人邮箱只有 8 位是本人或机构公开发布的，其余给机构官方投递渠道（BP 邮箱或表单）、LinkedIn、X。仍然不猜邮箱格式、不用数据经纪网站。
- 「Worth a manual check」里 3 位强匹配人选只差一个公开事实（如 Fuqua 毕业年份），可以让 Amaris 在 Duke 校友目录里查。
- 调研原始结果在 `intel/outreach/duke/`（discovery、verify、recheck、email、edit 各轮），`tools/build_duke_list.py` 合并生成名单，`tools/build_duke_pdf.py` 生成 PDF。

## Duke 学生可用的资金和创业支持

Amaris 是 Duke 在读本科生，下面这些资源都是因为她能拿到的。共 121 项、47 位联系人，按四类整理：Duke 校内项目、Duke 校友网络和学生基金、Research Triangle / 北卡 / 联邦资助、面向学生创始人的全国项目和比赛。

- `collateral/SimReal-Duke-funding-and-support.pdf`：开头是关键日期和「Start here」（高匹配、我们符合条件、开放或即将开放），后面每项写了能拿到什么、资格、时间、申请方式和联系人。
- `lists/duke-funding-and-support.csv`（每项一行）、`lists/duke-contacts.csv`（联系人，邮箱只收官方公开的）。
- 两条硬门槛：北卡的 NC IDEA 等要求公司总部在北卡；联邦 SBIR/STTR 要求美国公司且 50% 以上股份由美国公民或绿卡持有人持有。
- 原始调研在 `intel/resources/duke/`，`tools/build_duke_support.py` 重建。

## Duke 校友目录私信（Amaris 发送）

给名单上每位 Duke 校友投资人写好的校友目录表单内容，共 74 条（71 位 + 3 位待核实毕业年份）。

- `collateral/SimReal-Duke-alumni-messages.pdf`：每人一块，写明要勾的选项、第 3 栏「为什么联系你」的个性化内容和发送备注；第 2 栏自我介绍所有人相同，只换名字。
- `lists/duke-alumni-messages.csv`：同样内容，第 2 栏已按人填好名字，方便复制。
- SimReal 的事实只用 Charles 投资人邮件里的说法；校友的事实只用名单里核实过的。Duke 网站条款禁止未经请求的商业推销，所以每条都是向校友请教融资建议和引荐，不是硬推销。
- `tools/build_duke_messages.py` 重建；原始文案在 `intel/outreach/duke/messages/`。
