# -*- coding: utf-8 -*-
"""扫描三卷中的"空标题"（标题行后直接跟下一个标题，无正文）"""
import re, os
BASE = r"D:/Git/Book/整理中/1_原文校对/ad"
HEAD = re.compile(r"\\(chapter|section|subsection|subsubsection|subparagraph|paragraph)\{")
for fn in ["book.tex", "female.tex", "male.tex"]:
    with open(os.path.join(BASE, fn), encoding="utf-8", newline="") as f:
        lines = f.read().replace("\r\n", "\n").split("\n")
    heads = []
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if st.startswith("%"):
            continue
        m = HEAD.match(st)
        if m:
            heads.append((i, m.group(1), st))
    print(f"=== {fn} 空标题 ===")
    cnt = 0
    for idx, (i, lvl, st) in enumerate(heads):
        # 下一个标题
        if idx + 1 >= len(heads):
            continue
        ni, nlvl, nst = heads[idx + 1]
        # 中间有无非空、非注释内容
        mid = [l for l in lines[i:ni-1] if l.strip() and not l.strip().startswith("%")]
        if not mid:
            cnt += 1
            print(f"  L{i} [{lvl}] {st[:52]}   -> 下一标题 L{ni}")
    print(f"  合计空标题: {cnt}\n")
