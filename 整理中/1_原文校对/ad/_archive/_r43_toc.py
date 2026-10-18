# -*- coding: utf-8 -*-
"""第四十三轮：重生成三卷目录总览（新增 16 节：book 12 / female 2 / male 2）"""
import re, io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OLD = BASE + r"\_全书导览_三卷目录总览_2026-09-10.md"
OUT = OLD
FILES = [("book.tex", "综合卷"), ("female.tex", "女性卷"), ("male.tex", "男性卷")]

# 精确固化历轮新增（按 文件+标题 匹配），防同名继承污染
FILE_STAR = {
    # r41
    ("book.tex", "丁克家庭：选择不育生活的亲密关系经营"),
    ("book.tex", "性行为中的意外损伤与家庭急救"),
    ("book.tex", "烧伤、毁容与截肢者的性重建：当身体图式被改变"),
    ("book.tex", "异地恋与长期分离的亲密维护"),
    ("book.tex", "数字遗产与身后的亲密痕迹"),
    # r40
    ("book.tex", "年龄差伴侣：忘年恋的亲密与挑战"),
    ("book.tex", "皮肤可见疾病与性自信：银屑病、湿疹、白癜风与暴露焦虑"),
    ("book.tex", "职场恋情与权力不对等：办公室、上下级与师生"),
    # r38
    ("book.tex", "新手父母的性生活：睡眠、分工与碎片时间"),
    ("book.tex", "慢性腰痛与腰椎问题者的性姿势"),
    ("book.tex", "倒班与加班：作息错位下的性生活"),
    # r37
    ("book.tex", "男性的性反应"),
    ("male.tex", "消退期"),
}

# r43 新增 16 节（用前缀匹配，规避标题内引号字符差异）
R43_PREFIX = {
    ("book.tex", "坦陀罗、密宗与慢爱"),
    ("book.tex", "性拒绝的处理"),
    ("book.tex", "继亲家庭"),
    ("book.tex", "复婚"),
    ("book.tex", "留学生与移民的性健康调适"),
    ("book.tex", "间性人群的成年期支持"),
    ("book.tex", "视障与听障者的性健康"),
    ("book.tex", "智力障碍者的性权利与性教育"),
    ("book.tex", "独居与长期无伴侣者的性需求"),
    ("book.tex", "造口者的亲密与性重建"),
    ("book.tex", "睡眠呼吸暂停与勃起功能障碍：一条被忽视的链条"),
    ("book.tex", "老年 HIV 新发感染"),
    ("female.tex", "依恋风格与女性的亲密之性"),
    ("female.tex", "绝经之后"),
    ("male.tex", "睡眠呼吸暂停与勃起功能障碍"),
    ("male.tex", "依恋风格与男性在亲密关系中的性"),
}

STRIP_SHORT = {"消退期", "男性的性反应", "兴奋期", "平台期", "高潮期", "女性的性反应"}

PREFIXES = [
    "漏服之后怎么办", "停用之后还能怀上吗", "避孕责任：谁承担",
    "经期性行为的常见疑问速答", "经期性行为的实操与舒适度", "经期还能做什么",
    "经血逆流与子宫内膜异位症", "背叛创伤", "修复或不修复",
    "绳缚的神经与循环安全", "灌肠的安全边界", "跨性别者就医流程实务",
    "同性伴侣的法律事务", "\u201c安全细节补遗\u201d", "口交、乳交、肛交的安全细节补遗",
    "强奸创伤综合征与报案决策", "熟人强奸与", "女同性恋者获取性健康服务的障碍",
    "女性性少数者的社群与支持资源", "女女性行为实践", "药物辅助性侵",
    "\u201c捡尸\u201d与酒后失能", '"捡尸"与酒后失能', "捡尸\u201d与酒后失能",
    "体位补遗", "多人性行为", "色情与勃起功能障碍", "同志桑拿",
    "中医方剂补遗", "壮阳中药与西药的相互作用", "传统功法的安全审视",
    '"以形补形"', "电击类玩具", "乳头夹", "BDSM 后的情绪跌落",
]

starred = set()
if os.path.exists(OLD):
    for line in io.open(OLD, encoding="utf-8"):
        if "★" in line:
            m = re.search(r"｜(.+?)★", line.rstrip("\n"))
            if m:
                starred.add(m.group(1).strip())
starred -= STRIP_SHORT

data = {}
for fn, label in FILES:
    raw = open(os.path.join(BASE, fn), "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    lines = raw.decode("utf-8").split(crlf)
    ents = []
    nc = ns = nsub = 0
    for i, line in enumerate(lines, 1):
        st = line.strip()
        if st.startswith("%"):
            continue
        m = re.match(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}", st)
        if not m:
            continue
        lvl, title = m.group(1), m.group(2).strip()
        if not title:
            continue
        if lvl == "chapter":
            ents.append((0, i, title)); nc += 1
        elif lvl == "section":
            ents.append((1, i, title)); ns += 1
        elif lvl == "subsection":
            ents.append((2, i, title)); nsub += 1
        else:
            ents.append((3, i, title)); nsub += 1
    dch = {}
    for lv, i, t in ents:
        if lv == 0:
            dch.setdefault(t, []).append(i)
    dup_ch = [(t, ls) for t, ls in dch.items() if len(ls) > 1]
    dse = {}
    for lv, i, t in ents:
        if lv == 1:
            dse.setdefault(t, []).append(i)
    dup_se = sorted([(t, ls) for t, ls in dse.items() if len(ls) > 1], key=lambda x: -len(x[1]))
    data[fn] = dict(label=label, nlines=len(lines), ents=ents, nc=nc, ns=ns, nsub=nsub,
                    dup_ch=dup_ch, dup_se=dup_se)

out = []
out.append("# 三卷全书导览（目录总览·含行号）")
out.append("")
out.append("> 生成日期：2026-09-16（第四十三轮扩写后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")
out.append("> 说明：行号为当前文件实际行号；带 ★ 的标题为历轮新增/扩充内容所在处。")
out.append("> 本轮（第四十三轮）新增 16 节（纯插入，未动任何现有内容）：综合卷 12 节——《坦陀罗、密宗与慢爱：不以高潮为目标的性实践》《性拒绝的处理：被拒绝方与拒绝方的对话机制》《继亲家庭：亲密、边界与时间分配》《复婚：复合之后的信任重建与性》《留学生与移民的性健康调适》《间性人群的成年期支持：从被治疗的对象到主体》《视障与听障者的性健康》《智力障碍者的性权利与性教育》《独居与长期无伴侣者的性需求》《造口者的亲密与性重建》《睡眠呼吸暂停与勃起功能障碍：一条被忽视的链条》《老年 HIV 新发感染：一个被忽略的防艾盲区》；女性卷 2 节——《依恋风格与女性的亲密之性》《绝经之后：中老年女性的亲密、独居与再婚》；男性卷 2 节——《睡眠呼吸暂停与勃起功能障碍》《依恋风格与男性在亲密关系中的性》。另向术语表补入 12 个新词条（坦陀罗、慢爱、性拒绝、性欲差异、复婚、继亲家庭、造口、间性、依恋风格、OSA、GSM、U=U）。")
out.append("> 上轮（第四十一轮）：填充 132 处 0 字空标题骨架（综合卷 43 / 女性卷 73 / 男性卷 16）；新增 5 节（综合卷：《性行为中的意外损伤与家庭急救》《丁克家庭：选择不育生活的亲密关系经营》《异地恋与长期分离的亲密维护》《烧伤、毁容与截肢者的性重建》《数字遗产与身后的亲密痕迹》）；术语表补 6 词条。")
out.append("> 第四十轮新增 3 节（均在综合卷）：《年龄差伴侣：忘年恋的亲密与挑战》（性与多元关系节前）、《皮肤可见疾病与性自信：银屑病、湿疹、白癜风与暴露焦虑》（性创伤与心理康复节前）、《职场恋情与权力不对等：办公室、上下级与师生》（特殊职业人群的性健康节前）。")
out.append("> 第三十九轮无新增标题：全量修复三卷 Markdown 格式残留（约 3000 对粗体、约 22000 行 bullet、2 个表格转 LaTeX 环境），行号全面变动。")
out.append("> 第三十八轮新增 3 节（均在综合卷）：《新手父母的性生活：睡眠、分工与碎片时间》（育儿与夫妻关系节内末尾）、《慢性腰痛与腰椎问题者的性姿势》（残疾伴侣辅助姿势节前）、《倒班与加班：作息错位下的性生活》（出差旅行与酒店节前）。")
out.append("> 第三十七轮新增 2 节：综合卷《男性的性反应》（女性的性反应节后）；男性卷《消退期》（补齐男性四期缺环）。")
out.append("> 第三十六轮新增 7 节：综合卷 4 节——《漏服之后怎么办：口服避孕药的差错处理》《停用之后还能怀上吗：各类避孕方法的生育力恢复》《避孕责任：谁承担、怎么谈》《经期性行为的常见疑问速答》；女性卷 3 节——《经期性行为的实操与舒适度：体位、浸染与用品》《经期还能做什么：口交、肛交、自慰与\u201c高潮能缓解痛经吗\u201d》《经血逆流与子宫内膜异位症：经期性交会加重吗？》。")
out.append("> 第三十五轮新增 4 节 + 1 处更正：综合卷《背叛创伤》《修复或不修复》《绳缚的神经与循环安全》《灌肠的安全边界》，并更正原\u201c绳索痕迹用热敷\u201d一句。")
out.append("")
for fn, _ in FILES:
    d = data[fn]
    out.append("## %s %s（%d 行；章 %d / 节 %d / 子节 %d）" % (
        d["label"], fn, d["nlines"], d["nc"], d["ns"], d["nsub"]))
    out.append("")
    if d["dup_ch"]:
        parts = ["「%s」@%s" % (t, ",".join(str(x) for x in ls)) for t, ls in d["dup_ch"]]
        out.append("- **重名章 %d 组**：%s" % (len(parts), "；".join(parts)))
    if d["dup_se"]:
        parts = ["「%s」×%d" % (t, len(ls)) for t, ls in d["dup_se"][:12]]
        out.append("- **重名节共 %d 组（前12）**：%s" % (len(d["dup_se"]), "；".join(parts)))
    out.append("")
    ind = ["**", "　　", "　　　　", "　　　　　　"]
    for lv, i, t in d["ents"]:
        if (fn, t) in FILE_STAR:
            star = "★"
        elif any(rfn == fn and t.startswith(p) for rfn, p in R43_PREFIX):
            star = "★"
        elif any(t.startswith(p) for p in PREFIXES) or t.startswith("阴吹（阴道排气）") or t.startswith("子宫后位：正常变异") or t.startswith("婚姻内的同意：结婚证不是") or t.startswith("偶遇性行为"):
            star = "★"
        elif t in starred:
            star = "★"
        else:
            star = ""
        out.append("**%d｜%s**%s" % (i, t, star) if lv == 0 else "%s%d｜%s%s" % (ind[lv], i, t, star))
    out.append("")
open(OUT, "wb").write("\n".join(out).encode("utf-8"))

nstar = sum(1 for ln in out if "★" in ln and not ln.startswith("#") and not ln.startswith(">"))
print("written:", OUT)
print("entity star lines:", nstar)
for fn, _ in FILES:
    d = data[fn]
    print("%s: %d 行, ch=%d sec=%d sub=%d, dup_ch=%d dup_sec=%d" % (
        fn, d["nlines"], d["nc"], d["ns"], d["nsub"], len(d["dup_ch"]), len(d["dup_se"])))
