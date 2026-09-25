"""Check every draft against the fixed templates: only the opening line and the bracket fills may differ."""
import re,glob,difflib
EN="""Subject: Expert data for [Company]'s post-training

Hi [Name],

[One line about them]

I'm [Your name], co-founder of SimReal (simreal.co). We build RL environments, verifiers and expert data for post-training. Our team is ex-Citadel, Millennium and Jane Street.

Our edge is expert supply. Through 21 partner universities and our corporate networks, we reach 200,000+ professionals, from PhD students to senior practitioners, across [finance, law, medicine, engineering, ...]. 7,000+ have already signed up to our expert waitlist[, and every expert is ID- and credential-checked before starting work].

Before pitching anything, I'd like to understand where you're short: which domains, which formats (SFT, preference data, rubrics, RL tasks, evals), and what volume and turnaround you need. If there's a fit, we'd start with a small paid pilot so you can judge the quality yourselves.

Open to a 20-minute call next week?

Best,
[Your name]
Co-founder, SimReal"""
CN="""主题：SimReal｜[公司名] 后训练专家数据

[称呼]您好，

[一句关于对方的话]

我是 SimReal（simreal.co）联合创始人[姓名]。我们为大模型后训练提供 RL 环境、验证器和专家数据，团队来自 Citadel、Millennium 和 Jane Street。

我们的优势在专家供给：通过 21 所合作高校和企业网络，可触达 20 万+ 专业人士，从博士生到资深从业者，覆盖[金融、法律、医疗、工程……]等行业，其中 7,000+ 位已报名加入我们的专家候补名单[，所有专家上岗前均完成身份与资质核验]。

在介绍方案之前，想先了解贵司目前的数据缺口：哪些领域、什么形式（SFT、偏好数据、评分标准、RL 任务、评测集），以及需要的量级和交付周期。如果匹配，我们可以先做一个小批量付费试点，质量由你们直接判断。

下周是否方便约 20 分钟简单聊聊？

[姓名]
SimReal 联合创始人
微信/电话：[ ]"""
WX="""[称呼]您好，我是 SimReal 联合创始人[姓名]，[介绍人]推荐我联系您。我们为大模型团队做后训练专家数据和 RL 环境，团队来自 Citadel / Millennium / Jane Street，通过 21 所合作高校和企业网络可触达 20 万+ 各行业专业人士。想了解一下贵司现在数据上缺哪些（领域、形式、量级、交付周期），合适的话先做个小批量试点。您看下周方便约 20 分钟吗？"""
def pattern(t):
    # turn each [..] placeholder into a wildcard, but keep the fixed brackets literal
    keep={"[, and every expert is ID- and credential-checked before starting work]","[，所有专家上岗前均完成身份与资质核验]","[ ]"}
    parts=re.split(r"(\[[^\]]*\])",t); out=""
    for p in parts:
        if p.startswith("[") and p not in keep: out+="(.+?)"
        else: out+=re.escape(p)
    return re.compile("^"+out+"$",re.S)
banned=["verified expert","已验证","融资"," TS","投资人","投资方","investor","github","Series","raised"]
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for f in sorted(glob.glob("drafts/*.md")):
    s=open(f).read()
    email=s.split("## 邮件\n\n",1)[1].split("\n\n---",1)[0].strip()
    tpl=EN if email.startswith("Subject") else CN
    m=pattern(tpl).match(email)
    print(f, "EMAIL template match:", bool(m))
    if m: print("   fills:", [g[:70] for g in m.groups()])
    if "## 微信版" in s:
        wx=s.split("## 微信版（引荐后）\n\n",1)[1].strip()
        m2=pattern(WX).match(wx); print("   WECHAT match:", bool(m2), m2.groups() if m2 else "")
    bad=[b for b in banned if b.lower() in email.lower()]
    print("   banned terms in email:", bad)
