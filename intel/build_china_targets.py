"""把 china-claims.csv（供应商 → 客户）反向整理成外联目标名单。

每个目标一份文档 targets/<slug>，写到 OUT（默认 build/china-targets/）：
  name, category, tier, priority, angle, vendors[], evidence[], draft, review
tier：已证实客户 / 合作伙伴 / 潜在客户 / 渠道伙伴。
review 只在 --with-review 时写入（首次建库用）；之后审批状态以页面数据库为准。

Usage: python3 intel/build_china_targets.py [--signals D-signals.csv] [--with-review]
"""
import argparse, csv, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 原始"客户或合作方"写法 → 规范目标名（一个写法可拆成多个目标）
SPLIT = {
    "腾讯/阿里/百度/字节跳动": ["腾讯", "阿里巴巴", "百度", "字节跳动"],
    "三星、大疆、阿里、字节跳动": ["三星", "大疆", "阿里巴巴", "字节跳动"],
    "中国科学院、京东、商汤、科大讯飞、腾讯": ["中国科学院", "京东", "商汤", "科大讯飞", "腾讯"],
    "微软、高通、英伟达、阿里巴巴、百度、腾讯": ["微软", "高通", "英伟达", "阿里巴巴", "百度", "腾讯"],
    "丰田、博世、比亚迪、吉利": ["丰田", "博世", "比亚迪", "吉利"],
    "Google DeepMind、英伟达、迪士尼研究院、丰田研究院": ["Google DeepMind", "英伟达", "丰田"],
    "Figure AI、1X Technologies": ["Figure AI", "1X"],
    "智元机器人、银河通用机器人": ["智元机器人", "银河通用"],
    "百度、小米、京东": ["百度", "小米", "京东"],
    "蔚来、理想、博世": ["蔚来", "理想汽车", "博世"],
    "长安、广汽、奇瑞、上汽": ["长安汽车", "广汽", "奇瑞", "上汽"],
    "毫末、旷视、元戎": ["毫末智行", "旷视", "元戎启行"],
    "阿里巴巴/百度/字节跳动/网易": ["阿里巴巴", "百度", "字节跳动", "网易"],
    "阿里巴巴、字节跳动、百度、科大讯飞、旷视、好未来": ["阿里巴巴", "字节跳动", "百度", "科大讯飞", "旷视", "好未来"],
    "阿里、腾讯、京东、联想、百度": ["阿里巴巴", "腾讯", "京东", "联想", "百度"],
    "喜马拉雅/Rokid/Roobo": ["喜马拉雅"],
    "字节跳动 Seed、港科大、北大、清华": ["字节跳动"],
    "字节跳动 Seed（豆包大模型团队）、M-A-P": ["字节跳动"],
    "Meta、阿里巴巴、腾讯、百度等30余家": ["阿里巴巴", "腾讯", "百度"],
    "华为云/中国信通院": ["华为", "中国信通院"],
    "上海人工智能实验室 OpenDataLab（OmniDocBench）": ["上海人工智能实验室"],
    "上海人工智能实验室（中国大模型语料数据联盟）": ["上海人工智能实验室"],
}
ALIAS = {
    "字节跳动": ["字节跳动", "字节跳动 Seed/豆包", "字节跳动 Seed（Seed2.0）", "字节跳动 豆包 Seed（SuperGPQA）"],
    "阿里巴巴": ["阿里巴巴", "阿里", "阿里云", "阿里 通义 Qwen3.5", "阿里巴巴（通义/千问）"],
    "腾讯": ["腾讯", "腾讯混元", "腾讯（混元）", "腾讯科技（成都）有限公司", "腾讯朱雀实验室、腾讯科恩实验室"],
    "百度": ["百度", "百度（中国）有限公司", "百度（文心一言）", "百度文心一言（内部）", "百度智能云 千帆", "百度AI市场"],
    "华为": ["华为云", "华为云盘古大模型生态", "华为数据存储"],
    "月之暗面": ["月之暗面", "月之暗面（Kimi）", "月之暗面 Kimi K2.5"],
    "智谱": ["智谱AI"],
    "京东": ["京东", "京东（言犀/ViTAE大模型，内部）"],
    "智元机器人": ["智元机器人 AgiBot", "上海智元新创（智元机器人）", "觅蜂科技（蜂巢数据共创行动）"],
    "英伟达": ["英伟达", "NVIDIA 英伟达"],
    "Google DeepMind": ["Google DeepMind", "谷歌"],
    "1X": ["1X Technologies"],
    "银河通用": ["银河通用 Galbot"],
    "丰田": ["丰田 Toyota"], "博世": ["博世 Bosch"], "吉利": ["吉利 Geely"], "比亚迪": ["比亚迪 BYD"],
    "中国科学院": ["中国科学院", "中国科学院自动化研究所"],
    "红杉中国 xbench": ["红杉中国 xbench"],
    "北京瑞莱智慧": ["北京瑞莱智慧科技有限公司"],
    "OpenCSG 开放传神": ["开放传神 OpenCSG"],
    "北京人形机器人数据训练中心": ["人形机器人数据训练中心（北京石景山）"],
}
RAW2 = {}
for k, v in SPLIT.items():
    RAW2[k] = v
for canon, raws in ALIAS.items():
    for r in raws:
        RAW2.setdefault(r, [canon])

SKIP_REL = {"投资方"}
SKIP_NAME = re.compile(r"未具名|约60家|160\+|前沿模型团队|MMAR|M-A-P|北京国际|中国知网|中国移动北京|整数智能|上海库帕思|PublicAI|拓维|BOUNTY|Phantom|西北工业|北京大学|北京师范|上海交通|诠视|灵心巧手|鹏城|清华|循环智能|澜舟")
# 被 SKIP_NAME 排除但值得保留的（研究机构/小厂里可能是买家）
KEEP = {"鹏城实验室", "循环智能", "澜舟科技", "清华大学", "灵心巧手", "诠视科技"}

# 规范目标：类别、优先级、切入点
META = {
    "字节跳动": ("国内大模型公司", "P0", "Seed 后训练/评测团队。自建 Xpert 专家平台（8 万+专家），同时向海天瑞声、恺望、热热数据等外采；与 2077AI 共建 SuperGPQA。切入：Xpert 做不了的可执行 RL 环境+验证器（金融、软件工程、Agent 任务）。"),
    "阿里巴巴": ("国内大模型公司", "P0", "通义/Qwen。自建晓天睿士专家社区；外采海天瑞声、光轮（具身）、曼孚等；传领投 UniPat。切入：Agent/代码 RL 环境与金融、法律专家评测集。"),
    "腾讯": ("国内大模型公司", "P0", "混元。有 AI Expert 专家平台；龙猫称其核心供应商；海天瑞声、数据堂客户；与司南共建 SecBench；传参投 UniPat。切入：安全/金融/游戏 Agent 环境。"),
    "百度": ("国内大模型公司", "P1", "文心/千帆。内部百度众测+数据众包，同时是海天瑞声、数据堂、恺望客户。切入：千帆生态合作，把 RL 环境作为千帆数据服务的一部分。"),
    "智谱": ("国内大模型公司", "P0", "海天瑞声合作方（2024 协议），龙猫称其客户。GLM Agent/代码方向需要 RL 环境。"),
    "月之暗面": ("国内大模型公司", "P0", "龙猫称其客户；Kimi K2.5 采用 UniPat BabyVision；海天瑞声 2024-03 公告称未合作。切入：Agent/长程任务 RL 环境。"),
    "华为": ("科技大厂", "P1", "盘古生态与星尘、景联文、深数所合作。切入：行业大模型（金融、政企）专家数据与评测。"),
    "科大讯飞": ("国内大模型公司", "P1", "海天瑞声年报客户、曼孚历史客户。星火在教育、医疗垂直方向需专家数据。"),
    "商汤": ("国内大模型公司", "P1", "恺望、倍赛称其客户。日日新需要评测与专家数据。"),
    "京东": ("科技大厂", "P1", "京东众智内部供数；标贝、星尘、希尔贝壳客户。切入：零售/客服 Agent 环境。"),
    "小米": ("科技大厂", "P1", "星尘称其客户。MiMo-V2.6（2026-09）称半年投入高质量数据与强化学习环境，公开沙箱环境池与反 reward-hacking 管线。切入：RL 环境与验证器。"),
    "网易": ("科技大厂", "P2", "曼孚客户墙。伏羲/有道教育方向。"),
    "小红书": ("AI 应用公司", "P2", "热热数据称其客户。"),
    "好未来": ("AI 应用公司", "P2", "曼孚历史客户。教育大模型（九章）需数学/学科专家数据。"),
    "联想": ("科技大厂", "P3", "希尔贝壳客户。"),
    "滴滴": ("科技大厂", "P3", "标贝客户墙。"),
    "喜马拉雅": ("AI 应用公司", "P3", "标贝客户墙（语音）。"),
    "微软": ("frontier lab", "P2", "海天瑞声招股书时期前五大客户、年报仍列名；标贝、晴数客户墙。中国区团队采购多语种数据。"),
    "亚马逊": ("frontier lab", "P2", "海天瑞声年报客户、2019 前五大。"),
    "Google DeepMind": ("frontier lab", "P1", "光轮智能客户/合作方（具身仿真）。海外 frontier lab 已在主名单。"),
    "英伟达": ("科技大厂", "P1", "与光轮共同设计 Isaac Lab-Arena；晴数客户墙。切入：机器人/Agent 评测环境合作。"),
    "高通": ("企业", "P3", "晴数客户墙（端侧语音）。"),
    "三星": ("企业", "P3", "海天瑞声前五大客户，但 2020 年采购额骤降。"),
    "海康威视": ("企业", "P3", "海天瑞声年报客户（视觉）。"),
    "中国移动": ("企业", "P2", "海天瑞声年报客户；九天大模型，央企数据采购多走招标。"),
    "上海电信": ("企业", "P3", "库帕思合作方。"),
    "中国银行": ("金融机构", "P2", "标贝客户墙。金融大模型可切金融专家数据与评测。"),
    "东方财富": ("金融机构", "P1", "与司南 OpenCompass 共建 OpenFinData 金融评测集。直接的金融评测/专家数据买方。"),
    "智元机器人": ("垂直 AI", "P1", "光轮客户、库帕思合作方；旗下觅蜂科技发起蜂巢数据共创（海天瑞声加入）、参投恺望。具身数据大买家。"),
    "银河通用": ("垂直 AI", "P2", "光轮客户（具身仿真）。"),
    "Figure AI": ("垂直 AI", "P2", "光轮客户。"),
    "1X": ("垂直 AI", "P2", "光轮客户。"),
    "乐聚机器人": ("垂直 AI", "P2", "海天瑞声合作（数采、训练场）。"),
    "北京人形机器人数据训练中心": ("政府", "P3", "海天瑞声共建训练场。"),
    "灵心巧手": ("垂直 AI", "P3", "数据堂具身合作。"),
    "诠视科技": ("垂直 AI", "P3", "数据堂具身合作（2026-08）。"),
    "比亚迪": ("企业", "P3", "光轮客户（智驾/机器人仿真）。"),
    "吉利": ("企业", "P3", "光轮合作方。"), "丰田": ("企业", "P3", "光轮客户。"), "博世": ("企业", "P3", "光轮、龙猫客户。"),
    "蔚来": ("企业", "P3", "龙猫客户（智驾标注）。"), "理想汽车": ("企业", "P3", "龙猫客户（智驾标注）。"),
    "长安汽车": ("企业", "P3", "恺望客户（智驾）。"), "广汽": ("企业", "P3", "恺望客户。"), "奇瑞": ("企业", "P3", "恺望客户。"), "上汽": ("企业", "P3", "恺望客户。"),
    "小鹏汽车": ("企业", "P3", "标贝客户墙（车载语音）。"), "大疆": ("企业", "P3", "龙猫客户。"),
    "毫末智行": ("垂直 AI", "P3", "数据堂 2022 第一大客户、恺望客户（智驾）。"), "旷视": ("AI 应用公司", "P3", "恺望、曼孚客户。"), "元戎启行": ("垂直 AI", "P3", "恺望客户。"),
    "中国科学院": ("高校研究机构", "P3", "海天瑞声年报客户、合作协议（自动化所）；倍赛客户墙。"),
    "中国信通院": ("政府", "P3", "海天瑞声合作；深数所合作。标准/评测制定方，可作背书渠道。"),
    "上海人工智能实验室": ("高校研究机构", "P2", "OmniDocBench 由 2077AI 标注；中国大模型语料数据联盟。司南评测体系，可合作共建基准。"),
    "鹏城实验室": ("高校研究机构", "P2", "2023 年成为数据堂新大客户（AI 评测测试）。"),
    "清华大学": ("高校研究机构", "P3", "海天瑞声年报客户；百度 PANDA 数据集合作。"),
    "澜舟科技": ("国内大模型公司", "P3", "海天瑞声合作协议（2024）。"),
    "循环智能": ("AI 应用公司", "P3", "海天瑞声共建中文训练数据（2023）。"),
    "北京瑞莱智慧": ("AI 应用公司", "P2", "深数所首单语料交易买方。AI 安全方向，可切红队/安全评测数据。"),
    "红杉中国 xbench": ("其他", "P2", "与 UniPat 共建 BabyVision；xbench 评测体系。可合作共建专业领域评测。"),
    "OpenCSG 开放传神": ("AI 应用公司", "P3", "数据堂合作。"),
}

# 潜在客户（名单里未出现供应商关系，但属于后训练数据的天然买家）
POTENTIAL = {
    "DeepSeek 深度求索": ("国内大模型公司", "P0", "未找到公开的外部数据供应商。2026-06 扩招开出 Code Agent 数据、通用 Agent 数据、医学/法律/小语种专业领域数据 PM 等岗位，正是专家数据+环境+评测的需求；也在自建管线，切入点是补充长尾领域环境与验证器。"),
    "阶跃星辰": ("国内大模型公司", "P0", "未找到公开的外部数据供应商。在招 Agent RL、Agent 数据算法、GUI/Browser-use Agent，职责含构建强化学习环境。"),
    "MiniMax": ("国内大模型公司", "P0", "招股书前五大供应商为算力，未见数据供应商。M2.5 称基于 20 万+真实环境做 RL（编程/搜索/办公）；Copula Lab 创始团队出自其 Agent/评测团队。切入：办公、金融等专业环境与验证器补充。"),
    "美团": ("科技大厂", "P1", "LongCat-Flash-Thinking-2601 做多环境 RL（每套 60+ 工具）；发起 AGI-Eval 评测社区；媒体称有自建专家平台。"),
    "快手": ("科技大厂", "P1", "KAT-Coder 做大规模 Agentic RL，自动构建可执行仓库环境（成功率 16.5%→57.2%）。切入：软件工程环境与验证器。"),
    "蚂蚁集团": ("金融机构", "P1", "百灵 Ring-2.6-1T 面向 Agent 工作流、异步 RL。金融/医疗垂直，天然需要金融专家数据与评测。"),
    "百川智能": ("垂直 AI", "P1", "Baichuan-M3 强调顶级医生定义评测标准、Fact-Aware RL。切入：医学专家 rubric 与验证器。"),
    "零一万物": ("国内大模型公司", "P2", "转向企业解决方案。"),
    "面壁智能": ("国内大模型公司", "P2", "端侧模型 MiniCPM。"),
    "昆仑万维": ("国内大模型公司", "P2", "Skywork 系列 Agent/代码模型。"),
    "360": ("科技大厂", "P3", "360 智脑，安全方向。"),
    "中国电信": ("企业", "P3", "星辰大模型，央企采购走招标。"),
    "中国联通": ("企业", "P3", "有大模型微调数据清洗/标注招标（仅见搜索摘要）。"),
    "平安集团": ("金融机构", "P1", "金融、医疗大模型；已在主名单。"),
    "恒生电子": ("垂直 AI", "P1", "金融大模型；已在主名单。"),
    "九坤投资": ("金融机构", "P2", "量化 AI 研究团队；已在主名单。"),
}
# 已在 prospects.csv / drafts 的目标
DRAFTS = {
    "字节跳动": "bytedance-seed", "阿里巴巴": "qwen", "腾讯": "tencent-hunyuan", "智谱": "zhipu", "月之暗面": "moonshot-ai",
    "DeepSeek 深度求索": "deepseek", "阶跃星辰": "stepfun", "MiniMax": "minimax", "百川智能": "baichuan",
    "平安集团": "pingan", "恒生电子": "hundsun", "九坤投资": "ubiquant", "Google DeepMind": "google-deepmind", "微软": "",
}

CHANNEL = {
    "海天瑞声": ("P1", "渠道/分包伙伴：上市公司，客户覆盖字节/阿里/腾讯/百度，缺 RL 环境产品"),
    "Abaka": ("P1", "渠道/分包伙伴：与字节 Seed 共建 SuperGPQA，海外品牌，做专家标注与基准"),
    "整数智能": ("P1", "渠道/分包伙伴：疑与 Abaka 同一团队"),
    "UniPat": ("P1", "竞品兼潜在合作方：后训练数据/评测新公司，传阿里领投"),
    "智能知识（一面千识）": ("P1", "竞品兼潜在合作方：专家网络，前字节 Seed 团队"),
    "Copula": ("P1", "竞品兼潜在合作方：国内唯一明确卖 RL 环境的公司"),
    "光轮智能": ("P2", "具身仿真数据，客户重叠度高，可做联合方案"),
    "澳鹏中国": ("P1", "渠道/分包伙伴：中国收入 4.2 亿+，大模型业务高增长，有专家数据线 EliteAI"),
    "数据堂": ("P2", "渠道/分包伙伴：北交所 IPO 辅导中"),
}

SIGNAL_MAP = {"招商银行/平安（金融）": "中国银行", "中国移动/中国电信/联通": "中国移动", "字节 Seed": "字节跳动"}

REL_TIER = {"客户": "已证实客户", "财报披露": "已证实客户", "官网客户墙（转述）": "已证实客户",
            "合作": "合作伙伴", "共建基准": "合作伙伴", "论文致谢": "合作伙伴",
            "客户变动（停止合作等）": "合作伙伴"}
TIER_RANK = {"已证实客户": 0, "合作伙伴": 1, "潜在客户": 2, "渠道伙伴": 3}


def slug(name):
    # 数据库文档 id 只能用 ASCII：英文部分 + 名称哈希
    import hashlib
    ascii_part = re.sub(r"[^0-9A-Za-z]+", "-", name).strip("-").lower()[:30]
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    return f"{ascii_part}-{h}" if ascii_part else f"t-{h}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "build" / "china-targets"))
    ap.add_argument("--signals", default="")
    ap.add_argument("--with-review", action="store_true")
    a = ap.parse_args()

    targets = {}

    def get(name, meta, tier):
        t = targets.get(name)
        if not t:
            cat, pri, angle = meta
            t = targets[name] = {"name": name, "category": cat, "priority": pri, "angle": angle,
                                 "tier": tier, "vendors": [], "evidence": [], "draft": DRAFTS.get(name, "")}
        if TIER_RANK[tier] < TIER_RANK[t["tier"]]:
            t["tier"] = tier
        return t

    for r in csv.DictReader(open(ROOT / "intel/china-claims.csv", encoding="utf-8")):
        if r["关系类型"] in SKIP_REL:
            continue
        raw = r["客户或合作方"]
        names = RAW2.get(raw)
        if names is None:
            if raw in KEEP or raw in META:
                names = [raw]
            elif any(raw.startswith(k) for k in KEEP):
                names = [next(k for k in KEEP if raw.startswith(k))]
            elif SKIP_NAME.search(raw):
                continue
            else:
                names = [raw]
        vendor = r["供应商"]
        internal = "内部" in vendor
        for n in names:
            if n not in META:
                print("no META:", n, "<-", raw)
                continue
            t = get(n, META[n], REL_TIER.get(r["关系类型"], "合作伙伴"))
            if vendor not in t["vendors"] and not internal:
                t["vendors"].append(vendor)
            t["evidence"].append({"src": vendor, "rel": r["关系类型"], "what": r["工作内容或领域"],
                                  "quote": r["原文证据"], "url": r["来源链接"], "date": r["来源日期"],
                                  "stype": r["来源类型"], "conf": r["置信度"]})

    for n, meta in POTENTIAL.items():
        get(n, meta, "潜在客户")

    if a.signals:
        for r in csv.DictReader(open(a.signals, encoding="utf-8")):
            org = r["机构"]
            hit = SIGNAL_MAP.get(org) or next((n for n in targets if n.split()[0] in org or org.split()[0] in n), None)
            if not hit:
                print("signal unmatched:", org)
                continue
            targets[hit]["evidence"].append({"src": "公开信号", "rel": r["信号类型"], "what": r["信号内容"],
                                             "quote": r["原文证据"], "url": r["来源链接"], "date": r["来源日期"],
                                             "stype": r["来源类型"], "conf": r["置信度"]})

    # 渠道伙伴：供应商本身（分包/联合交付）；clients = 它在名单里服务的目标
    clients = {}
    for t in list(targets.values()):
        for v in t["vendors"]:
            clients.setdefault(v, set()).add(t["name"])
    for r in csv.DictReader(open(ROOT / "intel/china-vendors.csv", encoding="utf-8")):
        v = r["供应商"]
        if "内部" in v or "交易所" in v or "数据集团" in v or v.startswith(("中文在线", "司南", "智源", "SuperCLUE", "AGI-Eval", "xbench")):
            continue
        if v.startswith(("慧听", "京东众智", "百度智能云")):
            continue
        pri, role = CHANNEL.get(v.split()[0], ("P2", "渠道/分包伙伴"))
        t = get(v, (r["类型"], pri, f"{role}。{r['简介']}"), "渠道伙伴")
        t["clients"] = sorted(clients.get(v, []))
        t["channel"] = {"type": r["类型"], "size": r["规模"], "site": r["官网"], "domains": r["主要领域"], "claims": r["收录声明数"]}

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.json"):
        f.unlink()
    for t in targets.values():
        t["evidence"].sort(key=lambda e: ({"高": 0, "中": 1, "低": 2}.get(e["conf"], 3), e["date"]), reverse=False)
        if a.with_review:
            t["review"] = {"status": "pending", "note": "", "contact": ""}
        (out / f"{slug(t['name'])}.json").write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")
    from collections import Counter
    print(len(targets), Counter(t["tier"] for t in targets.values()), Counter(t["priority"] for t in targets.values()))


if __name__ == "__main__":
    main()
