# -*- coding: utf-8 -*-
"""r40 探测第 2 轮：骨架空标题分布统计（空花括号 + 空壳节两种口径），按章汇总"""
import re, os

BASE = r"D:\Git\Book\整理中\1_原文校对\ad"
FILES = ["book.tex", "female.tex", "male.tex"]

HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{([^{}]*)\}")
EMPTY_HDR = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph)\{\s*\}")

for fn in FILES:
    raw = open(os.path.join(BASE, fn), "rb").read()
    crlf = "\r\n" if b"\r\n" in raw else "\n"
    lines = raw.decode("utf-8").split(crlf)
    # 结构扫描
    ents = []  # (level, line, title)
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith("%"):
            continue
        m = HDR.match(st)
        if m:
            ents.append((m.group(1), i, m.group(2).strip()))
    lv_order = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3, "subparagraph": 4}
    # 空壳判定：标题 i 之后到下一个 lv<=自身 的标题之间，无非空非注释行（且不含 \begin{itemize} 等内容）
    hollow = []  # (level, line, title, chars)
    for idx, (lv, i, t) in enumerate(ents):
        end = len(lines)
        for lv2, j, _ in ents[idx + 1:]:
            if lv_order[lv2] <= lv_order[lv]:
                end = j - 1
                break
        chars = 0
        for ln in lines[i:end]:  # i 是 1 基，lines[i] 即标题下一行
            st = ln.strip()
            if not st or st.startswith("%"):
                continue
            chars += len(st)
        if chars < 30:  # 不足 30 字符视为空壳
            hollow.append((lv, i, t, chars))
    empty_brace = sum(1 for lv, i, t in ents if not t)
    print("== %s ==" % fn)
    print("   空花括号标题 {}：%d 处；内容空壳(<30字)：%d 处" % (empty_brace, len(hollow)))
    # 按所属章聚合空壳
    bych = {}
    cur_ch = "(卷首)"
    for lv, i, t in ents:
        if lv == "chapter":
            cur_ch = t if t else "(未命名章)"
        if any(h[1] == i for h in hollow):
            bych.setdefault(cur_ch, []).append((i, t if t else "(空标题)"))
    for ch, items in sorted(bych.items(), key=lambda x: -len(x[1]))[:18]:
        print("   [%3d 处] %s" % (len(items), ch[:60]))
    print()
