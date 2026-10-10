# -*- coding: utf-8 -*-
"""r77: 导出旧区「第四篇：性交体位与姿势艺术」(L27245~27842) 的完整结构 + 样本正文。"""
import io, re

H = re.compile(r"^\\(part|chapter|section|subsection|subsubsection)\*?\{(.*)\}\s*$")
lines = [x.rstrip("\r") for x in io.open("book.tex", encoding="utf-8", newline="").read().split("\n")]
A, B = 27245, 27842

out = []
toks = []
for i in range(A - 1, B):
    m = H.match(lines[i])
    if m:
        toks.append((i, m.group(1), m.group(2)))
toks.append((B, None, None))
for k in range(len(toks) - 1):
    i, lvl, t = toks[k]
    nxt = toks[k + 1][0]
    if lvl in ("part", "chapter", "section", "subsection"):
        out.append("  L%-6d %-13s %-4d 行  %s%s" % (i + 1, lvl, nxt - i,
                   "  " * {"part": 0, "chapter": 1, "section": 2, "subsection": 3}[lvl], t))
txt = "\n".join(out)
io.open("_r77_part4.txt", "w", encoding="utf-8", newline="").write(txt + "\n")
print(txt)
