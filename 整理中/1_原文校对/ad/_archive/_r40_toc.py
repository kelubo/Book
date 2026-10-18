# -*- coding: utf-8 -*-
"""第四十轮：重生成三卷目录总览（新增 3 节 + 行号更新）"""
import re, io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OLD = BASE + r"\_全书导览_三卷目录总览_2026-09-10.md"
OUT = OLD
FILES = [("book.tex", "综合卷"), ("female.tex", "女性卷"), ("male.tex", "男性卷")]

# 精确固化历轮新增（按 文件+标题 匹配），防同名继承污染
FILE_STAR = {
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

# 同名短标题跨卷污染剥离
STRIP_SHORT = {"消退期", "男性的性反应", "兴奋期", "平台期", "高潮期", "女性的性反应"}

PREFIXES = [
    "漏服之后怎么办",
    "停用之后还能怀上吗",
    "避孕责任：谁承担",
    "经期性行为的常见疑问速答",
    "经期性行为的实操与舒适度",
    "经期还能做什么",
    "经血逆流与子宫内膜异位症",
    "背叛创伤",
    "修复或不修复",
    "绳缚的神经与循环安全",
    "灌肠的安全边界",
    "跨性别者就医流程实务",
    "同性伴侣的法律事务",
    "\u201c安全细节补遗\u201d",
    "口交、乳交、肛交的安全细节补遗",
    "强奸创伤综合征与报案决策",
    "熟人强奸与",
    "女同性恋者获取性健康服务的障碍",
    "女性性少数者的社群与支持资源",
    "女女性行为实践",
    "药物辅助性侵",
    "\u201c捡尸\u201d与酒后失能",
    '"捡尸"与酒后失能',
    "捡尸\u201d与酒后失能",
    "体位补遗",
    "多人性行为",
    "色情与勃起功能障碍",
    "同志桑拿",
    "中医方剂补遗",
    "壮阳中药与西药的相互作用",
    "传统功法的安全审视",
    '"以形补形"',
    "电击类玩具",
    "乳头夹",
    "BDSM 后的情绪跌落",
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
out.append("> 生成日期：2026-09-15（第四十轮扩写后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")
out.append("> 说明：行号为当前文件实际行号；带 ★ 的标题为历轮新增/扩充内容所在处。")
out.append("> 本轮（第四十轮）新增 3 节（均在综合卷，纯插入未动现有内容）：《年龄差伴侣：忘年恋的亲密与挑战》（性与恋爱关系章，《性与多元关系》节前）、《皮肤可见疾病与性自信：银屑病、湿疹、白癜风与暴露焦虑》（身体形象与性章末，《性创伤与心理康复》节前）、《职场恋情与权力不对等：办公室、上下级与师生》（神经多样性节后，《特殊职业人群的性健康》节前）。")
out.append("> 上轮（第三十九轮）无新增标题：全量修复三卷 Markdown 格式残留（约 3000 对粗体、约 22000 行 bullet、2 个表格转 LaTeX 环境），行号全面变动。")
out.append("> 第三十八轮新增 3 节（均在综合卷）：《新手父母的性生活：睡眠、分工与碎片时间》（育儿与夫妻关系节内末尾）、《慢性腰痛与腰椎问题者的性姿势》（残疾伴侣辅助姿势节前）、《倒班与加班：作息错位下的性生活》（出差旅行与酒店节前）。")
out.append("> 第三十七轮新增 2 节：综合卷《男性的性反应》（女性的性反应节后，四期结构与女性版对称）；男性卷《消退期》（补齐男性四期缺环，呼应前文不应期两专节）。")
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
print("entity star lines (累积口径需+1头部说明行):", nstar)
for fn, _ in FILES:
    d = data[fn]
    print("%s: %d 行, ch=%d sec=%d sub=%d, dup_ch=%d dup_sec=%d" % (
        fn, d["nlines"], d["nc"], d["ns"], d["nsub"], len(d["dup_ch"]), len(d["dup_se"])))
