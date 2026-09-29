const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, HeadingLevel, BorderStyle, ShadingType, LevelFormat, ExternalHyperlink,
  Footer, PageNumber, TableLayoutType,
} = require("docx");

const INK = "111110", BODY = "33322F", MUTED = "6E6C66", RULE = "D9D6CF", ACCENT = "C2410C", TINT = "F6EEE8", HEAD = "F2F0EB";
const FONT = { ascii: "Arial", hAnsi: "Arial", eastAsia: "Microsoft YaHei", cs: "Arial" };
const CONTENT_W = 9638; // A4 width 11906 minus 2 × 1134 margins

const r = (text, o = {}) => new TextRun({ text, font: FONT, color: o.color || BODY, bold: o.bold, size: o.size || 20, italics: o.italics });
const p = (runs, o = {}) => new Paragraph({
  children: Array.isArray(runs) ? runs : [r(runs, o)],
  spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 300 },
  alignment: o.align,
  keepNext: o.keepNext,
});
const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text, font: FONT, color: INK, bold: true, size: 30 })],
  spacing: { before: 360, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 4 } },
  keepNext: true,
});
const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text, font: FONT, color: INK, bold: true, size: 24 })],
  spacing: { before: 240, after: 100 },
  keepNext: true,
});
const bullet = (runs) => new Paragraph({
  numbering: { reference: "dots", level: 0 },
  children: Array.isArray(runs) ? runs : [r(runs)],
  spacing: { after: 80, line: 300 },
});
const step = (runs) => new Paragraph({
  numbering: { reference: "steps", level: 0 },
  children: Array.isArray(runs) ? runs : [r(runs)],
  spacing: { after: 80, line: 300 },
});
const note = (text) => p([r(text, { color: MUTED, size: 17 })], { after: 120 });

const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const borders = { top: border, bottom: border, left: border, right: border };
function table(widths, rows, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0,
      cantSplit: true,
      children: cells.map((c, ci) => {
        const isHead = ri === 0;
        const runs = (Array.isArray(c) ? c : [c]).map((t) => typeof t === "string"
          ? r(t, { bold: isHead || (o.boldFirst && ci === 0), color: isHead ? INK : (o.accentCol === ci ? ACCENT : BODY), size: isHead ? 18 : 18 })
          : t);
        return new TableCell({
          borders,
          width: { size: widths[ci], type: WidthType.DXA },
          shading: isHead ? { fill: HEAD, type: ShadingType.CLEAR, color: "auto" } : (o.tintCol === ci ? { fill: TINT, type: ShadingType.CLEAR, color: "auto" } : undefined),
          margins: { top: 70, bottom: 70, left: 110, right: 110 },
          children: [new Paragraph({ children: runs, spacing: { after: 0, line: 276 } })],
        });
      }),
    })),
  });
}
const gap = () => p("", { after: 80 });

const logo = fs.readFileSync("img/simreal-logo-ink.png");

// ---------- Content ----------
const children = [];

children.push(new Paragraph({
  children: [new ImageRun({ type: "png", data: logo, transformation: { width: 170, height: 46 }, altText: { title: "SimReal", description: "SimReal logo", name: "logo" } })],
  spacing: { after: 240 },
}));
children.push(p([r("公司简介、产品清单与参考报价", { bold: true, size: 40, color: INK })], { after: 80 }));
children.push(p([r("2026 年 9 月", { color: MUTED, size: 18 })], { after: 240 }));
children.push(p([r("让 AI 从会考试，变成会干活。", { bold: true, size: 28, color: ACCENT })], { after: 120 }));
children.push(p("SimReal 为大模型公司和 AI 应用企业搭建真实工作的训练环境，提供行业专家数据和评测。AI 在环境里做真实的事，按真实结果打分，再用结果训练自己，在金融、法律、医疗、代码等专业领域越练越强。"));

// 1. Company
children.push(h1("一、公司简介"));
children.push(bullet([r("团队：", { bold: true, color: INK }), r("四位量化出身的创始人，来自剑桥、LSE、杜克，有 Jane Street、Citadel、D. E. Shaw、Millennium、Optiver 的从业经历，以及剑桥机器学习研究背景；四人都放弃了顶级量化机构的 return offer。")]));
children.push(bullet([r("进展：", { bold: true, color: INK }), r("成立 14 天做出 7 款产品；旗舰交易环境 Xitadel 让开源模型 Qwen3.8-27B 在从未见过的真实行情上交易表现提升 12%，多次独立运行均复现；两家前沿 AI 实验室在洽谈；已与 Surge AI、AfterQuery 合作；正在融资。")]));
children.push(bullet([r("专家网络：", { bold: true, color: INK }), r("7,000+ 专家已报名，通过 21 所合作高校可触达 20 万+ 专业人士，覆盖金融、法律、医疗、供应链、代码等领域。")]));
children.push(bullet([r("质量：", { bold: true, color: INK }), r("每个环境和评分标准上线前都做对抗测试。谜题基准经受 400 次作弊攻击，0 次成功；财务月结环境评分漏洞从 6 个降到 0。")]));
children.push(bullet([r("独立中立：", { bold: true, color: INK }), r("不接受模型公司入股，每家客户都能放心采购。")]));

// 2. Products
children.push(h1("二、产品清单"));
children.push(table([2000, 4200, 3438], [
  ["产品线", "包含", "用途"],
  ["专家数据", "SFT 指令数据、CoT 推理链、复杂 Query 构造、Reference Answer、RLHF 偏好数据、Reward 数据、代码 SFT 与调试数据", "行业专家出题、写答案、做判断，用于模型训练"],
  ["Rubric 与评测", "Rubric 设计与拆解、逐项评分与质检、LLM-as-a-Judge 数据、私有评测集、Benchmark 定制", "把好答案拆成可逐条检查的评分标准，测出模型真实水平"],
  ["Agent 数据", "多轮工具调用轨迹、长程任务、完整 Session、DeepResearch", "记录 Agent 完成长任务的全过程，含工具调用与中间步骤"],
  ["RL 训练环境与验证器", "交易、财务月结、软件工程、数学证明、逻辑推理、AI 研究、未来预测", "模型在环境里反复练习，验证器按真实结果自动打分"],
  ["企业定制与持续训练", "专属训练环境、专属评测、持续训练", "围绕客户自己的工作流搭建；模型每次升级都回到环境继续训练"],
], { boldFirst: true }));
children.push(h2("已上线和在建的训练环境"));
children.push(table([2600, 4400, 2638], [
  ["环境", "内容", "已有结果"],
  ["Xitadel · 交易", "AI 在真实行情中交易，按盈亏评分", "训练后交易表现 +12%"],
  ["财务月结", "让 AI 零差错完成月末结账", "评分漏洞 6 → 0"],
  ["软件工程", "检验 AI 写的代码能否经受住后续版本", "—"],
  ["数学证明 · 逻辑推理", "让 AI 证明答案，而不是猜答案", "709 道防作弊谜题"],
  ["AI 研究 · MLBench", "AI 独立完成研究项目，从读数据到交结果", "60 个研究任务"],
  ["未来预测", "对真实事件提前判断，揭晓后按结果打分", "数据实时接入"],
], { boldFirst: true, accentCol: 2 }));

// 3. How we work
children.push(h1("三、合作方式"));
children.push(step([r("需求沟通：", { bold: true, color: INK }), r("领域、数据形式、量级、交付周期。")]));
children.push(step([r("样例或试点：", { bold: true, color: INK }), r("先给样例，或做小批量付费试点。")]));
children.push(step([r("验收：", { bold: true, color: INK }), r("客户按自己的标准测评。")]));
children.push(step([r("批量与长期合作：", { bold: true, color: INK }), r("数据按批次交付；环境打包交付，接入客户的训练或测试流程。")]));

// 4. Pricing
children.push(h1("四、参考报价"));
children.push(note("以下为参考区间，按领域、难度、数量和交付周期浮动，以正式报价为准。"));
children.push(table([2500, 1300, 1700, 1700, 2438], [
  ["产品", "计价单位", "海外（USD）", "国内（RMB）", "说明"],
  ["试点 / Demo", "每项目", "5,000–30,000", "2 万–10 万", "通常 50–200 条，验收后转批量"],
  ["专家 SFT / CoT / 参考答案", "每条", "30–200", "200–1,000", "金融、法律、医疗；按难度分档"],
  ["复杂 Query 构造", "每题", "20–100", "100–500", "真实场景、多约束"],
  ["RLHF 偏好 / Reward", "每对", "10–100", "50–400", "专家判断，附理由"],
  ["Rubric 设计（含参考答案）", "每题", "150–800", "800–4,000", "上线前做对抗测试"],
  ["Rubric 逐项评分与质检", "每条回答", "5–30", "30–150", "含抽检复核"],
  ["LLM-as-a-Judge 校准数据", "每条", "20–80", "100–400", "专家逐项分数和理由"],
  ["Agent 长程轨迹（专家实跑）", "每 Session", "200–1,500", "1,000–8,000", "30 次以上工具调用，完整 Session"],
  ["RL 任务（含验证器）", "每任务", "300–2,000", "2,000–12,000", "非独家；独家另议"],
  ["RL 环境授权", "每环境每季度", "50,000–300,000", "30 万–200 万", "含持续更新；独家另议"],
  ["私有评测集 / Benchmark 定制", "每项目", "30,000–150,000", "20 万–100 万", "200–1,000 题，含 Rubric 和评分"],
  ["持续训练服务", "每季度", "100,000–1,000,000+", "另议", "面向前沿实验室"],
], { boldFirst: true, tintCol: 2 }));

children.push(bullet("独家交付另行报价；加急和特殊合规要求另议。"));

// 5. Contact
children.push(h1("五、联系方式"));
children.push(p([r("business@simreal.co", { bold: true, color: INK }), r("  ·  simreal.co", { color: BODY })]));

const doc = new Document({
  creator: "SimReal",
  title: "SimReal 公司简介、产品清单与参考报价",
  styles: {
    default: { document: { run: { font: FONT, size: 20, color: BODY } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 30, bold: true, color: INK }, paragraph: { outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 24, bold: true, color: INK }, paragraph: { outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: "dots", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } }, run: { color: ACCENT } } }] },
      { reference: "steps", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } }, run: { color: ACCENT, bold: true } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "SimReal · business@simreal.co · ", font: FONT, size: 15, color: MUTED }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 15, color: MUTED })],
      })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync("SimReal-公司简介与参考报价.docx", buf); console.log("ok", buf.length); });
