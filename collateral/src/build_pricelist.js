const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType, LevelFormat, Footer, Header, PageNumber,
  TableLayoutType, VerticalAlign, TabStopType,
} = require("docx");

const INK = "111110", BODY = "33322F", MUTED = "6E6C66", RULE = "D9D6CF", ACCENT = "C2410C", HEAD = "111110", GROUP = "F2F0EB";
const FONT = { ascii: "Arial", hAnsi: "Arial", eastAsia: "Microsoft YaHei", cs: "Arial" };
const W = 9638; // A4 minus 2 × 1134

const r = (text, o = {}) => new TextRun({ text, font: FONT, color: o.color || BODY, bold: o.bold, size: o.size || 19 });
const para = (runs, o = {}) => new Paragraph({
  children: Array.isArray(runs) ? runs : [r(runs, o)],
  spacing: { before: o.before ?? 0, after: o.after ?? 100, line: o.line ?? 290 },
  alignment: o.align, keepNext: o.keepNext,
  border: o.rule ? { bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } } : undefined,
});
const section = (no, text) => para([r(no + "  ", { bold: true, size: 24, color: ACCENT }), r(text, { bold: true, size: 24, color: INK })], { before: 320, after: 140, rule: true, keepNext: true });
const bullet = (runs) => new Paragraph({ numbering: { reference: "dots", level: 0 }, children: Array.isArray(runs) ? runs : [r(runs)], spacing: { after: 70, line: 290 } });
const term = (title, text) => new Paragraph({ numbering: { reference: "terms", level: 0 }, children: [r(title + "：", { bold: true, color: INK }), r(text)], spacing: { after: 90, line: 290 } });

const thin = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const cell = (content, width, o = {}) => new TableCell({
  width: { size: width, type: WidthType.DXA },
  columnSpan: o.span,
  verticalAlign: VerticalAlign.CENTER,
  borders: o.borders || { top: thin, bottom: thin, left: none, right: none },
  shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
  margins: { top: 80, bottom: 80, left: 100, right: 100 },
  children: [new Paragraph({ alignment: o.align, spacing: { after: 0, line: 270 }, children: Array.isArray(content) ? content : [r(content, o.run || {})] })],
});

// ---------- Price table ----------
const COLS = [760, 2050, 2800, 1000, 1600, 1428];
const headRow = new TableRow({
  tableHeader: true, cantSplit: true,
  children: ["编号", "产品 / 服务", "规格说明", "计价单位", "参考单价（RMB）", "参考单价（USD）"].map((t, i) =>
    cell([r(t, { bold: true, color: "FFFFFF", size: 17 })], COLS[i], { fill: HEAD, borders: { top: none, bottom: none, left: none, right: none }, align: i >= 4 ? AlignmentType.RIGHT : undefined })),
});
const groupRow = (code, name, en) => new TableRow({
  cantSplit: true,
  children: [cell([r(code, { bold: true, color: ACCENT, size: 18 }), r("   " + name, { bold: true, color: INK, size: 18 }), r("   " + en, { color: MUTED, size: 16 })], W, { span: 6, fill: GROUP })],
});
const item = (code, name, spec, unit, rmb, usd) => new TableRow({
  cantSplit: true,
  children: [
    cell([r(code, { color: MUTED, size: 17 })], COLS[0]),
    cell([r(name, { bold: true, color: INK, size: 18 })], COLS[1]),
    cell([r(spec, { size: 17 })], COLS[2]),
    cell([r(unit, { size: 17 })], COLS[3]),
    cell([r(rmb, { size: 18, color: INK })], COLS[4], { align: AlignmentType.RIGHT }),
    cell([r(usd, { size: 18, color: INK })], COLS[5], { align: AlignmentType.RIGHT }),
  ],
});

const priceTable = new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: COLS, layout: TableLayoutType.FIXED,
  rows: [
    headRow,
    groupRow("A", "专家数据", "Expert Data"),
    item("A01", "专家 SFT 指令数据", "行业专家撰写的指令与高质量回答；金融、法律、医疗等领域", "条", "200 – 1,000", "30 – 150"),
    item("A02", "CoT / Reasoning 推理数据", "含完整推理步骤的解答，覆盖数学、代码、金融等，逐步校验", "条", "250 – 1,200", "40 – 180"),
    item("A03", "复杂 Query 构造", "真实场景、多约束的高难度问题，现有模型答不好", "题", "100 – 500", "20 – 80"),
    item("A04", "参考答案（Reference Answer）", "为难题撰写可核验的标准答案", "题", "100 – 600", "20 – 100"),
    item("A05", "RLHF 偏好数据", "专家对多个回答排序或二选一，附判断理由", "对", "50 – 400", "10 – 60"),
    item("A06", "Reward 打分数据", "按维度为回答打分，用于奖励模型训练与校准", "条", "20 – 150", "5 – 25"),
    item("A07", "代码 SFT / 调试数据", "需求到代码、报错定位与修复；附测试用例", "条", "200 – 1,000", "30 – 150"),
    groupRow("B", "Rubric 与评测", "Rubrics & Evaluation"),
    item("B01", "Rubric 设计", "可逐条检查的评分标准，含参考答案；上线前对抗测试", "题", "800 – 4,000", "120 – 600"),
    item("B02", "Rubric 逐项评分与质检", "按 Rubric 逐项打分，含抽检复核", "条回答", "30 – 150", "5 – 25"),
    item("B03", "LLM-as-a-Judge 校准数据", "专家逐项分数与理由，用于训练或校准评测模型", "条", "100 – 400", "15 – 60"),
    item("B04", "私有评测集 / Benchmark 定制", "200–1,000 题，含 Rubric、评分脚本与报告", "项目", "200,000 起", "30,000 起"),
    groupRow("C", "Agent 数据", "Agent Data"),
    item("C01", "Agent 长程轨迹", "专家实跑的完整 Session：多轮对话、30 次以上工具调用、中间过程全保留", "Session", "1,000 – 8,000", "150 – 1,200"),
    item("C02", "DeepResearch 数据", "研究题目、检索轨迹、引用来源与最终报告，配 Rubric", "题", "1,500 – 10,000", "250 – 1,500"),
    groupRow("D", "RL 训练环境", "RL Environments"),
    item("D01", "RL 任务（含验证器）", "可自动评分的训练任务，验证器经对抗测试", "任务", "2,000 – 12,000", "300 – 2,000"),
    item("D02", "终端任务（Terminal-Bench 类）", "命令行环境中的多步 Agent 任务，含测试与自动评分", "任务", "2,000 – 12,000", "300 – 2,000"),
    item("D03", "标准环境授权（非独家）", "交易、财务月结、软件工程、数学证明、逻辑推理、AI 研究、未来预测", "环境 / 季度", "300,000 起", "50,000 起"),
    item("D04", "企业定制环境", "围绕客户工作流搭建专属训练环境与验证器", "项目", "500,000 起", "80,000 起"),
    groupRow("E", "服务", "Services"),
    item("E01", "试点（Pilot）", "50–200 条样本，验证质量与流程", "项目", "20,000 – 100,000", "5,000 – 15,000"),
    item("E02", "持续训练服务", "模型每次升级后，回到环境继续训练与对比", "季度", "面议", "面议"),
    groupRow("F", "多模态与原始数据", "Multimodal & Raw Data"),
    item("F01", "多模态训练与评测数据", "图文、视频、音频的 SFT、偏好与评测数据", "条", "按量报价", "按量报价"),
    item("F02", "原始数据资源", "图片、视频、音频、文本及海外多语种原始数据，合规采集", "批次", "按量报价", "按量报价"),
  ],
});

// ---------- Document ----------
const logo = fs.readFileSync("img/simreal-logo-ink.png");
const children = [];

// Title block: logo left, document meta right
children.push(new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [4800, 4838], layout: TableLayoutType.FIXED,
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 4800, type: WidthType.DXA }, borders: { top: none, bottom: none, left: none, right: none }, verticalAlign: VerticalAlign.BOTTOM,
      children: [new Paragraph({ children: [new ImageRun({ type: "png", data: logo, transformation: { width: 150, height: 40 }, altText: { title: "SimReal", description: "SimReal logo", name: "logo" } })] })] }),
    new TableCell({ width: { size: 4838, type: WidthType.DXA }, borders: { top: none, bottom: none, left: none, right: none }, verticalAlign: VerticalAlign.BOTTOM,
      children: [
        new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 20 }, children: [r("报价单编号：SR-PL-2026-09", { size: 16, color: MUTED })] }),
        new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 20 }, children: [r("版本：V1.0　日期：2026 年 9 月", { size: 16, color: MUTED })] }),
        new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [r("有效期：自发出之日起 30 天", { size: 16, color: MUTED })] }),
      ] }),
  ] })],
}));
children.push(para([r("产品与服务报价单", { bold: true, size: 40, color: INK })], { before: 360, after: 40 }));
children.push(para([r("Products & Services Price List", { size: 20, color: MUTED })], { after: 200, rule: true }));

// About
children.push(section("01", "关于 SimReal"));
children.push(para("SimReal 为大模型公司和 AI 应用企业提供后训练所需的专家数据、评测体系和 RL 训练环境，帮助模型在金融、法律、医疗、代码等专业领域完成真实工作。"));
children.push(bullet([r("团队：", { bold: true, color: INK }), r("创始团队来自剑桥、LSE、杜克，具有 Jane Street、Citadel、D. E. Shaw、Millennium、Optiver 从业经历。")]));
children.push(bullet([r("专家网络：", { bold: true, color: INK }), r("7,000+ 行业专家已报名，通过 21 所合作高校可触达 20 万+ 专业人士。")]));
children.push(bullet([r("质量：", { bold: true, color: INK }), r("评分标准与验证器上线前均经对抗测试；旗舰交易环境 Xitadel 使开源模型交易表现提升 12%。")]));

// Price list
children.push(section("02", "报价清单"));
children.push(para([r("以下为参考单价区间。具体单价按领域、难度、数据格式、数量与交付周期确定，以双方确认的需求说明书（SOW）为准。", { size: 17, color: MUTED })], { after: 140 }));
children.push(priceTable);

// Terms
children.push(section("03", "商务条款"));
children.push(term("报价有效期", "自本报价单发出之日起 30 天。"));
children.push(term("计价与起订", "按条、题、Session、任务或项目计价；首次合作建议从试点开始，试点费用可协商抵扣后续合同。"));
children.push(term("付款方式", "签约后预付 50%，交付验收后支付余款；长期合同可按月或按季度结算。"));
children.push(term("交付与验收", "按批次交付，格式可按客户要求（如 JSONL）；客户收到后 5 个工作日内完成抽检，抽检合格率不低于 95%，不合格部分免费返工。"));
children.push(term("独家与加急", "独家交付、加急交付另行报价。"));
children.push(term("数据权属与保密", "交付数据的使用权归客户，独家交付时知识产权一并转让；双方签署保密协议，专家个人信息脱敏处理。"));
children.push(term("合作方价格", "渠道与交付合作方可享合作价，具体比例按合作协议约定。"));
children.push(term("税费与发票", "以合同约定为准。"));

// Contact
children.push(section("04", "联系方式"));
children.push(new Paragraph({ spacing: { after: 60 }, children: [r("商务合作　", { color: MUTED }), r("business@simreal.co", { bold: true, color: INK })] }));
children.push(new Paragraph({ spacing: { after: 60 }, children: [r("官方网站　", { color: MUTED }), r("simreal.co", { bold: true, color: INK })] }));

const doc = new Document({
  creator: "SimReal",
  title: "SimReal 产品与服务报价单",
  styles: { default: { document: { run: { font: FONT, size: 19, color: BODY } } } },
  numbering: { config: [
    { reference: "dots", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } }, run: { color: ACCENT } } }] },
    { reference: "terms", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 380, hanging: 320 } }, run: { color: ACCENT, bold: true } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: W }],
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 } },
      children: [r("SimReal · 产品与服务报价单 · 保密", { size: 15, color: MUTED }), new TextRun({ text: "\t", font: FONT }), new TextRun({ children: ["第 ", PageNumber.CURRENT, " 页"], font: FONT, size: 15, color: MUTED })],
    })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync("SimReal-产品与服务报价单.docx", buf); console.log("ok", buf.length); });
