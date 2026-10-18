# -*- coding: utf-8 -*-
"""Round-14 expansions: 7 blocks into book.tex & male.tex, with verification.
Idempotent: re-run skips blocks already inserted."""
import re, sys

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
BOOK = BASE + "\\" + "book.tex"
MALE = BASE + "\\" + "male.tex"

# ---------- Block B: book, before 红旗信号 ----------
B = r"""\section{第一次就诊：流程、如何开口与费用参考}

知道"该挂哪个科"之后，更多人卡在"怎么开口"。这里把首次就诊的完整流程走一遍：

\begin{itemize}
	\item \textbf{就诊前准备}：写一份简单的"症状日记"——症状是什么、何时开始、什么情况下加重或缓解、与性生活/月经周期/用药有无关联；带上正在服用的药物清单、既往检查报告和疫苗接种记录。\textbf{就诊前不要自行冲洗阴道、涂药膏或自行服用抗生素}，以免掩盖体征干扰诊断；如需做尿道或宫颈取样，一般建议留取前 2--3 小时不排尿（以医院告知为准）。
	\item \textbf{如何开口}：直接陈述即可，不需要铺垫——"性生活后尿道刺痛三天，想查一下感染"就是很好的开场白。医生每天面对大量同类问题，你的描述越具体（时间线、伴随症状、末次高危行为的时间），诊断方向越准。隐瞒性行为史可能导致误判，如实告知是对自己负责。
	\item \textbf{常见检查项目}：视主诉而定——尿常规、分泌物或前列腺液检查、尿道/宫颈拭子（淋病与衣原体核酸）、血检（HIV、梅毒、乙肝等）、超声、妇科检查、精液分析等；多数当天可完成，部分结果需等数天。
	\item \textbf{费用参考（人民币，2026 年前后大陆公立医院常见区间）}：HIV 筛查约 50--150 元；梅毒筛查约 30--80 元；淋病/衣原体核酸单项约 100--200 元；阴道分泌物常规约 30--60 元；精液常规约 100--200 元；妇科超声约 100--300 元；HPV 分型检测约 200--400 元；TCT 约 150--300 元；PSA 约 50--100 元。地区与医院等级差异较大，\textbf{以当地医院公示为准}；部分 STI 筛查在疾控中心 VCT 门诊可免费（见本章前文）。
	\item \textbf{关于隐私}：门诊病历依法如实记录，这是后续诊疗与维权的基础；有顾虑可在挂号时咨询医院的隐私保护流程。选择线上问诊时，核验平台《医疗机构执业许可证》与医生执业信息，警惕以"性健康咨询"为名推销高价疗程的商业机构。
	\item \textbf{性治疗与心理咨询}：公立医院心理科/精神科收费相对规范（单次数十至数百元）；社会机构的婚姻家庭咨询与性治疗多为按次计费（数百至上千元不等），资质参差不齐，签约前核实受训背景与督导经历，勿与"挽回感情服务"类营销混淆。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
紧张到说不出口时，可以提前把症状写在纸上递给医生，或开场就说"我有点紧张，但想认真查一下"。在医生眼里这是每天要处理的常规问题，对事不对人；你越如实，诊断越省时间。
\end{tcolorbox}

"""

# ---------- Block A: book, before 线上权威渠道 ----------
A = r"""\section{年度性健康自查清单}

把性健康纳入年度健康管理——像体检、看牙一样按计划执行，而不是"出问题了再说"。以下清单按自身情况裁剪使用：

\begin{itemize}
	\item \textbf{通用底单（所有成年人，每年一次）}：核对疫苗状态（未免疫或无抗体者补种乙肝疫苗；适龄人群按当地供应情况评估 HPV 疫苗）；按风险等级安排 STI 筛查——单一固定伴侣且双方已排除感染者可适当降低频率，有新伴侣或多伴侣者建议每 3--6 个月筛查 HIV、梅毒、淋病、衣原体并按窗口期复查；每年复核一次避孕方式是否仍适合当前生活状态（详见避孕章对比矩阵）。
	\item \textbf{每月自检}：观察生殖器与腹股沟皮肤有无溃疡、赘生物、颜色改变；男性加做睾丸触诊（对照男性卷"定期自检指南"）；女性留意分泌物性状与周期的规律，出现明显改变及时就诊。
	\item \textbf{女性追加}：有性生活后按指南定期宫颈癌筛查（TCT 与 HPV 分型，频率遵医嘱）；乳腺自检并按年龄安排影像学检查；备孕前完成孕前评估与遗传咨询。
	\item \textbf{男性追加}：45 岁起（有家族史提前至 40 岁）与医生讨论 PSA 筛查；有生育计划时做精液分析；久坐、高温作业或备孕者做好阴囊温度管理（见男性卷生活方式章节）。
	\item \textbf{男男性行为者（MSM）}：筛查增加咽部与直肠部位的淋病/衣原体取样；定期检测乙肝、丙肝；按医嘱评估 PrEP 使用（见本章前文）。
	\item \textbf{HIV 感染者与 PrEP 使用者}：按医嘱约每 3 个月随访病毒载量、CD4 与肾功能，把随访日期写进日历。
	\item \textbf{慢性病患者}：糖尿病、心血管疾病、抑郁症等患者每年与医生讨论一次疾病与药物对性功能的影响——不要默认"没办法"，多数情况可以调整。
	\item \textbf{更年期与老年人群}：围绝经期症状评估（是否适合 MHT）；恢复或增加性生活前做心血管耐受力评估；关注盆底功能（漏尿、下坠感）并及时转诊盆底康复。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
准备一个"性健康档案"：疫苗接种记录、历次筛查报告、手术与用药史、过敏史，就诊时带全，能省去大量重复检查，也避免口述遗漏。清单是提醒而非任务——完成得不完美没关系，做了就比不做强。
\end{tcolorbox}

"""

# ---------- Block C: book, before 网络性勒索 ----------
C = r"""\subsubsection{分手之后：协商删除与隐私重建}

前文的应对指南针对的是"影像已经被传播"的情形；更常见的处境是关系破裂后，双方手里还留着当年的私密内容。这个阶段处理得当，绝大多数风险可以在传播发生之前化解：

\begin{itemize}[leftmargin=2cm]
	\item \textbf{先谈删除，再谈对错}：删除请求放在分手沟通的最前面，而不是夹在争吵里。明确表达诉求："我们之间拍的那些照片和视频，请全部删除，我也会删掉你发给我的内容。"平静、具体的语言比指责性开场白更容易得到配合。
	\item \textbf{删除要彻底}：提醒对方覆盖所有位置——手机相册与"最近删除"、云端备份与共享相册、聊天记录中的原图、电脑与旧设备；双方互删最好当面或视频连线确认，而不是只凭一句"删了"。
	\item \textbf{解除共享与授权}：逐一检查共享相册、家人共享、旧设备登录与聊天文件同步，退出授权；修改常用密码并开启两步验证，防止情绪失控的前任"顺手翻旧账"。
	\item \textbf{拉扯期冷处理}：若对方拿"删除"讨价还价，不要反复哀求，也不要威胁对等报复——那只会把影像变成筹码。立场表达一次即可，随后保持距离；一旦对方以公开相要挟，直接转入下节网络性勒索的应对程序（不支付、存证据、报警）。
	\item \textbf{白纸黑字的边界}：和平分手的双方可以互作"不保存、不传播、不用于任何场合"的承诺。这类约定没有强制执行力，但让双方对底线形成明确共识，也留下了对方认可边界的沟通记录。
	\item \textbf{重建安全感}：分手后数月内对影像外流的担忧是常见的、合理的自我保护反应，不是"多心"；持续影响睡眠与情绪时，可经 12338 或 12356 热线转介心理咨询。
\end{itemize}

"""

# ---------- Block D: book, before 饮食与性健康 ----------
D = r"""\subsection{出差、旅行与酒店：路上的性健康}

旅行和出差打乱的不只是作息——陌生环境、时差、酒精加上"没人认识我"的放松感，会悄悄改变性行为的风险结构。

\begin{itemize}
    \item \textbf{行前小包}：足量安全套（检查有效期）、小包装水基润滑剂；服用口服避孕药者跨时区时可按出发地时间逐步调整服药时刻，或出发前咨询医生；常用药随身携带而非托运。
    \item \textbf{酒店的卫生真相}：规范消毒的床品、毛巾与浴缸\textbf{不是性传播感染的传播途径}——HIV、淋病、衣原体等病原体离开人体后极其脆弱；真菌（如念珠菌）在潮湿环境下的间接接触风险理论存在但极低，易感人群自带毛巾即可安心。与其焦虑床品，不如把注意力放在更现实的环节上。
    \item \textbf{偷拍防范}：入住后留意正对床铺与浴室的烟雾报警器、插座孔、绿植摆件等可疑位置；熄灯后用手机摄像头缓慢扫描房间，针孔摄像头的红外补光会呈现红色光点；发现后保留现场、报警并要求酒店出面处理。
    \item \textbf{时差、疲劳与性欲}：长途飞行后性欲下降多为生理性疲劳的正常表现；与其"必须补上"，不如先补睡眠（见上文"性爱时机与作息型"小节）。
    \item \textbf{异地重逢的预期管理}：久别重逢常自带"必须完美"的期待，反而滋生表现焦虑；把第一晚当作重新熟悉身体的约会，节奏放慢，满意度通常更高。
    \item \textbf{公共与半公共空间}：车内、公园等场所发生性行为可能违反治安管理规定，"浪漫加分"与当场尴尬之间并不对等。
    \item \textbf{酒精与判断力}："出差自由感"叠加酒局文化，是无保护性行为发生率最高的场景组合之一；提前给自己定一条底线（如"喝酒不进陌生人的房间"），比酒桌上现做决定可靠得多。
\end{itemize}

"""

# ---------- Block G: glossary tail (book) ----------
G_OLD = r"""男性避孕候选药。

\end{description}"""
G_NEW = r"""男性避孕候选药。
\item[非自愿亲密影像（NCII）] 未经当事人同意被拍摄、留存或传播的私密影像，俗称“复仇式色情”；核心应对为固定证据、平台投诉、报警与心理支持，分手阶段优先协商彻底删除（详见数字时代相关章节）。
\item[互盲] 辅助生殖中供精（供卵）者与受方夫妇、后代之间互不知晓对方身份的制度安排，保护各方隐私，并阻断未来可能的法律与情感纠纷。
\item[年度性健康自查] 将 STI 筛查、疫苗状态核对、生殖器自检与避孕方式复核纳入年度计划的自我管理做法，按人群与风险等级差异化安排（详见“求助与资源导航”章）。

\end{description}"""

# ---------- Block E: male, before 环境内分泌干扰物 ----------
E = r"""\subsection{赛前禁欲与运动表现：迷思与真相}

"大赛前不能近女色，会泄元气"——从拳坛到足坛，赛前禁欲的传统延续了几百年；现代运动科学的结论要平淡得多：

\begin{itemize}[leftmargin=2cm]
	\item \textbf{能耗真相}：一次普通性生活约 3--5 METs、持续 10--25 分钟，运动当量大致相当于快走两站地或爬两层楼，\textbf{远不足以"掏空"次日的体能}；真正消耗储备的是失眠与酗酒——而这两件事恰恰常与"赛前夜纵欲"捆绑出现，替性行为背了锅。
	\item \textbf{睾酮神话}："禁欲 7 天睾酮飙升"的说法源自小样本短期观察，波动幅度远未达到影响力量表现的程度；长期禁欲也不会积累"雄性资本"，性活动对静息睾酮的长远影响微乎其微。
	\item \textbf{研究证据}：多数针对力量、耐力、反应时的对照研究未发现赛前一夜性行为与运动表现的显著关联；个别研究提示赛前 2 小时内的性行为可能干扰需要高度专注项目的赛前唤醒——所以"留出恢复与睡眠的缓冲"即可，无需禁欲数天。
	\item \textbf{睡眠优先}：与其纠结禁不禁欲，不如保证赛前 7--9 小时睡眠；若性活动是入睡的助眠手段（性高潮后催产素与催乳素释放有助入睡），对次日状态反而是加分项。
	\item \textbf{个体化调整}：确有运动员自感性行为后"状态松懈"，这类主观差异值得尊重——重大赛事前几晚改为非性亲密（按摩、依偎）是两全方案；关键是与伴侣提前沟通，而不是突然冷淡让对方多想。
	\item \textbf{心态归位}：对"禁欲加分"的执念本身可能成为赛前焦虑源；把性生活当作与训练、饮食并列的日常管理项目，按自己的感受安排即可。
\end{itemize}

\begin{tcolorbox}[colback=pink!5!white,colframe=red!50!black,title=贴心小叮咛]
相关研究样本普遍偏小、项目差异大，本节为一般性证据综述，不构成个体化训练建议；职业运动员的赛前安排请以队医与教练团队方案为准。
\end{tcolorbox}

"""

# ---------- Block F: male, before HIV 感染者的生育选择 ----------
F = r"""\subparagraph{捐精者视角：报名、流程与责任}

上文讲的是精子库的制度设计；站在"想捐精的人"这一边，实际体验是这样的：

\begin{itemize}
	\item \textbf{基本门槛}：中国国籍的健康男性；多数精子库要求年龄 22--45 周岁、身高下限（常见 165cm 以上，各库不同）、无遗传病家族史、无高危行为史，部分库对学历另有要求——细则以当地人类精子库公告为准
	\item \textbf{通过率仅约两成}：初筛最难的是\textbf{精液质量关}——不仅新鲜精液要达标，还要求\textbf{冷冻复苏后活力仍然合格}，多数报名者正是在这一环节被淘汰。\textbf{被淘汰不等于不育}：许多被淘汰者自然生育能力完全正常，只是精液不耐冷冻这一关
	\item \textbf{完整流程}：报名预约 → 精液初筛 → 合格者抽血（传染病、染色体与常见遗传病基因筛查）及全身体检 → 签署知情同意书 → 正式供精（需多次采集，每次采集前禁欲 3--7 天）→ 精液冷冻检疫 6 个月 → 供精者复查 HIV 等阴性后，冻精方可投入使用
	\item \textbf{补助而非报酬}：供精属于人道主义行为，发放的是交通与误工补助（累计数千元，各库标准不同），"靠捐精赚钱"既不符合规定也行不通
	\item \textbf{义务与承诺}：如实告知个人及家族健康史；\textbf{不得同时向两家及以上精子库供精}；接受匿名与互盲安排，不查询、不接触受方家庭及后代；同一供精者的精液最多使 5 名妇女受孕，由各库联网控制
	\item \textbf{法律定位}：捐精者对供精所生的后代\textbf{不承担、也不享有任何法律上的抚养义务或亲权}；后代一般不获知捐精者身份——这是互盲制度的两面
	\item \textbf{心理准备}：有人会纠结"那些孩子算不算我的"——法律与伦理上均已明确不构成亲权关系；若这一关过不去，选择自精保存或退出供精都完全正当，供精过程中改变主意也可与精子库协商终止（已冷冻标本的处置以知情同意书为准）
\end{itemize}

"""

JOBS = [
    ("B-首次就诊", BOOK, B, r"""\section{需要尽快就医的"红旗"信号}"""),
    ("A-年度清单", BOOK, A, r"""\section{线上权威渠道}"""),
    ("C-分手影像", BOOK, C, r"""\subsection{网络性勒索（Sextortion）}"""),
    ("D-出差酒店", BOOK, D, r"""\section{饮食与性健康}""" + "\n\n" + r"""饮食是生活方式的重要组成部分"""),
    ("G-术语表",   BOOK, None, None),   # special
    ("E-赛前禁欲", MALE, E, r"""\section{环境内分泌干扰物与男性生殖健康}"""),
    ("F-捐精视角", MALE, F, r"""\subsection{HIV 感染者的生育选择（单阳家庭与洗精术）}"""),
]

ENVS = ["itemize", "enumerate", "tcolorbox", "description", "table", "tabularx", "center"]

def load(path):
    raw = open(path, "rb").read()
    return raw, raw.decode("utf-8")

def save(path, raw, s):
    open(path, "wb").write(s.encode("utf-8"))

def check_body(name, body):
    for e in ENVS:
        x = len(re.findall(r"\\begin\{" + e + r"\}", body))
        y = len(re.findall(r"\\end\{" + e + r"\}", body))
        if x != y:
            raise SystemExit("FAIL %s: env %s begin=%d end=%d" % (name, e, x, y))
    bo, bc = body.count("{"), body.count("}")
    if bo != bc:
        raise SystemExit("FAIL %s: braces {=%d }=%d" % (name, bo, bc))
    return bo

def insert(path, name, body, anchor):
    raw, s = load(path)
    if b"\r\n" in raw:
        body = body.replace("\n", "\r\n")
        anchor = anchor.replace("\n", "\r\n")
    title = re.match(r"\\(?:section|subsection|subsubsection|subparagraph)\{[^}]*\}", body)
    if title and title.group(0) in s:
        print("SKIP(already in) %s" % name)
        return
    n = s.count(anchor)
    if n != 1:
        raise SystemExit("FAIL %s: anchor count=%d" % (name, n))
    check_body(name, body.replace("\r\n", "\n"))
    s2 = s.replace(anchor, body + anchor, 1)
    save(path, raw, s2)
    print("OK %s  (+%d chars, braces balanced)" % (name, len(body)))

def glossary(path):
    raw, s = load(path)
    if "非自愿亲密影像（NCII）" in s:
        print("SKIP(already in) G-术语表")
        return
    g_old, g_new = G_OLD, G_NEW
    if b"\r\n" in raw:
        g_old = g_old.replace("\n", "\r\n")
        g_new = g_new.replace("\n", "\r\n")
    n = s.count(g_old)
    if n != 1:
        raise SystemExit("FAIL G: anchor count=%d" % n)
    # brace check on the added item lines only (exclude the anchor's \end{description})
    added = g_new[len(g_old):]
    core = added.replace("\r", "")
    if core.endswith("\n\\end{description}"):
        core = core[: -len("\n\\end{description}")]
    elif core.endswith("\\end{description}"):
        core = core[: -len("\\end{description}")]
    bo, bc = core.count("{"), core.count("}")
    if bo != bc:
        raise SystemExit("FAIL G: braces {=%d }=%d" % (bo, bc))
    s2 = s.replace(g_old, g_new, 1)
    save(path, raw, s2)
    print("OK G-术语表  (+%d chars)" % len(added))

def report(path):
    raw, s = load(path)
    print("-- %s  (%d chars)" % (path.split("\\")[-1], len(s)))
    for e in ENVS:
        x = len(re.findall(r"\\begin\{" + e + r"\}", s))
        y = len(re.findall(r"\\end\{" + e + r"\}", s))
        flag = "" if x == y else "   <<< MISMATCH"
        print("   %-11s begin=%-4d end=%-4d%s" % (e, x, y, flag))
    print("   braces: {=%d }=%d delta=%d" % (s.count("{"), s.count("}"), s.count("{") - s.count("}")))

for name, path, body, anchor in JOBS:
    if name == "G-术语表":
        glossary(path)
    else:
        insert(path, name, body, anchor)

print("")
print("===== global check after insertion =====")
report(BOOK)
report(MALE)
print("ALL DONE")
