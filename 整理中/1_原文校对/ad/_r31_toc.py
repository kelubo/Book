# -*- coding: utf-8 -*-
"""第三十一轮：重生成三卷目录总览（更新行号 + 本轮 10 个新★，沿用上轮文件累积★）"""
import re, io, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OLD = BASE + r"\_全书导览_三卷目录总览_2026-09-10.md"
OUT = OLD
FILES = [("book.tex", "综合卷"), ("female.tex", "女性卷"), ("male.tex", "男性卷")]

STAR_LEVEL = {}  # 本轮全部走前缀匹配（引号码位不定）
PREFIXES = [
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

starred = set(STAR_LEVEL.keys())
if os.path.exists(OLD):
    for line in io.open(OLD, encoding="utf-8"):
        if "★" in line:
            m = re.search(r"｜(.+?)★", line.rstrip("\n"))
            if m:
                starred.add(m.group(1).strip())

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
out.append("> 生成日期：2026-09-14（第三十一轮扩写后重新生成） ｜ 路径：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")
out.append("> 说明：行号为当前文件实际行号；带 ★ 的标题为历轮新增/扩充内容所在处。")
out.append("> 本轮（第三十一轮）新增 10 节（均在综合卷）：SM 域《电击类玩具（e-stim）的安全使用》《乳头夹与夹具：佩戴安全细节》《BDSM 后的情绪跌落（Sub Drop / Top Drop）：机制、识别与照护》（SM的健康与安全节尾）；中医域《中医方剂补遗：五子衍宗丸、左归丸与蛇床子》《壮阳中药与西药的相互作用：同服之前必读》（中药治疗后）《传统功法的安全审视：铁裆功、气功导引与提肛》《\"以形补形\"与壮阳食疗：传统说法的现代审视》（中医性养生保健方法后）；其他《色情与勃起功能障碍：\"色情诱导 ED\"之争与使用自查》（VR 成瘾小节后）《多人性行为（3P / 群交 / 换偶）的安全与协商：当伴侣数大于二》（偶遇性行为守则节后）《同志桑拿与性场所：文化、安全与法律》（LGBTQ+ 促进策略前）。")
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
        if any(t.startswith(p) for p in PREFIXES) or t.startswith("阴吹（阴道排气）") or t.startswith("子宫后位：正常变异") or t.startswith("婚姻内的同意：结婚证不是") or t.startswith("偶遇性行为"):
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
print("starred carried(set):", len(starred))
print("entity star lines (历轮口径需+1头部说明行):", nstar)
for fn, _ in FILES:
    d = data[fn]
    print("%s: %d 行, ch=%d sec=%d sub=%d, dup_ch=%d dup_sec=%d" % (
        fn, d["nlines"], d["nc"], d["ns"], d["nsub"], len(d["dup_ch"]), len(d["dup_se"])))
