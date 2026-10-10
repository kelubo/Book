# -*- coding: utf-8 -*-
"""Regenerate the three-volume TOC overview markdown with current line numbers.
Carries over old ★ marks by title, adds this round's marks."""
import re, io

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
OUT = BASE + r"\_全书导览_三卷目录总览_2026-09-08.md"
FILES = [("book.tex", "综合卷"), ("female.tex", "女性卷"), ("male.tex", "男性卷")]

NEW_STAR = {
    "第一次就诊：流程、如何开口与费用参考",
    "年度性健康自查清单",
    "分手之后：协商删除与隐私重建",
    "出差、旅行与酒店：路上的性健康",
    "赛前禁欲与运动表现：迷思与真相",
    "捐精者视角：报名、流程与责任",
}

# --- collect old starred titles ---
starred = set(NEW_STAR)
try:
    for line in io.open(OUT, encoding="utf-8"):
        if "★" in line:
            m = re.search(r"｜(.+?)★", line.rstrip("\n"))
            if m:
                starred.add(m.group(1).strip())
except FileNotFoundError:
    pass

data = {}
for fn, label in FILES:
    raw = open(BASE + "\\" + fn, "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    lines = raw.decode("utf-8").split(crlf)
    ents = []
    chapters, sections, subs = [], [], 0
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
            ents.append((0, i, title)); chapters.append(title)
        elif lvl == "section":
            ents.append((1, i, title)); sections.append(title)
        elif lvl == "subsection":
            ents.append((2, i, title)); subs += 1
        else:  # subsubsection / subparagraph
            ents.append((3, i, title)); subs += 1
    # duplicate chapter groups with line numbers
    dch = {}
    for lv, i, t in ents:
        if lv == 0:
            dch.setdefault(t, []).append(i)
    dup_ch = [(t, ls) for t, ls in dch.items() if len(ls) > 1]
    dse = {}
    for lv, i, t in ents:
        if lv == 1:
            dse.setdefault(t, []).append(i)
    dup_se = sorted([(t, ls) for t, ls in dse.items() if len(ls) > 1],
                    key=lambda x: -len(x[1]))
    data[fn] = dict(label=label, nlines=len(lines), ents=ents,
                    nc=len(chapters), ns=len(sections), nsub=subs,
                    dup_ch=dup_ch, dup_se=dup_se)

out = []
out.append("# 三卷全书导览（目录总览·含行号）")
out.append("")
out.append("> 生成日期：2026-09-08（第十四轮扩写后重新生成） ｜ 文件：整理中/1_原文校对/ad/ ｜ 用途：审校/合并/阅读导航底图")
out.append("> 说明：行号为当前文件实际行号；带 ★ 的标题为本项目历轮新增/扩充内容所在处。本轮新增：年度性健康自查清单、首次就诊流程与费用、分手后影像协商删除、出差旅行酒店性健康（综合卷），赛前禁欲迷思、捐精者视角（男性卷），术语表补 3 条。")
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
        star = "★" if t in starred else ""
        if lv == 0:
            out.append("**%d｜%s**%s" % (i, t, star))
        else:
            out.append("%s%d｜%s%s" % (ind[lv], i, t, star))
    out.append("")
open(OUT, "wb").write("\n".join(out).encode("utf-8"))
print("written:", OUT)
print("lines:", len(out), "| starred titles carried:", len(starred))
for fn, _ in FILES:
    d = data[fn]
    print("%s: %d lines, ch=%d sec=%d sub=%d, dup_ch=%d dup_sec=%d" % (
        fn, d["nlines"], d["nc"], d["ns"], d["nsub"], len(d["dup_ch"]), len(d["dup_se"])))
